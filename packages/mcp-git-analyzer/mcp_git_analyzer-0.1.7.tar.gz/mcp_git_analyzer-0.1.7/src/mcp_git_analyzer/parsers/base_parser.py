"""Base parser interface and shared data structures for multi-language support."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class Symbol:
    """Represents a code symbol (function, class, method, component, interface, type_alias)."""
    name: str
    type: str  # 'function', 'class', 'method', 'variable', 'component', 'interface', 'type_alias'
    signature: str
    docstring: str | None
    start_line: int
    end_line: int
    parent_name: str | None = None
    parameters: list[dict] = field(default_factory=list)
    return_type: str | None = None
    decorators: list[str] = field(default_factory=list)
    # Additional metadata for extended symbol types
    is_async: bool = False
    is_generator: bool = False
    is_exported: bool = False
    generic_params: list[str] = field(default_factory=list)
    # Struct/class field definitions (for C/C++/Rust structs, TypeScript interfaces)
    fields: list[dict] = field(default_factory=list)  # [{name, type, visibility?, default?}]
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Import:
    """Represents an import statement."""
    module: str
    alias: str | None
    imported_names: list[str]
    is_relative: bool
    line_number: int
    import_type: str = "esm"  # 'esm', 'commonjs', 'python'
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Pattern:
    """Represents a detected code pattern."""
    pattern_type: str  # 'algorithm', 'design_pattern', 'idiom', 'async_pattern'
    pattern_name: str
    confidence: float
    evidence: str
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class FunctionCall:
    """Represents a function or method call."""
    caller_name: str  # Fully qualified name of the calling function
    callee_name: str  # Name of the called function/method
    call_type: str  # 'function', 'method', 'builtin', 'constructor'
    line_number: int
    is_external: bool  # True if callee is from an imported module
    module: str | None = None  # Module name if external
    arguments: list[str] = field(default_factory=list)  # Argument representations
    is_async_call: bool = False  # True for await expressions
    
    def to_dict(self) -> dict:
        return asdict(self)


# Common algorithm patterns (language-agnostic)
ALGORITHM_PATTERNS: dict[str, dict] = {
    "recursion": {
        "keywords": ["recursive", "recursion", "self-call"],
        "indicators": None  # Handled by call graph analysis
    },
    "dynamic_programming": {
        "keywords": ["dp", "memoization", "memoize", "cache", "tabulation"],
        "indicators": None  # Language-specific
    },
    "divide_and_conquer": {
        "keywords": ["divide", "conquer", "merge", "split"],
        "indicators": None
    },
    "binary_search": {
        "keywords": ["binary_search", "bisect", "binarySearch"],
        "indicators": None
    },
    "sorting": {
        "keywords": ["sort", "quicksort", "mergesort", "heapsort", "bubblesort"],
        "indicators": None
    },
    "graph_traversal": {
        "keywords": ["bfs", "dfs", "breadth_first", "depth_first", "traverse", "breadthFirst", "depthFirst"],
        "indicators": None
    },
    "greedy": {
        "keywords": ["greedy", "optimal", "best"],
        "indicators": None
    },
    "backtracking": {
        "keywords": ["backtrack", "backtracking"],
        "indicators": None
    },
}

# Common design patterns (language-agnostic)
DESIGN_PATTERNS: dict[str, dict] = {
    "singleton": {
        "keywords": ["singleton", "instance", "getInstance"],
        "indicators": None
    },
    "factory": {
        "keywords": ["factory", "create", "builder", "make"],
        "indicators": None
    },
    "decorator_pattern": {
        "keywords": ["wrapper", "decorator", "wrap"],
        "indicators": None
    },
    "observer": {
        "keywords": ["observer", "subscribe", "publish", "emit", "on", "addEventListener"],
        "indicators": None
    },
    "strategy": {
        "keywords": ["strategy", "policy"],
        "indicators": None
    },
}

# JavaScript/TypeScript specific patterns
JS_PATTERNS: dict[str, dict] = {
    "promise_chain": {
        "keywords": ["then", "catch", "finally"],
        "indicators": lambda code, name: ".then(" in code or ".catch(" in code
    },
    "async_await": {
        "keywords": ["async", "await"],
        "indicators": lambda code, name: "async " in code and "await " in code
    },
    "callback": {
        "keywords": ["callback", "cb", "done", "next"],
        "indicators": lambda code, name: "callback" in code.lower() or ", cb)" in code or ", done)" in code
    },
    "react_hooks": {
        "keywords": ["useState", "useEffect", "useMemo", "useCallback", "useRef", "useContext", "useReducer"],
        "indicators": lambda code, name: "use" in name and name[0].islower() and len(name) > 3 and name[3].isupper()
    },
    "higher_order_function": {
        "keywords": ["map", "filter", "reduce", "forEach", "find", "some", "every"],
        "indicators": lambda code, name: any(f".{fn}(" in code for fn in ["map", "filter", "reduce", "forEach"])
    },
    "module_pattern": {
        "keywords": ["module", "exports", "require"],
        "indicators": lambda code, name: "module.exports" in code or "exports." in code
    },
    "event_emitter": {
        "keywords": ["emit", "on", "once", "removeListener", "addEventListener"],
        "indicators": lambda code, name: ".emit(" in code or ".on(" in code or "addEventListener" in code
    },
}


class BaseParser(ABC):
    """Abstract base class for language-specific parsers."""
    
    @property
    @abstractmethod
    def language(self) -> str:
        """Return the language name (e.g., 'python', 'javascript', 'typescript')."""
        pass
    
    @property
    @abstractmethod
    def file_extensions(self) -> list[str]:
        """Return list of file extensions this parser handles (e.g., ['.py'])."""
        pass
    
    @abstractmethod
    def parse_file(self, file_path: Path) -> dict:
        """
        Parse a source file and extract all symbols, imports, and patterns.
        
        Args:
            file_path: Path to the source file
        
        Returns:
            Dict with symbols, imports, patterns, and metadata
        """
        pass
    
    @abstractmethod
    def parse_source(self, source: str, file_name: str = "<source>", 
                     extract_calls: bool = False) -> dict:
        """
        Parse source code string.
        
        Args:
            source: Source code string
            file_name: Optional file name for context
            extract_calls: If True, extract function call graph
        
        Returns:
            Dict with symbols, imports, patterns, calls (if enabled), and metadata
        """
        pass
    
    def _node_text(self, node, source: str) -> str:
        """Get text content of a Tree-sitter node."""
        if not node:
            return ""
        return source[node.start_byte:node.end_byte]
    
    def _get_child_by_type(self, node, types: list[str], skip: int = 0):
        """Get first child of given type(s)."""
        count = 0
        for child in node.children:
            if child.type in types:
                if count >= skip:
                    return child
                count += 1
        return None
    
    def _get_children_by_type(self, node, types: list[str]) -> list:
        """Get all children of given type(s)."""
        return [child for child in node.children if child.type in types]
    
    def _create_parse_result(
        self,
        file_name: str,
        source: str,
        symbols: list[Symbol],
        imports: list[Import],
        patterns: list[Pattern],
        calls: list[FunctionCall] | None = None
    ) -> dict:
        """Create standardized parse result dictionary."""
        # Determine source type based on file name
        source_type = self._determine_source_type(file_name)
        
        result = {
            "file": file_name,
            "language": self.language,
            "source_type": source_type,
            "line_count": source.count("\n") + 1,
            "symbols": [s.to_dict() for s in symbols],
            "imports": [i.to_dict() for i in imports],
            "patterns": [p.to_dict() for p in patterns],
            "summary": {
                "total_symbols": len(symbols),
                "functions": len([s for s in symbols if s.type == "function"]),
                "classes": len([s for s in symbols if s.type == "class"]),
                "methods": len([s for s in symbols if s.type == "method"]),
                "components": len([s for s in symbols if s.type == "component"]),
                "interfaces": len([s for s in symbols if s.type == "interface"]),
                "type_aliases": len([s for s in symbols if s.type == "type_alias"]),
                "total_imports": len(imports),
                "patterns_detected": len(patterns),
                "total_calls": len(calls) if calls else 0
            }
        }
        
        if calls is not None:
            result["calls"] = [c.to_dict() for c in calls]
        
        return result
    
    def _determine_source_type(self, file_name: str) -> str:
        """
        Determine the source type of a file.
        
        Args:
            file_name: File path/name to check
        
        Returns:
            "header": Header files (.h, .hpp, etc.)
            "test": Test files (test_*, *_test.*, tests/ directory)
            "source": Regular source files
        """
        if not file_name or file_name == "<source>":
            return "source"
        
        from pathlib import Path
        path = Path(file_name)
        name = path.name.lower()
        ext = path.suffix.lower()
        file_path_lower = file_name.lower()
        
        # Check for test files
        if (name.startswith("test_") or 
            name.startswith("spec_") or
            "_test." in name or
            ".test." in name or
            "_spec." in name or
            ".spec." in name or
            "tests/" in file_path_lower or
            "test/" in file_path_lower or
            "__tests__/" in file_path_lower):
            return "test"
        
        # Check for header files (C/C++)
        header_extensions = {".h", ".hpp", ".hxx", ".h++", ".hh", ".inl"}
        if ext in header_extensions:
            return "header"
        
        return "source"
    
    def _is_pascal_case(self, name: str) -> bool:
        """Check if a name is in PascalCase (used for React component detection)."""
        if not name or len(name) < 2:
            return False
        return name[0].isupper() and not name.isupper() and "_" not in name
