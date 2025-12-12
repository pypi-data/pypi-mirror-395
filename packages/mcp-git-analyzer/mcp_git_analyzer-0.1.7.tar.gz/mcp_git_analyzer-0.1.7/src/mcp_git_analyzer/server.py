"""MCP Git Analyzer Server - FastMCP implementation."""

from typing import Annotated, Literal
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server.fastmcp import FastMCP, Context
from mcp.types import ToolAnnotations

from mcp_git_analyzer.db import Database
from mcp_git_analyzer.tools import GitTools, AnalysisTools, SearchTools, ReportTools, AlgorithmTools


@dataclass
class AppContext:
    """Application context with typed dependencies."""
    db: Database
    git: GitTools
    analysis: AnalysisTools
    search: SearchTools
    report: ReportTools
    algorithm: AlgorithmTools


# Lifespan context to manage database and tools
@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Initialize database and tools on startup."""
    db = Database()
    git_tools = GitTools(db)
    analysis_tools = AnalysisTools(db)
    search_tools = SearchTools(db)
    report_tools = ReportTools(db, analysis_tools, search_tools)
    algorithm_tools = AlgorithmTools(db)
    
    yield AppContext(
        db=db,
        git=git_tools,
        analysis=analysis_tools,
        search=search_tools,
        report=report_tools,
        algorithm=algorithm_tools
    )


# Server instructions for AI assistants
SERVER_INSTRUCTIONS = """
## MCP Git Analyzer - Usage Guidelines

### Recommended Workflow
1. `clone_repo` → Clone target repository
2. `analyze_repo` → Parse and extract all symbols/patterns
3. `get_api_summary` or `get_public_api` → Get API listing for porting
4. `generate_report("api_summary")` → Complete formatted report
5. `list_symbols`, `find_patterns` → Explore specifics
6. `read_file`, `search_in_files` → Access actual source code directly

### IMPORTANT: Source Code Access
After cloning a repository, you have DIRECT access to all source files:
- Use `read_file` to view file contents (no external fetch needed)
- Use `search_in_files` for grep-like text search across files
- Use `inspect_symbol` to get source code for specific functions/classes
Do NOT fetch from GitHub URLs - the code is already local!

### CRITICAL: grounded_values Rules
Many tools return a `grounded_values` field containing:
- Exact counts that MUST be used in your response
- `must_quote` list of fields to include verbatim
- These values are extracted from actual code - DO NOT estimate or guess

Example tool output:
```json
"grounded_values": {
    "total_functions": 44,
    "total_types": 8,
    "must_quote": ["functions[*].name", "statistics.*"]
}
```
You MUST say "44개의 함수" not "약 40개" or "50+".

### CRITICAL: Number/Count Rules
- ALWAYS use exact values from `statistics` or `grounded_values`
- NEVER estimate with "50+", "약 40개", "numerous" - use actual counts
- If a count is not available from tools, say "정확한 개수는 확인 필요"

### Response Structure (for porting/migration tasks)
Your response MUST include these THREE sections in order:

#### 1. 원본 라이브러리 기능 요약 (Source Library Summary)
**Use `get_api_summary` or `get_public_api` formatted_summary field directly.**
- List ALL functions from tool output (not a subset)
- Show file-by-file breakdown with exact function names
- Include signatures from `functions[].signature` field
- DO NOT add functions that don't exist in tool output

Example:
```markdown
### 헤더 파일 (Public API)

#### `fastlog.h` (4개 함수)
- `float fastlog2f(float x)`
- `float fastlogf(float x)`
- `float fasterlog2f(float x)`
- `float fasterlogf(float x)`
```

#### 2. 설계/아키텍처 (Design/Architecture)
- Map each source file to target module using actual file names
- Define public API based on functions from step 1
- Use patterns from `find_patterns` results

#### 3. 마이그레이션 로드맵 (Migration Roadmap)
- Phase 1: Core functionality (list specific function names from API summary)
- Phase 2: Extended features
- Phase 3: Testing & optimization

### Verbatim Fields (MUST show in response)
| Tool | Field | How to Use |
|------|-------|------------|
| `get_public_api` | `formatted_summary` | Copy directly into response |
| `get_public_api` | `grounded_values.total_*` | Use exact numbers |
| `get_api_summary` | `summary` (markdown) | Copy directly into response |
| `get_file_analysis` | `symbols[].signature` | Show exact signatures |
| `list_algorithms` | `algorithms[].symbol_name` | List actual names |
| `inspect_symbol` | `source_code` | Quote in code block |
| `read_file` | `content` | Quote actual file content |
| `search_in_files` | `results[].line` | Show matching lines |

### For Detailed Guidelines
Read resources:
- `guidelines://tool-usage` - Comprehensive tool usage
- `guidelines://response-structure` - Response templates for porting analysis
""".strip()


# Initialize MCP server
mcp = FastMCP(
    "Git Analyzer",
    lifespan=lifespan,
    instructions=SERVER_INSTRUCTIONS
)


# ============================================================================
# Git Management Tools
# ============================================================================

@mcp.tool(
    annotations=ToolAnnotations(
        title="Clone Repository",
        readOnlyHint=False,
        idempotentHint=True,
        openWorldHint=True
    )
)
def clone_repo(
    url: Annotated[str, "Git repository URL (HTTPS or SSH)"],
    branch: Annotated[str | None, "Branch to checkout (default: repository's default branch)"] = None,
    ctx: Context = None
) -> dict:
    """
    Clone a Git repository for analysis.
    
    Downloads the repository to local storage and registers it in the database.
    Use this before analyzing a repository.
    """
    git: GitTools = ctx.request_context.lifespan_context.git
    return git.clone_repo(url, branch)


@mcp.tool(
    annotations=ToolAnnotations(
        title="List Repositories",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def list_repos(ctx: Context = None) -> dict:
    """
    List all registered repositories.
    
    Returns all repositories that have been cloned, along with their
    analysis status and basic statistics.
    """
    git: GitTools = ctx.request_context.lifespan_context.git
    return git.list_repos()


@mcp.tool(
    annotations=ToolAnnotations(
        title="Get Repository File Tree",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def get_repo_tree(
    repo_id: Annotated[int, "Repository ID from list_repos"],
    max_depth: Annotated[int, "Maximum directory depth to show"] = 3,
    ctx: Context = None
) -> dict:
    """
    Get the file structure of a repository.
    
    Returns a tree view of directories and files with language detection.
    Useful for understanding project organization.
    """
    git: GitTools = ctx.request_context.lifespan_context.git
    return git.get_repo_tree(repo_id, max_depth)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Delete Repository",
        readOnlyHint=False,
        destructiveHint=True,
        idempotentHint=True
    )
)
def delete_repo(
    repo_id: Annotated[int, "Repository ID to delete"],
    delete_files: Annotated[bool, "Also delete cloned files from disk"] = False,
    ctx: Context = None
) -> dict:
    """
    Delete a repository from the database.
    
    Removes the repository record and all associated analysis data.
    Optionally deletes the cloned files from disk.
    """
    git: GitTools = ctx.request_context.lifespan_context.git
    return git.delete_repo(repo_id, delete_files)


# ============================================================================
# Analysis Tools
# ============================================================================

@mcp.tool(
    annotations=ToolAnnotations(
        title="Analyze Repository",
        readOnlyHint=False,
        idempotentHint=True
    )
)
async def analyze_repo(
    repo_id: Annotated[int, "Repository ID to analyze"],
    languages: Annotated[list[str] | None, "Languages to analyze (default: all supported)"] = None,
    include_call_graph: Annotated[bool, "Extract function call graph (optional, slower)"] = False,
    ctx: Context = None
) -> dict:
    """
    Analyze all files in a repository.
    
    Parses source code to extract:
    - Functions, classes, and methods with signatures
    - Docstrings and documentation
    - Import statements and dependencies
    - Algorithm and design patterns
    - Function call graph (optional)
    
    Results are stored in the database for future queries.
    """
    analysis: AnalysisTools = ctx.request_context.lifespan_context.analysis
    
    # Report progress
    msg = f"Starting analysis of repository {repo_id}"
    if include_call_graph:
        msg += " (with call graph extraction)"
    await ctx.info(msg)
    
    result = analysis.analyze_repo(repo_id, languages, include_call_graph)
    
    if result.get("status") == "success":
        stats = result.get("statistics", {})
        msg = f"Completed: {stats.get('analyzed_files', 0)} files, {stats.get('total_symbols', 0)} symbols"
        if include_call_graph:
            msg += f", {stats.get('total_calls', 0)} calls"
        await ctx.info(msg)
    
    return result


@mcp.tool(
    annotations=ToolAnnotations(
        title="Get File Analysis",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def get_file_analysis(
    repo_id: Annotated[int, "Repository ID"],
    file_path: Annotated[str, "Relative path to file within repository"],
    ctx: Context = None
) -> dict:
    """
    Get detailed analysis for a specific file.
    
    Returns all extracted symbols, imports, and detected patterns
    for the specified file.
    """
    analysis: AnalysisTools = ctx.request_context.lifespan_context.analysis
    return analysis.get_file_analysis(repo_id, file_path)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Get Symbol Details",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def get_symbol_details(
    symbol_name: Annotated[str, "Name of the symbol (function, class, method)"],
    repo_id: Annotated[int | None, "Repository ID to limit search"] = None,
    ctx: Context = None
) -> dict:
    """
    Get detailed information about a symbol.
    
    Returns signature, docstring, parameters, location, and any
    detected patterns associated with the symbol.
    """
    analysis: AnalysisTools = ctx.request_context.lifespan_context.analysis
    return analysis.get_symbol_details(symbol_name, repo_id)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Get Repository Summary",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def get_repo_summary(
    repo_id: Annotated[int, "Repository ID"],
    ctx: Context = None
) -> dict:
    """
    Get comprehensive summary of a repository's analysis.
    
    Returns:
    - Language breakdown with line counts
    - Symbol counts by type
    - Top detected patterns
    - Most used imports/dependencies
    - Key classes and their methods
    """
    analysis: AnalysisTools = ctx.request_context.lifespan_context.analysis
    return analysis.get_repo_summary(repo_id)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Get Public API",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def get_public_api(
    repo_id: Annotated[int, "Repository ID"],
    include_fields: Annotated[bool, "Include struct/class field definitions"] = True,
    include_methods: Annotated[bool, "Include method definitions for classes"] = True,
    file_path: Annotated[str | None, "Optional file path to limit scope"] = None,
    ctx: Context = None
) -> dict:
    """
    Extract public API surface from a repository.
    
    Specifically designed for porting analysis: extracts only exported/public
    symbols (functions, structs, classes) with their signatures, fields, and
    method definitions.
    
    Returns:
    - functions: Exported function signatures with parameters and return types
    - types: Structs, classes, interfaces with their field definitions
    - constants: Exported constants and static values
    - header_files: Grouped by header file (for C/C++)
    - grounded_values: Exact counts that MUST be used in response
    - formatted_summary: Ready-to-include markdown summary
    
    IMPORTANT: Use formatted_summary for direct inclusion in response.
    Use grounded_values.must_quote fields verbatim. Do not hallucinate.
    """
    analysis: AnalysisTools = ctx.request_context.lifespan_context.analysis
    return analysis.get_public_api(repo_id, include_fields, include_methods, file_path)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Get API Summary",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def get_api_summary(
    repo_id: Annotated[int, "Repository ID"],
    format: Annotated[Literal["markdown", "structured"], "Output format"] = "markdown",
    include_signatures: Annotated[bool, "Include full function signatures"] = True,
    group_by: Annotated[Literal["file", "category", "flat"], "How to group functions"] = "file",
    ctx: Context = None
) -> dict:
    """
    Generate a formatted API summary for direct inclusion in AI responses.
    
    This tool produces a ready-to-use summary of the library's public API,
    specifically designed for porting analysis scenarios. The output can be
    directly copied into your response.
    
    Use this AFTER analyze_repo when you need to list all functions/types
    in the source library.
    
    Returns:
    - summary: Formatted markdown or structured data
    - grounded_values: Exact counts to use in response
    - file_breakdown: Per-file function listing
    
    Example workflow:
    1. clone_repo → get repo_id
    2. analyze_repo → parse code
    3. get_api_summary → get formatted API listing
    4. Include summary directly in your response
    """
    analysis: AnalysisTools = ctx.request_context.lifespan_context.analysis
    
    # Get public API data
    api_result = analysis.get_public_api(repo_id, include_fields=True, include_methods=True)
    
    if api_result.get("status") != "success":
        return api_result
    
    # If markdown format requested, return the pre-formatted summary
    if format == "markdown":
        return {
            "status": "success",
            "format": "markdown",
            "summary": api_result.get("formatted_summary", ""),
            "grounded_values": api_result.get("grounded_values", {}),
            "usage_instruction": "Copy the 'summary' field directly into your response. Use grounded_values for exact counts."
        }
    
    # For structured format, return organized data
    header_files = api_result.get("header_files", {})
    source_files = api_result.get("source_files", {})
    
    if group_by == "file":
        file_breakdown = []
        for file_path, data in sorted({**header_files, **source_files}.items()):
            from pathlib import Path
            file_info = {
                "file": Path(file_path).name,
                "path": file_path,
                "is_header": file_path in header_files,
                "functions": [],
                "types": [],
                "constants": []
            }
            
            for func in data.get("functions", []):
                func_entry = {"name": func["name"]}
                if include_signatures:
                    func_entry["signature"] = func.get("signature", func["name"])
                func_entry["parameters"] = func.get("parameters", [])
                func_entry["return_type"] = func.get("return_type")
                file_info["functions"].append(func_entry)
            
            for t in data.get("types", []):
                file_info["types"].append({
                    "name": t["name"],
                    "kind": t.get("kind", "type"),
                    "fields": t.get("fields", [])
                })
            
            for const in data.get("constants", []):
                file_info["constants"].append({"name": const["name"]})
            
            file_breakdown.append(file_info)
        
        return {
            "status": "success",
            "format": "structured",
            "file_breakdown": file_breakdown,
            "grounded_values": api_result.get("grounded_values", {}),
            "statistics": api_result.get("statistics", {}),
            "usage_instruction": "Use file_breakdown to list functions. Use grounded_values for exact counts."
        }
    
    elif group_by == "flat":
        # Flat list of all functions
        all_functions = []
        for func in api_result.get("public_api", {}).get("functions", []):
            func_entry = {"name": func["name"], "file": func.get("file", "")}
            if include_signatures:
                func_entry["signature"] = func.get("signature", func["name"])
            all_functions.append(func_entry)
        
        return {
            "status": "success",
            "format": "flat",
            "functions": all_functions,
            "types": api_result.get("public_api", {}).get("types", []),
            "constants": api_result.get("public_api", {}).get("constants", []),
            "grounded_values": api_result.get("grounded_values", {}),
            "usage_instruction": "Use functions list directly. Each name is from actual source code."
        }
    
    else:  # category grouping - group by likely purpose
        categories = {
            "math": [],
            "string": [],
            "io": [],
            "memory": [],
            "other": []
        }
        
        for func in api_result.get("public_api", {}).get("functions", []):
            name_lower = func["name"].lower()
            if any(kw in name_lower for kw in ["log", "exp", "pow", "sin", "cos", "tan", "sqrt", "abs", "floor", "ceil", "round", "fast"]):
                categories["math"].append(func)
            elif any(kw in name_lower for kw in ["str", "char", "print", "format", "parse"]):
                categories["string"].append(func)
            elif any(kw in name_lower for kw in ["read", "write", "open", "close", "file", "stream"]):
                categories["io"].append(func)
            elif any(kw in name_lower for kw in ["alloc", "malloc", "free", "mem", "buffer"]):
                categories["memory"].append(func)
            else:
                categories["other"].append(func)
        
        # Remove empty categories
        categories = {k: v for k, v in categories.items() if v}
        
        return {
            "status": "success",
            "format": "categorized",
            "categories": {
                cat: [{"name": f["name"], "signature": f.get("signature", f["name"])} for f in funcs]
                for cat, funcs in categories.items()
            },
            "grounded_values": api_result.get("grounded_values", {}),
            "usage_instruction": "Functions are categorized by likely purpose. Use exact names from categories."
        }


# ============================================================================
# Search Tools
# ============================================================================

@mcp.tool(
    annotations=ToolAnnotations(
        title="Search Code",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def search_code(
    query: Annotated[str, "Search query (supports: AND, OR, NOT, 'phrase', prefix*)"],
    search_type: Annotated[Literal["all", "function", "class", "method"], "Filter by symbol type"] = "all",
    repo_id: Annotated[int | None, "Repository ID to limit search"] = None,
    limit: Annotated[int, "Maximum results to return"] = 20,
    ctx: Context = None
) -> dict:
    """
    Search symbols using full-text search.
    
    Searches across function/class/method names, signatures, and docstrings.
    Use this to find specific functionality in the codebase.
    """
    search: SearchTools = ctx.request_context.lifespan_context.search
    return search.search_code(query, search_type, repo_id, limit)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Find Patterns",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def find_patterns(
    pattern_type: Annotated[Literal["algorithm", "design_pattern", "all"], "Type of pattern to find"] = "all",
    pattern_name: Annotated[str | None, "Specific pattern name (e.g., 'recursion', 'singleton')"] = None,
    repo_id: Annotated[int | None, "Repository ID to limit search"] = None,
    min_confidence: Annotated[float, "Minimum confidence threshold (0.0-1.0)"] = 0.5,
    ctx: Context = None
) -> dict:
    """
    Find detected algorithm and design patterns.
    
    Patterns include:
    - Algorithms: recursion, dynamic_programming, binary_search, graph_traversal, etc.
    - Design patterns: singleton, factory, decorator, iterator, context_manager
    
    Returns pattern locations with confidence scores and evidence.
    """
    search: SearchTools = ctx.request_context.lifespan_context.search
    return search.find_patterns(pattern_type, pattern_name, repo_id, min_confidence)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Find Imports",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def find_imports(
    module: Annotated[str | None, "Module name to search for (partial match)"] = None,
    repo_id: Annotated[int | None, "Repository ID to limit search"] = None,
    include_relative: Annotated[bool, "Include relative imports"] = False,
    limit: Annotated[int, "Maximum results to return"] = 50,
    ctx: Context = None
) -> dict:
    """
    Find import statements across the codebase.
    
    Useful for understanding dependencies and how modules are used.
    Returns import locations and a summary of most-used modules.
    """
    search: SearchTools = ctx.request_context.lifespan_context.search
    return search.find_imports(module, repo_id, include_relative, limit)


@mcp.tool(
    annotations=ToolAnnotations(
        title="List Symbols",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def list_symbols(
    repo_id: Annotated[int, "Repository ID"],
    symbol_type: Annotated[Literal["function", "class", "method", "all"], "Filter by symbol type"] = "all",
    file_path: Annotated[str | None, "Filter by specific file path"] = None,
    visibility: Annotated[Literal["public", "private", "all"], "Filter by visibility (public/private/all)"] = "all",
    limit: Annotated[int, "Maximum results to return"] = 100,
    group_by_file: Annotated[bool, "Group results by file path for easier reading"] = False,
    ctx: Context = None
) -> dict:
    """
    List all symbols in a repository.
    
    Returns a comprehensive list of functions, classes, and methods
    with their signatures, locations, and visibility status.
    
    Use visibility='public' to filter for exported/public API only.
    Use group_by_file=True to get results organized by file for porting analysis.
    """
    search: SearchTools = ctx.request_context.lifespan_context.search
    return search.list_symbols(repo_id, symbol_type, file_path, visibility, limit, group_by_file)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Inspect Symbol",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def inspect_symbol(
    repo_id: Annotated[int, "Repository ID"],
    symbol_name: Annotated[str, "Name of the symbol to inspect"],
    include_source: Annotated[bool, "Include actual source code snippet"] = True,
    context_lines: Annotated[int, "Extra lines of context around symbol (0-10)"] = 0,
    ctx: Context = None
) -> dict:
    """
    Get detailed information about a specific symbol including source code.
    
    This tool provides complete symbol details with the actual source code
    for accurate analysis. Use this when you need to see implementation
    details, not just signatures.
    
    Returns:
    - Full signature, parameters, return type
    - Docstring and documentation
    - Actual source code (when include_source=True)
    - Child symbols (methods for classes)
    - Associated patterns
    
    IMPORTANT: Use the source_code field verbatim when discussing implementation.
    """
    search: SearchTools = ctx.request_context.lifespan_context.search
    return search.inspect_symbol(repo_id, symbol_name, include_source, context_lines)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Read File",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def read_file(
    repo_id: Annotated[int, "Repository ID"],
    file_path: Annotated[str, "Relative path within repository (e.g., 'src/main.py')"],
    start_line: Annotated[int | None, "Start line number (1-indexed, inclusive)"] = None,
    end_line: Annotated[int | None, "End line number (1-indexed, inclusive)"] = None,
    ctx: Context = None
) -> dict:
    """
    Read file content from a cloned repository.
    
    Provides DIRECT ACCESS to source files in analyzed repositories.
    Use this instead of fetching from external URLs - the code is already
    available locally after clone_repo.
    
    Features:
    - Read entire file or specific line ranges
    - Automatic language detection
    - Security: path traversal prevention, binary file rejection
    
    Limits:
    - Maximum 1000 lines per request (use line ranges for larger files)
    - Text files only (binary files rejected)
    - 10MB file size limit
    
    Example uses:
    - View implementation details not captured by inspect_symbol
    - Read configuration files, READMEs, documentation
    - Examine specific sections of large files
    
    Returns:
    - content: The file text
    - line_count: Total lines in file
    - language: Detected programming language
    - truncated: Whether content was truncated due to limits
    """
    search: SearchTools = ctx.request_context.lifespan_context.search
    return search.read_repo_file(repo_id, file_path, start_line, end_line)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Search In Files",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def search_in_files(
    repo_id: Annotated[int, "Repository ID"],
    query: Annotated[str, "Search string or regex pattern"],
    is_regex: Annotated[bool, "Treat query as regular expression"] = False,
    file_pattern: Annotated[str | None, "Glob pattern to filter files (e.g., '*.py', 'src/**/*.js')"] = None,
    max_results: Annotated[int, "Maximum matches to return"] = 50,
    context_lines: Annotated[int, "Lines of context before/after each match"] = 2,
    ctx: Context = None
) -> dict:
    """
    Search for text content in repository files (grep-like).
    
    Unlike search_code which searches indexed symbols, this tool searches
    actual file content. Use it to find:
    - String literals and comments
    - Configuration values
    - Patterns not captured by code analysis
    - Content in non-code files (READMEs, configs)
    
    Features:
    - Literal string or regex search
    - File pattern filtering (glob)
    - Context lines around matches
    - Skips binary files and common ignore directories
    
    Returns matches with:
    - File path and line number
    - Matching line content
    - Context lines before/after
    """
    search: SearchTools = ctx.request_context.lifespan_context.search
    return search.search_file_content(repo_id, query, is_regex, file_pattern, max_results, context_lines)


# ============================================================================
# Call Graph Tools
# ============================================================================

@mcp.tool(
    annotations=ToolAnnotations(
        title="Get Call Graph",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def get_call_graph(
    repo_id: Annotated[int, "Repository ID"],
    symbol_name: Annotated[str | None, "Focus on specific function/method (shows calls to/from it)"] = None,
    depth: Annotated[int, "Maximum traversal depth from target symbol"] = 3,
    direction: Annotated[Literal["callers", "callees", "both"], "Direction to traverse"] = "both",
    output_format: Annotated[Literal["json", "mermaid"], "Output format"] = "json",
    ctx: Context = None
) -> dict:
    """
    Get function call graph for a repository.
    
    Shows which functions call which other functions.
    Can focus on a specific symbol to see its callers and/or callees.
    
    Requires: Run analyze_repo with include_call_graph=True first.
    
    Output formats:
    - json: Structured data with nodes and edges
    - mermaid: Flowchart diagram for visualization
    """
    analysis: AnalysisTools = ctx.request_context.lifespan_context.analysis
    return analysis.get_call_graph(repo_id, symbol_name, depth, direction, output_format)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Find Callers",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def find_callers(
    symbol_name: Annotated[str, "Name of the function or method to find callers of"],
    repo_id: Annotated[int | None, "Repository ID to limit search"] = None,
    ctx: Context = None
) -> dict:
    """
    Find all callers of a specific function or method.
    
    Returns a list of all places where this function is called,
    with file paths and line numbers.
    
    Requires: Run analyze_repo with include_call_graph=True first.
    """
    analysis: AnalysisTools = ctx.request_context.lifespan_context.analysis
    return analysis.find_callers(symbol_name, repo_id)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Find Callees",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def find_callees(
    symbol_name: Annotated[str, "Name of the function or method"],
    repo_id: Annotated[int, "Repository ID"],
    ctx: Context = None
) -> dict:
    """
    Find all functions called by a specific function or method.
    
    Returns a list of all function calls made within this function,
    with line numbers and whether they are external/resolved.
    
    Requires: Run analyze_repo with include_call_graph=True first.
    """
    analysis: AnalysisTools = ctx.request_context.lifespan_context.analysis
    return analysis.find_callees(symbol_name, repo_id)


# ============================================================================
# Report Generation Tools
# ============================================================================

@mcp.tool(
    annotations=ToolAnnotations(
        title="Generate Report",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def generate_report(
    repo_id: Annotated[int, "Repository ID"],
    report_type: Annotated[
        Literal["summary", "detailed", "dependencies", "architecture", "porting_analysis"],
        "Type of report: summary (overview), detailed (all data), dependencies (imports), architecture (classes + call graph), porting_analysis (for migration planning)"
    ] = "summary",
    output_format: Annotated[
        Literal["json", "markdown", "html"],
        "Output format for the report"
    ] = "markdown",
    save_path: Annotated[str | None, "Optional file path to save the report (adds extension automatically)"] = None,
    ctx: Context = None
) -> dict:
    """
    Generate an analysis report for a repository.
    
    Report types:
    - summary: High-level overview with key statistics, top patterns, key classes
    - detailed: Full analysis with all symbols, patterns, imports, and call graph
    - dependencies: Focus on external/internal dependencies and import analysis
    - architecture: Class hierarchy, file distribution, and Mermaid call graph
    - porting_analysis: File-by-file symbol listing with exact counts for migration planning
    
    Output formats:
    - json: Structured data for programmatic use
    - markdown: Human-readable with tables and formatting
    - html: Styled HTML with Mermaid diagram support
    
    If save_path is provided, the report is saved to that location.
    
    Response Integration (for porting_analysis):
        Use files_analysis[].symbols[] verbatim in your response.
        Use statistics.* for exact counts - NEVER estimate.
    """
    report: ReportTools = ctx.request_context.lifespan_context.report
    return report.generate_report(repo_id, report_type, output_format, save_path)


# ============================================================================
# Algorithm Analysis Tools
# ============================================================================

@mcp.tool(
    annotations=ToolAnnotations(
        title="Extract Algorithms",
        readOnlyHint=False,
        idempotentHint=True
    )
)
async def extract_algorithms(
    repo_id: Annotated[int, "Repository ID to extract algorithms from"],
    min_lines: Annotated[int, "Minimum line count for extraction (default: 5)"] = 5,
    force_reextract: Annotated[bool, "Re-extract even if already exists"] = False,
    ctx: Context = None
) -> dict:
    """
    Extract and analyze all algorithms from a repository.
    
    Analyzes functions and methods to compute:
    - Complexity metrics (cyclomatic, nesting depth, loops, conditionals)
    - AST-based structural hash for duplicate detection
    - Static category classification (sorting, searching, graph, dp, math, etc.)
    
    Requires: Run analyze_repo first to populate symbols.
    """
    algorithm: AlgorithmTools = ctx.request_context.lifespan_context.algorithm
    
    await ctx.info(f"Extracting algorithms from repository {repo_id}...")
    result = algorithm.extract_algorithms(repo_id, min_lines, force_reextract)
    
    if result.get("status") == "success":
        stats = result.get("statistics", {})
        await ctx.info(f"Extracted {stats.get('extracted', 0)} algorithms")
    
    return result


@mcp.tool(
    annotations=ToolAnnotations(
        title="Get LLM Analysis Prompt",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def get_llm_analysis_prompt(
    algorithm_id: Annotated[int, "Algorithm ID to get prompt for"],
    ctx: Context = None
) -> dict:
    """
    Get the standard LLM analysis prompt for an algorithm.
    
    Returns a structured prompt with the algorithm's source code.
    The client should:
    1. Call their LLM with the returned 'prompt' field
    2. Parse the LLM's JSON response
    3. Save the result using save_llm_analysis
    
    The prompt asks for: purpose, category, time/space complexity,
    use cases, and potential improvements.
    """
    algorithm: AlgorithmTools = ctx.request_context.lifespan_context.algorithm
    return algorithm.get_llm_analysis_prompt(algorithm_id)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Save LLM Analysis",
        readOnlyHint=False,
        idempotentHint=True
    )
)
def save_llm_analysis(
    algorithm_id: Annotated[int, "Algorithm ID to save analysis for"],
    analysis: Annotated[str, "LLM analysis result as JSON string with: purpose, category, time_complexity, space_complexity, use_cases, improvements"],
    ctx: Context = None
) -> dict:
    """
    Save LLM analysis results for an algorithm.
    
    Expected JSON structure:
    {
        "purpose": "Description of what the algorithm does",
        "category": "sorting|searching|graph|dp|math|string|tree|io|other",
        "time_complexity": {"notation": "O(...)", "explanation": "..."},
        "space_complexity": {"notation": "O(...)", "explanation": "..."},
        "use_cases": ["case1", "case2"],
        "improvements": ["improvement1", "improvement2"]
    }
    """
    algorithm: AlgorithmTools = ctx.request_context.lifespan_context.algorithm
    return algorithm.save_llm_analysis(algorithm_id, analysis)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Save Algorithm Embedding",
        readOnlyHint=False,
        idempotentHint=True
    )
)
def save_algorithm_embedding(
    algorithm_id: Annotated[int, "Algorithm ID to save embedding for"],
    embedding: Annotated[list[float], "Embedding vector as list of floats"],
    model_name: Annotated[str, "Name of the embedding model used (e.g., 'text-embedding-3-small')"],
    ctx: Context = None
) -> dict:
    """
    Save an embedding vector for an algorithm.
    
    The client should generate the embedding using their preferred model
    (e.g., OpenAI text-embedding-3-small, Cohere embed-v3, etc.) and
    provide it here for similarity search.
    """
    algorithm: AlgorithmTools = ctx.request_context.lifespan_context.algorithm
    return algorithm.save_embedding(algorithm_id, embedding, model_name)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Find Similar Algorithms",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def find_similar_algorithms(
    algorithm_id: Annotated[int, "Algorithm ID to find similar algorithms for"],
    method: Annotated[Literal["hash", "embedding", "both"], "Comparison method"] = "both",
    threshold: Annotated[float, "Similarity threshold for embedding search (0.0-1.0)"] = 0.8,
    limit: Annotated[int, "Maximum results"] = 20,
    ctx: Context = None
) -> dict:
    """
    Find algorithms similar to the specified algorithm.
    
    Methods:
    - hash: Find structurally identical algorithms (exact AST match)
    - embedding: Find semantically similar algorithms using embeddings
    - both: Combine hash and embedding results
    
    Requires: Embeddings must be saved first for embedding-based search.
    """
    algorithm: AlgorithmTools = ctx.request_context.lifespan_context.algorithm
    return algorithm.find_similar(algorithm_id, method, threshold, limit)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Get Algorithm",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def get_algorithm(
    algorithm_id: Annotated[int, "Algorithm ID to retrieve"],
    ctx: Context = None
) -> dict:
    """
    Get detailed information about an algorithm.
    
    Returns complete algorithm details including:
    - Source code (original and normalized)
    - Complexity metrics
    - Static and LLM categories
    - LLM analysis results (if available)
    - Embedding status
    """
    algorithm: AlgorithmTools = ctx.request_context.lifespan_context.algorithm
    return algorithm.get_algorithm(algorithm_id)


@mcp.tool(
    annotations=ToolAnnotations(
        title="List Algorithms",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def list_algorithms(
    repo_id: Annotated[int, "Repository ID"],
    category: Annotated[str | None, "Filter by category (sorting, searching, graph, dp, math, string, tree, io, other)"] = None,
    category_type: Annotated[Literal["static", "llm", "any"], "Which category to filter by"] = "static",
    min_complexity: Annotated[int | None, "Minimum cyclomatic complexity"] = None,
    limit: Annotated[int, "Maximum results"] = 100,
    ctx: Context = None
) -> dict:
    """
    List algorithms in a repository with optional filters.
    
    Filters:
    - category: Filter by algorithm category
    - category_type: Use 'static' (auto-detected), 'llm' (LLM-determined), or 'any'
    - min_complexity: Filter by minimum cyclomatic complexity
    
    Returns algorithm list with category summary.
    """
    algorithm: AlgorithmTools = ctx.request_context.lifespan_context.algorithm
    return algorithm.list_algorithms(repo_id, category, category_type, min_complexity, limit)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Search Algorithms",
        readOnlyHint=True,
        idempotentHint=True
    )
)
def search_algorithms(
    query: Annotated[str, "Search query (supports FTS5 operators: AND, OR, NOT, 'phrase', prefix*)"],
    repo_id: Annotated[int | None, "Optional repository ID filter"] = None,
    limit: Annotated[int, "Maximum results"] = 20,
    ctx: Context = None
) -> dict:
    """
    Search algorithms using full-text search.
    
    Searches in source code and LLM analysis.
    Use this to find algorithms by keywords, patterns, or descriptions.
    """
    algorithm: AlgorithmTools = ctx.request_context.lifespan_context.algorithm
    return algorithm.search_algorithms(query, repo_id, limit)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Build Similarity Index",
        readOnlyHint=False,
        idempotentHint=True
    )
)
def build_similarity_index(
    repo_id: Annotated[int | None, "Optional repository ID to limit index (None for all repos)"] = None,
    index_type: Annotated[Literal["flat", "ivf", "hnsw"], "Index type: flat (exact), ivf (fast), hnsw (best quality/speed)"] = "flat",
    ctx: Context = None
) -> dict:
    """
    Build ANN index for fast embedding similarity search.
    
    This significantly improves performance for large datasets (>1000 embeddings).
    Must be called before using find_similar_algorithms with embedding method.
    
    Index types:
    - flat: Exact search, slower but most accurate (recommended for <10K embeddings)
    - ivf: Inverted file index, faster approximate search (good for 10K-1M embeddings)
    - hnsw: Hierarchical NSW graph, best quality/speed tradeoff (recommended for >100K)
    
    The index is kept in memory and should be rebuilt after adding new embeddings.
    
    Requires: FAISS library (pip install faiss-cpu numpy)
    """
    algorithm: AlgorithmTools = ctx.request_context.lifespan_context.algorithm
    return algorithm.build_similarity_index(repo_id, index_type)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Reduce Embedding Dimensions",
        readOnlyHint=False,
        destructiveHint=True,
        idempotentHint=False
    )
)
def reduce_embedding_dimensions(
    target_dimension: Annotated[int, "Target dimension (must be < current dimension)"],
    repo_id: Annotated[int | None, "Optional repository ID to limit reduction (None for all repos)"] = None,
    method: Annotated[Literal["pca"], "Reduction method (currently only PCA supported)"] = "pca",
    ctx: Context = None
) -> dict:
    """
    Reduce embedding dimensions for storage/performance optimization.
    
    Uses PCA to reduce dimensionality while preserving maximum variance.
    Benefits:
    - Reduces storage size (e.g., 768 -> 128 dimensions = 83% reduction)
    - Improves search speed
    - Can reduce noise in embeddings
    
    Warning: This modifies embeddings in the database. Consider backing up first.
    The operation cannot be reversed without regenerating embeddings.
    
    Returns variance retention statistics to help assess quality loss.
    
    Requires: scikit-learn library (pip install scikit-learn)
    """
    algorithm: AlgorithmTools = ctx.request_context.lifespan_context.algorithm
    return algorithm.reduce_embedding_dimensions(repo_id, target_dimension, method)


# ============================================================================
# Resources
# ============================================================================

@mcp.resource("repo://{repo_id}/summary")
def get_repo_summary_resource(repo_id: int, ctx: Context = None) -> str:
    """Get repository analysis summary as a resource."""
    analysis: AnalysisTools = ctx.request_context.lifespan_context.analysis
    result = analysis.get_repo_summary(int(repo_id))
    
    if result.get("status") != "success":
        return f"Error: {result.get('message', 'Unknown error')}"
    
    # Format as readable text
    repo = result.get("repository", {})
    lines = [
        f"# Repository: {repo.get('name', 'Unknown')}",
        f"URL: {repo.get('url', 'N/A')}",
        f"Last analyzed: {repo.get('last_analyzed', 'Never')}",
        "",
        "## Language Breakdown",
    ]
    
    for lang in result.get("languages", []):
        lines.append(f"- {lang['language']}: {lang['file_count']} files, {lang['total_lines']} lines")
    
    lines.extend(["", "## Symbol Counts"])
    for stype, count in result.get("symbol_counts", {}).items():
        lines.append(f"- {stype}: {count}")
    
    lines.extend(["", "## Top Patterns"])
    for pattern in result.get("top_patterns", []):
        lines.append(f"- {pattern['pattern_type']}/{pattern['pattern_name']}: {pattern['count']} occurrences")
    
    lines.extend(["", "## Top Dependencies"])
    for imp in result.get("top_imports", [])[:10]:
        lines.append(f"- {imp['module']}: {imp['count']} uses")
    
    return "\n".join(lines)


@mcp.resource("guidelines://tool-usage")
def get_tool_usage_guidelines() -> str:
    """
    Detailed tool usage guidelines for AI assistants.
    
    Read this resource when you need comprehensive guidance on how to
    integrate tool results into responses.
    """
    return '''
# MCP Git Analyzer - Detailed Tool Usage Guidelines

## Tool Categories & When to Use

### 1. Repository Setup Tools
| Tool | Purpose | Key Output Fields |
|------|---------|-------------------|
| `clone_repo` | Download repository | `repo_id` (use for subsequent calls) |
| `list_repos` | See available repos | `repositories[].id`, `repositories[].name` |
| `get_repo_tree` | View file structure | `tree` (nested structure) |

### 2. Analysis Tools
| Tool | Purpose | Key Output Fields |
|------|---------|-------------------|
| `analyze_repo` | Full repository parse | `statistics.total_functions`, `statistics.total_classes`, `patterns[]` |
| `get_file_analysis` | Single file details | `symbols[]` (MUST show these), `imports[]`, `patterns[]` |
| `get_repo_summary` | Quick overview | `symbol_counts`, `languages[]`, `top_patterns[]` |
| `get_public_api` | Porting analysis | `functions[]`, `types[]` - USE VERBATIM |

### 3. Search Tools  
| Tool | Purpose | Key Output Fields |
|------|---------|-------------------|
| `list_symbols` | Find functions/classes | `results[].name`, `results[].signature` |
| `find_patterns` | Detect design patterns | `results[].pattern_type`, `results[].evidence` |
| `find_imports` | Dependency analysis | `results[].module`, `results[].count` |
| `inspect_symbol` | Deep dive | `symbol.source_code` - USE VERBATIM |

### 4. Algorithm Tools
| Tool | Purpose | Key Output Fields |
|------|---------|-------------------|
| `extract_algorithms` | Parse algorithms | `statistics.categories` |
| `list_algorithms` | Browse algorithms | `algorithms[].symbol_name`, `category_summary` |
| `get_algorithm_detail` | Full details | `algorithm.source_code`, `complexity_metrics` |

### 5. Report Tools
| Tool | Purpose | Key Output Fields |
|------|---------|-------------------|
| `generate_report` | Comprehensive report | Depends on `report_type` |

---

## Field Usage Rules

### MUST Include Verbatim
These fields contain factual data that MUST appear in your response as-is:

```
analyze_repo:
  - statistics.total_files → "총 N개 파일"
  - statistics.total_functions → "N개의 함수"
  - statistics.total_classes → "N개의 클래스"

get_file_analysis:
  - symbols[].name → List each function/class name
  - symbols[].signature → Show actual signatures
  - symbols[].parameters → Detail parameters

list_algorithms:
  - algorithms[].symbol_name → List algorithm names
  - category_summary → Show category distribution

inspect_symbol:
  - symbol.source_code → Quote actual code
```

### NEVER Estimate
❌ Wrong: "약 50개의 함수", "50+ functions", "numerous functions"
✅ Correct: "47개의 함수" (from statistics.total_functions)

---

## Response Templates

### For Porting/Migration Analysis

```markdown
## 1. 원본 라이브러리 분석

### 파일별 함수 목록
[From get_file_analysis for each file]

**header1.h** (N개 함수)
- `function1(param1: type, param2: type) -> return_type`
- `function2(...)`

**header2.h** (M개 함수)  
- ...

### 통계
- 총 파일 수: [statistics.total_files]
- 총 함수 수: [statistics.total_functions]
- 총 클래스 수: [statistics.total_classes]

### 알고리즘 패턴
[From list_algorithms.category_summary]
- math: N개
- sorting: M개
- ...

## 2. 타겟 언어 설계

[Based on actual file/function mapping]

| 원본 파일 | 타겟 모듈 | 함수 수 |
|-----------|-----------|---------|
| header1.h | module1.rs | N |
| header2.h | module2.rs | M |

## 3. 마이그레이션 로드맵

[Phased plan based on actual dependencies from find_imports]
```

### For Code Review/Understanding

```markdown
## 코드 구조 분석

### 핵심 컴포넌트
[From list_symbols with type="class"]

1. **ClassName** (`file.py:L10-50`)
   - 역할: [from docstring]
   - 메서드: N개
   
### 주요 패턴
[From find_patterns]

- Pattern1: N회 발견 (files: ...)
- Pattern2: M회 발견

### 의존성
[From find_imports]
- External: package1 (N uses), package2 (M uses)
- Internal: module1 → module2
```

---

## Common Mistakes to Avoid

1. **Ignoring tool output**: You called the tool but didn\'t use the data
2. **Estimating counts**: Always use exact numbers from statistics
3. **Generic descriptions**: Use actual function names, not "various utility functions"
4. **Missing signatures**: Show `signature` field, not just `name`
5. **Skipping source code**: When discussing implementation, quote `source_code`

---

## Quick Reference: Output → Response Mapping

```
Tool Called                    → Must Include in Response
─────────────────────────────────────────────────────────
analyze_repo                   → Exact counts from statistics
get_file_analysis(file.h)      → List of symbols[].name + signature
list_symbols                   → results[].name grouped logically
find_patterns                  → Pattern names + evidence
list_algorithms                → Algorithm names + categories
extract_algorithms             → Category distribution
inspect_symbol                 → source_code in code block
generate_report("porting_analysis") → Complete structured output
get_api_summary                → Copy summary field directly
get_public_api                 → Use formatted_summary + grounded_values
```
'''.strip()


@mcp.resource("guidelines://response-structure")
def get_response_structure_guidelines() -> str:
    """
    Response structure templates for porting/migration analysis.
    
    Read this resource when creating responses for library porting tasks.
    Contains exact templates to follow for consistent, accurate responses.
    """
    return '''
# Response Structure Guidelines for Porting Analysis

## Overview
When analyzing a library for porting to another language, your response MUST follow
a specific structure and use tool output verbatim. This ensures accuracy and prevents
hallucination of APIs that don't exist.

---

## Mandatory 3-Section Structure

### Section 1: 원본 라이브러리 기능 요약 (Source Library Summary)

**Purpose**: List ALL public functions/types from the source library.

**Data Source**: 
- `get_api_summary` → Use `summary` field directly
- `get_public_api` → Use `formatted_summary` field directly

**Template**:
```markdown
## 1. 원본 라이브러리 기능 요약

### 통계
- 총 함수: **[grounded_values.total_functions]개**
- 총 타입: **[grounded_values.total_types]개**
- 헤더 파일: **[grounded_values.header_file_count]개**

### 헤더별 함수 목록

#### `header1.h` (N개 함수)
**함수:**
- `function1_signature`
- `function2_signature`
...

#### `header2.h` (M개 함수)
**함수:**
- `functionA_signature`
...
```

**Rules**:
- Copy function names and signatures EXACTLY from tool output
- Use EXACT counts from grounded_values
- Do NOT add functions that don't appear in tool output
- Do NOT estimate with "약 40개", "50+"

### Section 2: 설계/아키텍처 (Design/Architecture)

**Purpose**: Map source files to target language modules.

**Data Source**:
- `get_public_api` → `header_files` and `source_files` keys
- `find_patterns` → Design patterns to consider

**Template**:
```markdown
## 2. [Target Language] 설계

### 모듈 매핑

| 원본 파일 | 타겟 모듈 | 함수 수 |
|-----------|-----------|---------|
| header1.h | module1.rs | N |
| header2.h | module2.rs | M |

### 주요 타입

```[target_language]
// From types[] in get_public_api output
struct TypeName {
    field1: Type1,
    field2: Type2,
}
```

### 고려사항
- [From find_patterns results]
```

### Section 3: 마이그레이션 로드맵 (Migration Roadmap)

**Purpose**: Phased implementation plan with specific function names.

**Template**:
```markdown
## 3. 마이그레이션 로드맵

### Phase 1: 핵심 기능 (Core)
- [ ] `function1` - [brief description]
- [ ] `function2` - [brief description]
- [ ] 테스트: 원본 대비 정확도 검증

### Phase 2: 확장 기능 (Extended)
- [ ] `function3`
- [ ] `function4`
- [ ] 문서화

### Phase 3: 최적화 (Optimization)
- [ ] SIMD 버전 (if applicable)
- [ ] 벤치마크
- [ ] 배포
```

---

## grounded_values Usage Rules

### What is grounded_values?
A field in tool output containing verified counts and field paths.

### Structure Example:
```json
"grounded_values": {
    "total_functions": 44,
    "total_types": 8,
    "must_quote": ["functions[*].name", "functions[*].signature"],
    "warning": "이 값들은 도구 결과에서 직접 추출됨..."
}
```

### Rules:
1. **Use exact numbers**: `grounded_values.total_functions` → "44개 함수" (not "약 40개")
2. **Quote must_quote fields**: List actual function names from `functions[*].name`
3. **Never invent data**: If grounded_values doesn't have a count, don't guess

---

## Common Mistakes

### ❌ Wrong:
- "약 50개의 함수가 있습니다" (estimating)
- "다양한 수학 함수들이 포함되어 있습니다" (vague)
- Listing functions not in tool output (hallucinating)
- "fast/faster 버전이 각각 있어 정밀도 4자리/2자리" (unverified precision claims)

### ✅ Correct:
- "44개의 함수가 있습니다" (from grounded_values)
- "fastlog2f, fastlogf, fasterlog2f, fasterlogf" (actual names from output)
- "정확도는 원본 구현과 동일하며 테스트 필요" (if precision not in data)

---

## Quick Workflow

1. `clone_repo` → Get repo_id
2. `analyze_repo` → Parse code
3. `get_api_summary(format="markdown")` → Get formatted API summary
4. Copy `summary` field directly into Section 1
5. Use `grounded_values` for all counts
6. Map files to target modules for Section 2
7. List specific function names for Section 3 phases

---

## Test File Analysis

When original repo has tests, mention them:

**Data Source**: `generate_report("api_summary")` → `test_analysis` field

**Template**:
```markdown
### 테스트 전략

원본 테스트 파일: [test_analysis.count]개 ([test_analysis.total_lines] lines)
- `test_file1.c`
- `test_file2.c`

Rust 테스트 전략:
- 원본 테스트 케이스 기반 property-based test
- 표준 라이브러리 대비 상대 오차 검증
```
'''.strip()


# ============================================================================
# Prompts (Templates for AI assistants)
# ============================================================================

@mcp.prompt()
def porting_plan(
    source_repo: str,
    target_language: str,
    analysis_results: str
) -> str:
    """
    Generate a structured porting plan from analysis results.
    
    Use this prompt template after analyzing a repository to ensure
    the response includes all required sections with actual data.
    
    Args:
        source_repo: Name of the source repository
        target_language: Target programming language (e.g., "Rust", "Go")
        analysis_results: JSON string from analyze_repo or generate_report
    """
    return f'''
Based on the analysis of **{source_repo}**, create a porting plan to **{target_language}**.

## Analysis Data (USE THIS DATA VERBATIM)
```json
{analysis_results}
```

## Required Response Structure

### 1. 원본 라이브러리 기능 요약 (Source Library Summary)
- List ALL functions from the analysis data above
- Show exact function signatures
- Group by file/module
- Include exact counts (do NOT estimate)

### 2. {target_language} 크레이트/패키지 설계
- Map each source file to target module
- Define public API based on actual functions
- Note any patterns detected

### 3. 마이그레이션 로드맵
- Phase 1: Core functionality (list specific functions)
- Phase 2: Extended features
- Phase 3: Optimization & testing

### Rules
- Every function name must come from the analysis data
- Every count must be exact from statistics
- Do not add functions that don\'t exist in the source
'''


# ============================================================================
# Entry Point
# ============================================================================

def main():
    """Run the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
