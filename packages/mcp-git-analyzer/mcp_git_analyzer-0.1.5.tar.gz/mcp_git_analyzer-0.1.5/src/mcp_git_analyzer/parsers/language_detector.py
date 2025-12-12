"""Language detection utility for C/C++ header files.

This module provides utilities to detect whether a .h file is C or C++ based on:
1. Syntactic patterns (keywords, headers, constructs)
2. Build file analysis (CMakeLists.txt, Makefile)
"""

from __future__ import annotations

import re
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache


class DetectedLanguage(Enum):
    """Detected language for ambiguous files."""
    C = "c"
    CPP = "cpp"
    UNKNOWN = "unknown"


@dataclass
class DetectionResult:
    """Result of language detection."""
    language: DetectedLanguage
    confidence: float  # 0.0 to 1.0
    evidence: list[str]  # Reasons for detection


# C++ only keywords that cannot appear in pure C
CPP_ONLY_KEYWORDS = {
    # C++98/03
    "class", "namespace", "template", "typename", "new", "delete",
    "private", "public", "protected", "virtual", "override", "final",
    "try", "catch", "throw", "explicit", "mutable",
    "dynamic_cast", "static_cast", "reinterpret_cast", "const_cast",
    "typeid", "operator", "using",
    # C++11
    "constexpr", "decltype", "nullptr", "noexcept",
    "alignas", "alignof", "static_assert", "thread_local",
    "char16_t", "char32_t",
    # C++20
    "concept", "requires", "co_await", "co_yield", "co_return",
    "consteval", "constinit", "char8_t",
    # C++23
    "import", "module", "export",
}

# C++ only standard library headers (no .h extension)
CPP_ONLY_HEADERS = {
    "iostream", "istream", "ostream", "fstream", "sstream", "streambuf",
    "vector", "string", "map", "set", "list", "deque", "array", "forward_list",
    "unordered_map", "unordered_set", "queue", "stack", "priority_queue",
    "algorithm", "numeric", "functional", "iterator", "memory", "utility",
    "tuple", "optional", "variant", "any", "bitset", "valarray",
    "chrono", "thread", "mutex", "future", "atomic", "condition_variable",
    "regex", "filesystem", "random", "complex", "ratio", "type_traits",
    "initializer_list", "typeindex", "typeinfo", "exception", "stdexcept",
    "system_error", "limits", "new", "scoped_allocator", "shared_mutex",
    "execution", "span", "ranges", "concepts", "coroutine", "compare",
    "version", "source_location", "numbers", "bit", "format", "expected",
}

# C++ wrapper headers for C standard library (cstdio instead of stdio.h)
CPP_C_WRAPPER_PATTERN = re.compile(r"^c[a-z]+$")

# C-specific patterns (C99/C11/C23)
C_ONLY_KEYWORDS = {
    "restrict",  # C99
    "_Bool", "_Complex", "_Imaginary",  # C99
    "_Atomic", "_Generic", "_Noreturn",  # C11
    "_Static_assert", "_Thread_local", "_Alignas", "_Alignof",  # C11
}

# Regex patterns for C++ syntax detection
CPP_SYNTAX_PATTERNS = [
    (re.compile(r"\bclass\s+\w+\s*[:{]"), "class definition"),
    (re.compile(r"\bnamespace\s+\w+"), "namespace declaration"),
    (re.compile(r"\btemplate\s*<"), "template declaration"),
    (re.compile(r"::\s*\w+"), "scope resolution operator"),
    (re.compile(r"\busing\s+namespace\b"), "using namespace"),
    (re.compile(r"\bstd::\w+"), "std:: usage"),
    (re.compile(r"\b(public|private|protected)\s*:"), "access specifier"),
    (re.compile(r"\bvirtual\s+\w+"), "virtual function"),
    (re.compile(r"\boverride\s*[;{]"), "override specifier"),
    (re.compile(r"\w+\s*&\s*\w+\s*[,=)]"), "reference parameter"),
    (re.compile(r"\[\s*[^\]]*\s*\]\s*\("), "lambda expression"),
    (re.compile(r"\bauto\s+\w+\s*="), "auto type deduction"),
    (re.compile(r"\bnullptr\b"), "nullptr usage"),
    (re.compile(r"\bconstexpr\b"), "constexpr usage"),
    (re.compile(r"\bnoexcept\b"), "noexcept specifier"),
    (re.compile(r"\bdecltype\s*\("), "decltype usage"),
    (re.compile(r"\bstatic_cast\s*<"), "static_cast"),
    (re.compile(r"\bdynamic_cast\s*<"), "dynamic_cast"),
    (re.compile(r"\breinterpret_cast\s*<"), "reinterpret_cast"),
    (re.compile(r"\bconst_cast\s*<"), "const_cast"),
    (re.compile(r"\bstd::(unique_ptr|shared_ptr|weak_ptr)<"), "smart pointer"),
    (re.compile(r"\boperator\s*[+\-*/%&|^~!=<>]+\s*\("), "operator overloading"),
]

# Regex patterns for C-only syntax
C_ONLY_PATTERNS = [
    (re.compile(r"\brestrict\b"), "restrict keyword"),
    (re.compile(r"\b_Generic\s*\("), "_Generic expression"),
    (re.compile(r"\b_Atomic\b"), "_Atomic qualifier"),
    (re.compile(r"\b_Bool\b"), "_Bool type"),
    (re.compile(r"\b_Complex\b"), "_Complex type"),
    (re.compile(r"\b_Noreturn\b"), "_Noreturn specifier"),
]

# CMake patterns
CMAKE_CXX_PATTERNS = [
    (re.compile(r"LANGUAGES\s+.*\bCXX\b", re.IGNORECASE), "CMake CXX language"),
    (re.compile(r"project\s*\([^)]*\bCXX\b", re.IGNORECASE), "CMake project CXX"),
    (re.compile(r"enable_language\s*\(\s*CXX", re.IGNORECASE), "CMake enable CXX"),
    (re.compile(r"CMAKE_CXX_STANDARD", re.IGNORECASE), "CMAKE_CXX_STANDARD"),
    (re.compile(r"CMAKE_CXX_FLAGS", re.IGNORECASE), "CMAKE_CXX_FLAGS"),
    (re.compile(r"\bCXX_STANDARD\b", re.IGNORECASE), "CXX_STANDARD property"),
    (re.compile(r"\.cpp\b|\.cxx\b|\.cc\b"), "C++ source files"),
]

CMAKE_C_ONLY_PATTERNS = [
    (re.compile(r"LANGUAGES\s+C\s*\)", re.IGNORECASE), "CMake C-only language"),
    (re.compile(r"CMAKE_C_STANDARD", re.IGNORECASE), "CMAKE_C_STANDARD"),
    (re.compile(r"CMAKE_C_FLAGS", re.IGNORECASE), "CMAKE_C_FLAGS"),
    (re.compile(r"\bC_STANDARD\b", re.IGNORECASE), "C_STANDARD property"),
]

# Makefile patterns
MAKEFILE_CXX_PATTERNS = [
    (re.compile(r"\bCXX\s*[:?]?="), "CXX variable"),
    (re.compile(r"\bCXXFLAGS\s*[:?]?="), "CXXFLAGS variable"),
    (re.compile(r"\$\(CXX\)"), "$(CXX) usage"),
    (re.compile(r"\bg\+\+\b"), "g++ compiler"),
    (re.compile(r"\bclang\+\+\b"), "clang++ compiler"),
    (re.compile(r"-std=c\+\+"), "C++ standard flag"),
    (re.compile(r"\.cpp\b|\.cxx\b|\.cc\b"), "C++ source files"),
]

MAKEFILE_C_ONLY_PATTERNS = [
    (re.compile(r"\bCC\s*[:?]?=\s*(?!.*\+\+)"), "CC variable (not C++)"),
    (re.compile(r"\bCFLAGS\s*[:?]?="), "CFLAGS variable"),
    (re.compile(r"-std=c[0-9]"), "C standard flag"),
]


def detect_language_from_content(source: str) -> DetectionResult:
    """
    Detect whether source code is C or C++ based on content analysis.
    
    Args:
        source: Source code content
    
    Returns:
        DetectionResult with detected language, confidence, and evidence
    """
    evidence_cpp: list[str] = []
    evidence_c: list[str] = []
    
    # Check for C++ only headers in #include
    include_pattern = re.compile(r'#include\s*[<"]([^>"]+)[>"]')
    for match in include_pattern.finditer(source):
        header = match.group(1)
        header_name = header.replace(".h", "").split("/")[-1]
        
        if header_name in CPP_ONLY_HEADERS:
            evidence_cpp.append(f"C++ header <{header}>")
        elif CPP_C_WRAPPER_PATTERN.match(header_name):
            evidence_cpp.append(f"C++ wrapper header <{header}>")
    
    # Check for C++ keywords
    # Use word boundary to avoid false positives
    for keyword in CPP_ONLY_KEYWORDS:
        pattern = re.compile(rf"\b{keyword}\b")
        if pattern.search(source):
            evidence_cpp.append(f"C++ keyword '{keyword}'")
            if len(evidence_cpp) >= 3:  # Early exit if enough evidence
                break
    
    # Check for C++ syntax patterns
    for pattern, description in CPP_SYNTAX_PATTERNS:
        if pattern.search(source):
            evidence_cpp.append(description)
            if len(evidence_cpp) >= 5:  # Early exit
                break
    
    # Check for C-only patterns
    for keyword in C_ONLY_KEYWORDS:
        pattern = re.compile(rf"\b{keyword}\b")
        if pattern.search(source):
            evidence_c.append(f"C-only keyword '{keyword}'")
    
    for pattern, description in C_ONLY_PATTERNS:
        if pattern.search(source):
            evidence_c.append(description)
    
    # Determine result
    if evidence_cpp and not evidence_c:
        confidence = min(0.5 + len(evidence_cpp) * 0.1, 1.0)
        return DetectionResult(DetectedLanguage.CPP, confidence, evidence_cpp)
    elif evidence_c and not evidence_cpp:
        confidence = min(0.5 + len(evidence_c) * 0.1, 1.0)
        return DetectionResult(DetectedLanguage.C, confidence, evidence_c)
    elif evidence_cpp and evidence_c:
        # Rare: mixed indicators. C++ wins if more evidence
        if len(evidence_cpp) > len(evidence_c):
            return DetectionResult(
                DetectedLanguage.CPP, 
                0.6, 
                evidence_cpp + [f"(also C indicators: {', '.join(evidence_c)})"]
            )
        else:
            return DetectionResult(
                DetectedLanguage.C, 
                0.6, 
                evidence_c + [f"(also C++ indicators: {', '.join(evidence_cpp)})"]
            )
    else:
        # No strong indicators - default to C (conservative)
        return DetectionResult(
            DetectedLanguage.UNKNOWN, 
            0.3, 
            ["no definitive indicators found, defaulting to C"]
        )


def detect_language_from_build_file(build_file_path: Path) -> DetectionResult | None:
    """
    Detect project language from build file (CMakeLists.txt or Makefile).
    
    Args:
        build_file_path: Path to CMakeLists.txt or Makefile
    
    Returns:
        DetectionResult or None if cannot determine
    """
    if not build_file_path.exists():
        return None
    
    try:
        content = build_file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None
    
    evidence_cpp: list[str] = []
    evidence_c: list[str] = []
    
    file_name = build_file_path.name.lower()
    
    if file_name == "cmakelists.txt":
        for pattern, description in CMAKE_CXX_PATTERNS:
            if pattern.search(content):
                evidence_cpp.append(description)
        
        for pattern, description in CMAKE_C_ONLY_PATTERNS:
            if pattern.search(content):
                evidence_c.append(description)
    
    elif file_name in ("makefile", "gnumakefile") or file_name.endswith(".mk"):
        for pattern, description in MAKEFILE_CXX_PATTERNS:
            if pattern.search(content):
                evidence_cpp.append(description)
        
        for pattern, description in MAKEFILE_C_ONLY_PATTERNS:
            if pattern.search(content):
                evidence_c.append(description)
    
    if evidence_cpp and not evidence_c:
        return DetectionResult(DetectedLanguage.CPP, 0.8, evidence_cpp)
    elif evidence_c and not evidence_cpp:
        return DetectionResult(DetectedLanguage.C, 0.8, evidence_c)
    elif evidence_cpp and evidence_c:
        # Mixed project - likely has both C and C++
        return DetectionResult(
            DetectedLanguage.CPP,  # Prefer C++ for mixed
            0.6,
            evidence_cpp + ["(mixed C/C++ project)"]
        )
    
    return None


@lru_cache(maxsize=128)
def find_build_file(directory: Path) -> Path | None:
    """
    Find build file in directory or parent directories.
    
    Args:
        directory: Starting directory
    
    Returns:
        Path to build file or None
    """
    build_files = ["CMakeLists.txt", "Makefile", "makefile", "GNUmakefile"]
    
    current = directory
    for _ in range(10):  # Limit search depth
        for build_file in build_files:
            candidate = current / build_file
            if candidate.exists():
                return candidate
        
        parent = current.parent
        if parent == current:
            break
        current = parent
    
    return None


class BuildFileCache:
    """Cache for build file analysis results per repository."""
    
    def __init__(self):
        self._cache: dict[str, DetectionResult | None] = {}
    
    def get_project_language(self, repo_path: Path) -> DetectionResult | None:
        """
        Get cached language detection result for repository.
        
        Args:
            repo_path: Repository root path
        
        Returns:
            Cached DetectionResult or None
        """
        key = str(repo_path)
        if key not in self._cache:
            build_file = find_build_file(repo_path)
            if build_file:
                self._cache[key] = detect_language_from_build_file(build_file)
            else:
                self._cache[key] = None
        return self._cache.get(key)
    
    def clear(self):
        """Clear the cache."""
        self._cache.clear()


# Global build file cache
_build_file_cache = BuildFileCache()


def detect_header_language(
    file_path: Path,
    source: str | None = None,
    repo_path: Path | None = None
) -> DetectionResult:
    """
    Detect language for a .h header file.
    
    Priority:
    1. Content analysis (strongest indicators)
    2. Build file analysis
    3. Default to C (conservative)
    
    Args:
        file_path: Path to header file
        source: Source content (optional, will be read if not provided)
        repo_path: Repository root path for build file lookup
    
    Returns:
        DetectionResult with detected language
    """
    # Read source if not provided
    if source is None:
        try:
            source = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return DetectionResult(
                DetectedLanguage.C,
                0.3,
                ["failed to read file, defaulting to C"]
            )
    
    # Content analysis
    content_result = detect_language_from_content(source)
    
    # If high confidence from content, use it
    if content_result.language != DetectedLanguage.UNKNOWN and content_result.confidence >= 0.7:
        return content_result
    
    # Try build file analysis
    if repo_path:
        build_result = _build_file_cache.get_project_language(repo_path)
        if build_result:
            # Combine with content result
            if content_result.language == build_result.language:
                # Agreement - boost confidence
                return DetectionResult(
                    build_result.language,
                    min(1.0, content_result.confidence + 0.2),
                    content_result.evidence + build_result.evidence
                )
            elif content_result.language == DetectedLanguage.UNKNOWN:
                # Use build file result
                return build_result
            # Conflict - trust content more
    
    # Default handling
    if content_result.language == DetectedLanguage.UNKNOWN:
        return DetectionResult(
            DetectedLanguage.C,
            0.4,
            ["no definitive indicators, defaulting to C"]
        )
    
    return content_result


def get_language_for_extension(
    extension: str,
    file_path: Path | None = None,
    source: str | None = None,
    repo_path: Path | None = None
) -> str:
    """
    Get the language name for a file extension.
    
    For .h files, performs language detection.
    
    Args:
        extension: File extension (e.g., ".c", ".h", ".cpp")
        file_path: Optional file path for .h detection
        source: Optional source content for .h detection
        repo_path: Optional repository path for build file lookup
    
    Returns:
        Language string: "c", "cpp", or "csharp"
    """
    # Clear mapping for non-ambiguous extensions
    extension_map = {
        ".c": "c",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".cxx": "cpp",
        ".c++": "cpp",
        ".hpp": "cpp",
        ".hxx": "cpp",
        ".h++": "cpp",
        ".hh": "cpp",
        ".cs": "csharp",
    }
    
    if extension in extension_map:
        return extension_map[extension]
    
    # Handle .h files with detection
    if extension == ".h":
        if file_path and source is None:
            result = detect_header_language(file_path, repo_path=repo_path)
        elif source:
            result = detect_language_from_content(source)
            if result.language == DetectedLanguage.UNKNOWN:
                result = DetectionResult(DetectedLanguage.C, 0.4, ["default"])
        else:
            result = DetectionResult(DetectedLanguage.C, 0.4, ["default"])
        
        return result.language.value if result.language != DetectedLanguage.UNKNOWN else "c"
    
    return "unknown"


def clear_build_file_cache():
    """Clear the build file cache."""
    _build_file_cache.clear()
    find_build_file.cache_clear()
