"""Parsers package."""

from mcp_git_analyzer.parsers.base_parser import (
    BaseParser,
    Symbol,
    Import,
    Pattern,
    FunctionCall,
    ALGORITHM_PATTERNS,
    DESIGN_PATTERNS,
    JS_PATTERNS,
)
from mcp_git_analyzer.parsers.python_parser import PythonParser
from mcp_git_analyzer.parsers.javascript_parser import JavaScriptParser
from mcp_git_analyzer.parsers.typescript_parser import TypeScriptParser
from mcp_git_analyzer.parsers.java_parser import JavaParser
from mcp_git_analyzer.parsers.go_parser import GoParser
from mcp_git_analyzer.parsers.rust_parser import RustParser
from mcp_git_analyzer.parsers.c_parser import CParser
from mcp_git_analyzer.parsers.cpp_parser import CppParser
from mcp_git_analyzer.parsers.csharp_parser import CSharpParser
from mcp_git_analyzer.parsers.algorithm_extractor import (
    AlgorithmExtractor,
    AlgorithmInfo,
    ComplexityMetrics,
)
from mcp_git_analyzer.parsers.similarity import (
    SimilarityAnalyzer,
    SimilarAlgorithm,
)
from mcp_git_analyzer.parsers.language_detector import (
    detect_header_language,
    detect_language_from_content,
    detect_language_from_build_file,
    get_language_for_extension,
    DetectedLanguage,
    DetectionResult,
    clear_build_file_cache,
)


def get_parser(language: str) -> BaseParser | None:
    """
    Factory function to get the appropriate parser for a language.
    
    Args:
        language: Language name ('python', 'javascript', 'typescript', 'java', 'go', 'rust',
                  'c', 'cpp', 'csharp')
    
    Returns:
        Parser instance or None if language not supported
    """
    parsers = {
        "python": PythonParser,
        "javascript": JavaScriptParser,
        "typescript": TypeScriptParser,
        "java": JavaParser,
        "go": GoParser,
        "rust": RustParser,
        "c": CParser,
        "cpp": CppParser,
        "csharp": CSharpParser,
    }
    parser_class = parsers.get(language)
    return parser_class() if parser_class else None


__all__ = [
    # Base classes and data structures
    "BaseParser",
    "Symbol",
    "Import",
    "Pattern",
    "FunctionCall",
    # Pattern definitions
    "ALGORITHM_PATTERNS",
    "DESIGN_PATTERNS",
    "JS_PATTERNS",
    # Language-specific parsers
    "PythonParser",
    "JavaScriptParser",
    "TypeScriptParser",
    "JavaParser",
    "GoParser",
    "RustParser",
    "CParser",
    "CppParser",
    "CSharpParser",
    # Factory function
    "get_parser",
    # Algorithm extraction
    "AlgorithmExtractor",
    "AlgorithmInfo",
    "ComplexityMetrics",
    # Similarity analysis
    "SimilarityAnalyzer",
    "SimilarAlgorithm",
    # Language detection
    "detect_header_language",
    "detect_language_from_content",
    "detect_language_from_build_file",
    "get_language_for_extension",
    "DetectedLanguage",
    "DetectionResult",
    "clear_build_file_cache",
]
