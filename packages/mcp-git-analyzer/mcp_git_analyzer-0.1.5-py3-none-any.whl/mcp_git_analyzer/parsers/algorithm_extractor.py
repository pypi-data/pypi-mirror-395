"""Algorithm extraction and analysis module.

Extracts algorithm source code, computes complexity metrics,
generates AST-based structural hashes, and performs static classification.
Supports Python, JavaScript, and TypeScript.
"""

import hashlib
import re
from dataclasses import dataclass, asdict

import tree_sitter_python as tspython
import tree_sitter_javascript as tsjavascript
import tree_sitter_typescript as tstypescript
from tree_sitter import Language, Parser, Node


# Initialize language parsers
LANGUAGES = {
    "python": Language(tspython.language()),
    "javascript": Language(tsjavascript.language()),
    "typescript": Language(tstypescript.language_tsx()),
}

# Create parsers for each language
_parsers: dict[str, Parser] = {}
for lang_name, lang in LANGUAGES.items():
    _parsers[lang_name] = Parser(lang)


# Node type mappings for different languages
FUNCTION_NODES = {
    "python": ["function_definition"],
    "javascript": ["function_declaration", "arrow_function", "function_expression", "method_definition"],
    "typescript": ["function_declaration", "arrow_function", "function_expression", "method_definition"],
}

LOOP_NODES = {
    "python": ["for_statement", "while_statement"],
    "javascript": ["for_statement", "for_in_statement", "for_of_statement", "while_statement", "do_statement"],
    "typescript": ["for_statement", "for_in_statement", "for_of_statement", "while_statement", "do_statement"],
}

CONDITIONAL_NODES = {
    "python": ["if_statement", "elif_clause", "conditional_expression"],
    "javascript": ["if_statement", "ternary_expression", "switch_statement"],
    "typescript": ["if_statement", "ternary_expression", "switch_statement"],
}

NESTING_NODES = {
    "python": ["if_statement", "for_statement", "while_statement", "try_statement", "with_statement", "match_statement"],
    "javascript": ["if_statement", "for_statement", "for_in_statement", "for_of_statement", "while_statement", "do_statement", "try_statement", "switch_statement"],
    "typescript": ["if_statement", "for_statement", "for_in_statement", "for_of_statement", "while_statement", "do_statement", "try_statement", "switch_statement"],
}

COMMENT_NODES = {
    "python": ["comment"],
    "javascript": ["comment"],
    "typescript": ["comment"],
}

DOCSTRING_PATTERNS = {
    "python": {"node_type": "expression_statement", "child_type": "string"},
    "javascript": {"node_type": "comment", "pattern": r"^/\*\*"},
    "typescript": {"node_type": "comment", "pattern": r"^/\*\*"},
}


# Static category definitions based on code patterns
STATIC_CATEGORIES = {
    "sorting": {
        "keywords": ["sort", "swap", "pivot", "partition", "merge", "heap", "bubble", "insertion", "selection", "quick"],
        "patterns": [r"\.sort\(", r"sorted\(", r"swap.*\[", r"pivot"],
    },
    "searching": {
        "keywords": ["search", "find", "lookup", "binary", "linear", "index", "locate"],
        "patterns": [r"while.*low.*high", r"mid\s*=", r"bisect"],
    },
    "graph": {
        "keywords": ["graph", "node", "edge", "vertex", "bfs", "dfs", "dijkstra", "path", "traverse", "neighbor"],
        "patterns": [r"visited", r"queue.*append", r"stack.*append", r"adjacen"],
    },
    "dp": {
        "keywords": ["dp", "memo", "cache", "tabulation", "subproblem", "optimal"],
        "patterns": [r"@cache", r"@lru_cache", r"memo\[", r"dp\["],
    },
    "math": {
        "keywords": ["factorial", "fibonacci", "prime", "gcd", "lcm", "power", "sqrt", "matrix", "vector", "sum", "product"],
        "patterns": [r"math\.", r"numpy", r"\*\*", r"//", r"%"],
    },
    "string": {
        "keywords": ["string", "substr", "pattern", "match", "parse", "regex", "split", "join", "replace"],
        "patterns": [r"re\.", r"\.split\(", r"\.join\(", r"\.replace\("],
    },
    "tree": {
        "keywords": ["tree", "node", "leaf", "root", "child", "parent", "binary", "bst", "avl", "heap"],
        "patterns": [r"\.left", r"\.right", r"\.children", r"\.parent"],
    },
    "io": {
        "keywords": ["read", "write", "file", "open", "close", "stream", "buffer", "parse", "serialize"],
        "patterns": [r"open\(", r"\.read\(", r"\.write\(", r"json\.", r"pickle\."],
    },
}


@dataclass
class ComplexityMetrics:
    """Complexity metrics for an algorithm."""
    cyclomatic: int = 1  # Cyclomatic complexity (starts at 1)
    nesting_depth: int = 0  # Maximum nesting depth
    loops: int = 0  # Number of loop constructs
    conditionals: int = 0  # Number of conditional branches
    lines: int = 0  # Number of code lines (non-empty, non-comment)
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AlgorithmInfo:
    """Extracted algorithm information."""
    symbol_name: str
    symbol_type: str  # 'function' or 'method'
    parent_name: str | None
    source_code: str
    normalized_code: str
    ast_hash: str
    complexity_metrics: ComplexityMetrics
    static_category: str
    start_line: int
    end_line: int
    
    def to_dict(self) -> dict:
        d = asdict(self)
        d["complexity_metrics"] = self.complexity_metrics.to_dict()
        return d


class AlgorithmExtractor:
    """Extract and analyze algorithms from source code (Python, JavaScript, TypeScript)."""
    
    def __init__(self, language: str = "python"):
        """
        Initialize the extractor for a specific language.
        
        Args:
            language: One of 'python', 'javascript', 'typescript'
        """
        if language not in LANGUAGES:
            raise ValueError(f"Unsupported language: {language}. Supported: {list(LANGUAGES.keys())}")
        
        self.language = language
        self.parser = _parsers[language]
    
    @classmethod
    def for_language(cls, language: str) -> "AlgorithmExtractor":
        """Factory method to create extractor for a specific language."""
        return cls(language)
    
    def extract_algorithm(
        self, 
        source: str, 
        start_line: int, 
        end_line: int,
        symbol_name: str,
        symbol_type: str,
        parent_name: str | None = None
    ) -> AlgorithmInfo:
        """
        Extract algorithm information from a symbol's source code.
        
        Args:
            source: Full source code of the file
            start_line: Start line of the symbol (1-indexed)
            end_line: End line of the symbol (1-indexed)
            symbol_name: Name of the function/method
            symbol_type: 'function' or 'method'
            parent_name: Parent class name if method
        
        Returns:
            AlgorithmInfo with all extracted data
        """
        # Extract source code for the symbol
        lines = source.split("\n")
        func_source = "\n".join(lines[start_line - 1:end_line])
        
        # Normalize the code
        normalized = self._normalize_code(func_source)
        
        # Compute AST hash
        ast_hash = self._compute_ast_hash(func_source)
        
        # Compute complexity metrics
        metrics = self._compute_complexity(func_source)
        
        # Determine static category
        static_category = self._classify_static(func_source, symbol_name, metrics)
        
        return AlgorithmInfo(
            symbol_name=symbol_name,
            symbol_type=symbol_type,
            parent_name=parent_name,
            source_code=func_source,
            normalized_code=normalized,
            ast_hash=ast_hash,
            complexity_metrics=metrics,
            static_category=static_category,
            start_line=start_line,
            end_line=end_line
        )
    
    def _normalize_code(self, source: str) -> str:
        """
        Normalize code by removing comments, docstrings, and standardizing whitespace.
        
        Args:
            source: Original source code
        
        Returns:
            Normalized source code
        """
        # Parse the source
        tree = self.parser.parse(bytes(source, "utf-8"))
        
        # Collect ranges to remove (comments, strings that are docstrings)
        remove_ranges: list[tuple[int, int]] = []
        comment_nodes = COMMENT_NODES.get(self.language, ["comment"])
        DOCSTRING_PATTERNS.get(self.language, {})
        
        def collect_removable(node: Node, is_first_stmt: bool = False):
            # Remove comments
            if node.type in comment_nodes:
                remove_ranges.append((node.start_byte, node.end_byte))
            
            # Handle language-specific docstrings
            if self.language == "python":
                if node.type == "expression_statement" and is_first_stmt:
                    # Check if it's a docstring (string as first statement)
                    for child in node.children:
                        if child.type == "string":
                            remove_ranges.append((node.start_byte, node.end_byte))
                            break
            elif self.language in ("javascript", "typescript"):
                # JSDoc comments are already caught as comments
                pass
            
            # Check for docstrings in function/class bodies
            body_types = {
                "python": "block",
                "javascript": "statement_block",
                "typescript": "statement_block",
            }
            body_type = body_types.get(self.language, "block")
            
            if node.type == body_type:
                for i, child in enumerate(node.children):
                    collect_removable(child, is_first_stmt=(i == 0))
            else:
                for child in node.children:
                    collect_removable(child, False)
        
        collect_removable(tree.root_node)
        
        # Remove collected ranges (in reverse order to preserve indices)
        result = source
        for start, end in sorted(remove_ranges, reverse=True):
            result = result[:start] + result[end:]
        
        # Normalize whitespace
        lines = [line.strip() for line in result.split("\n") if line.strip()]
        return "\n".join(lines)
    
    def _compute_ast_hash(self, source: str) -> str:
        """
        Compute a structural hash of the AST, ignoring variable names and literals.
        
        This allows detection of structurally similar algorithms even if they
        use different variable names or literal values.
        
        Args:
            source: Source code
        
        Returns:
            Hex digest of the structural hash
        """
        tree = self.parser.parse(bytes(source, "utf-8"))
        
        def hash_node(node: Node) -> str:
            """Recursively build a structural representation."""
            if node.type == "identifier":
                # Replace identifiers with placeholder
                return "ID"
            elif node.type in ("integer", "float", "string"):
                # Replace literals with type placeholder
                return node.type.upper()
            elif node.child_count == 0:
                # Leaf node - use type
                return node.type
            else:
                # Internal node - combine type with children
                children_hash = ",".join(hash_node(child) for child in node.children)
                return f"{node.type}({children_hash})"
        
        structure = hash_node(tree.root_node)
        return hashlib.sha256(structure.encode()).hexdigest()[:16]
    
    def _compute_complexity(self, source: str) -> ComplexityMetrics:
        """
        Compute complexity metrics for the source code.
        
        Metrics:
        - Cyclomatic complexity: Number of decision points + 1
        - Nesting depth: Maximum depth of nested control structures
        - Loops: Count of for/while loops
        - Conditionals: Count of if/elif/else and ternary operators
        - Lines: Non-empty, non-comment lines
        
        Args:
            source: Source code
        
        Returns:
            ComplexityMetrics object
        """
        tree = self.parser.parse(bytes(source, "utf-8"))
        
        metrics = ComplexityMetrics()
        
        # Count non-empty, non-comment lines (language-aware)
        comment_prefixes = {
            "python": ["#"],
            "javascript": ["//"],
            "typescript": ["//"],
        }
        prefixes = comment_prefixes.get(self.language, ["#", "//"])
        lines = [line for line in source.split("\n") 
                 if line.strip() and not any(line.strip().startswith(p) for p in prefixes)]
        metrics.lines = len(lines)
        
        # Get language-specific node types
        loop_nodes = set(LOOP_NODES.get(self.language, []))
        conditional_nodes = set(CONDITIONAL_NODES.get(self.language, []))
        nesting_nodes = set(NESTING_NODES.get(self.language, []))
        
        def analyze_node(node: Node, depth: int = 0):
            """Recursively analyze nodes for complexity."""
            # Track nesting depth for control structures
            is_nesting = node.type in nesting_nodes
            
            current_depth = depth + 1 if is_nesting else depth
            metrics.nesting_depth = max(metrics.nesting_depth, current_depth)
            
            # Count decision points for cyclomatic complexity
            if node.type in conditional_nodes:
                metrics.cyclomatic += 1
                metrics.conditionals += 1
            elif node.type in loop_nodes:
                metrics.cyclomatic += 1
                metrics.loops += 1
            elif node.type in ("and", "or", "&&", "||"):  # Boolean operators
                metrics.cyclomatic += 1
            elif node.type in ("except_clause", "catch_clause"):  # Exception handlers
                metrics.cyclomatic += 1
            elif node.type in ("case_clause", "switch_case"):  # Switch/match cases
                metrics.cyclomatic += 1
            elif node.type == "elif_clause":  # Python elif
                metrics.cyclomatic += 1
                metrics.conditionals += 1
            
            # Recurse into children
            for child in node.children:
                analyze_node(child, current_depth if is_nesting else depth)
        
        analyze_node(tree.root_node)
        
        return metrics
    
    def _classify_static(
        self, 
        source: str, 
        symbol_name: str, 
        metrics: ComplexityMetrics
    ) -> str:
        """
        Classify the algorithm into a category using static analysis.
        
        Uses keyword matching, regex patterns, and complexity heuristics.
        
        Args:
            source: Source code
            symbol_name: Function/method name
            metrics: Computed complexity metrics
        
        Returns:
            Category string (sorting, searching, graph, dp, math, string, tree, io, other)
        """
        source_lower = source.lower()
        name_lower = symbol_name.lower()
        
        scores: dict[str, float] = {cat: 0.0 for cat in STATIC_CATEGORIES}
        
        for category, info in STATIC_CATEGORIES.items():
            # Check keywords in function name
            for kw in info["keywords"]:
                if kw in name_lower:
                    scores[category] += 2.0
                if kw in source_lower:
                    scores[category] += 0.5
            
            # Check regex patterns
            for pattern in info["patterns"]:
                if re.search(pattern, source, re.IGNORECASE):
                    scores[category] += 1.5
        
        # Apply heuristics based on complexity
        if metrics.loops >= 2 and metrics.conditionals >= 2:
            scores["sorting"] += 0.5
            scores["searching"] += 0.3
        
        if metrics.nesting_depth >= 3:
            scores["graph"] += 0.3
            scores["tree"] += 0.3
        
        # Find best category
        best_category = max(scores, key=scores.get)
        if scores[best_category] < 1.0:
            return "other"
        
        return best_category
    
    def should_extract(
        self, 
        symbol_type: str, 
        start_line: int, 
        end_line: int, 
        min_lines: int = 5
    ) -> bool:
        """
        Determine if a symbol should be extracted as an algorithm.
        
        Args:
            symbol_type: Type of symbol ('function', 'method', 'class', 'component')
            start_line: Start line of the symbol
            end_line: End line of the symbol
            min_lines: Minimum line count threshold
        
        Returns:
            True if the symbol should be extracted
        """
        # Only extract functions, methods, and components
        if symbol_type not in ("function", "method", "component"):
            return False
        
        # Check minimum line count
        line_count = end_line - start_line + 1
        if line_count < min_lines:
            return False
        
        return True
