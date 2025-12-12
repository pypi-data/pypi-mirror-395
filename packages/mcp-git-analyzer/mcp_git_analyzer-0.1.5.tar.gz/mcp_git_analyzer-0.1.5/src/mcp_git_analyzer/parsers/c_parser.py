"""C code parser using Tree-sitter."""

from pathlib import Path

import tree_sitter_c as tsc
from tree_sitter import Language, Parser, Node

from mcp_git_analyzer.parsers.base_parser import (
    BaseParser,
    Symbol,
    Import,
    Pattern,
    FunctionCall,
    ALGORITHM_PATTERNS as BASE_ALGORITHM_PATTERNS,
    DESIGN_PATTERNS as BASE_DESIGN_PATTERNS,
)


# Initialize C parser
C_LANGUAGE = Language(tsc.language())
_parser = Parser(C_LANGUAGE)


# C-specific pattern indicators (extending base patterns)
ALGORITHM_PATTERNS = {
    **BASE_ALGORITHM_PATTERNS,
    "dynamic_programming": {
        **BASE_ALGORITHM_PATTERNS["dynamic_programming"],
        "indicators": lambda code, name: (
            "memo" in code.lower() or 
            "cache" in code.lower() or 
            "dp[" in code or
            "table[" in code
        )
    },
    "divide_and_conquer": {
        **BASE_ALGORITHM_PATTERNS["divide_and_conquer"],
        "indicators": lambda code, name: (
            ("left" in code and "right" in code) or 
            "mid" in code or
            "pivot" in code
        )
    },
    "binary_search": {
        **BASE_ALGORITHM_PATTERNS["binary_search"],
        "indicators": lambda code, name: (
            "mid" in code and 
            ("low" in code or "left" in code) and 
            ("high" in code or "right" in code)
        )
    },
    "sorting": {
        **BASE_ALGORITHM_PATTERNS["sorting"],
        "indicators": lambda code, name: (
            "qsort(" in code or 
            "swap" in code.lower() or
            "partition" in code.lower()
        )
    },
    "graph_traversal": {
        **BASE_ALGORITHM_PATTERNS["graph_traversal"],
        "indicators": lambda code, name: (
            "visited" in code.lower() and 
            ("queue" in code.lower() or "stack" in code.lower())
        )
    },
    "memory_management": {
        "keywords": ["malloc", "calloc", "realloc", "free", "alloc"],
        "indicators": lambda code, name: (
            "malloc(" in code or 
            "calloc(" in code or 
            "realloc(" in code or
            "free(" in code
        )
    },
}

DESIGN_PATTERNS = {
    **BASE_DESIGN_PATTERNS,
    "opaque_pointer": {
        "keywords": ["handle", "opaque", "pimpl"],
        "indicators": lambda code, name: (
            "struct" in code and 
            ("typedef" in code or "*" in code) and
            "void*" not in code
        )
    },
    "callback": {
        "keywords": ["callback", "handler", "hook", "func_ptr"],
        "indicators": lambda code, name: (
            "(*" in code and ")(" in code  # Function pointer pattern
        )
    },
    "object_pattern": {
        "keywords": ["init", "create", "destroy", "new", "free"],
        "indicators": lambda code, name: (
            ("_init" in name or "_create" in name or "_new" in name) and
            "struct" in code
        )
    },
}


class CParser(BaseParser):
    """Parse C source code using Tree-sitter."""
    
    def __init__(self):
        self.parser = _parser
    
    @property
    def language(self) -> str:
        return "c"
    
    @property
    def file_extensions(self) -> list[str]:
        return [".c", ".h"]
    
    def parse_file(self, file_path: Path) -> dict:
        """
        Parse a C file and extract all symbols, imports, and patterns.
        
        Args:
            file_path: Path to the C file
        
        Returns:
            Dict with symbols, imports, patterns, and metadata
        """
        try:
            source = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            return {"error": str(e), "symbols": [], "imports": [], "patterns": []}
        
        return self.parse_source(source, str(file_path))
    
    def parse_source(self, source: str, file_name: str = "<source>",
                     extract_calls: bool = False) -> dict:
        """
        Parse C source code string.
        
        Args:
            source: C source code
            file_name: Optional file name for context
            extract_calls: If True, extract function call graph
        
        Returns:
            Dict with symbols, imports, patterns, calls (if enabled), and metadata
        """
        tree = self.parser.parse(bytes(source, "utf-8"))
        root = tree.root_node
        
        symbols: list[Symbol] = []
        imports: list[Import] = []
        
        # Extract includes
        imports.extend(self._extract_includes(root, source))
        
        # Extract symbols
        for child in root.children:
            if child.type == "function_definition":
                func = self._extract_function(child, source)
                if func:
                    symbols.append(func)
            elif child.type == "declaration":
                # Could be function declaration, variable, typedef, or struct
                decl_symbols = self._extract_declaration(child, source)
                symbols.extend(decl_symbols)
            elif child.type == "struct_specifier":
                struct = self._extract_struct(child, source)
                if struct:
                    symbols.append(struct)
            elif child.type == "enum_specifier":
                enum = self._extract_enum(child, source)
                if enum:
                    symbols.append(enum)
            elif child.type == "type_definition":
                typedef = self._extract_typedef(child, source)
                if typedef:
                    symbols.append(typedef)
            elif child.type == "preproc_function_def":
                macro = self._extract_macro_function(child, source)
                if macro:
                    symbols.append(macro)
            elif child.type == "preproc_def":
                macro = self._extract_macro(child, source)
                if macro:
                    symbols.append(macro)
        
        # Detect patterns
        calls: list[FunctionCall] = []
        if extract_calls:
            calls = self._extract_calls_from_symbols(symbols, source, imports)
        
        patterns = self._detect_patterns(symbols, source, calls if extract_calls else None)
        
        return self._create_parse_result(
            file_name=file_name,
            source=source,
            symbols=symbols,
            imports=imports,
            patterns=patterns,
            calls=calls if extract_calls else None
        )
    
    def _extract_includes(self, root: Node, source: str) -> list[Import]:
        """Extract all #include directives."""
        imports = []
        
        for child in root.children:
            if child.type == "preproc_include":
                # #include <header.h> or #include "header.h"
                path_node = self._get_child_by_type(child, ["system_lib_string", "string_literal"])
                if path_node:
                    header = self._node_text(path_node, source)
                    # Remove quotes or angle brackets
                    is_system = header.startswith("<")
                    header_name = header.strip('<>"')
                    
                    imports.append(Import(
                        module=header_name,
                        alias=None,
                        imported_names=[header_name.split("/")[-1].replace(".h", "")],
                        is_relative=not is_system,
                        line_number=child.start_point[0] + 1,
                        import_type="c_include"
                    ))
        
        return imports
    
    def _extract_function(self, node: Node, source: str, 
                          parent_name: str | None = None) -> Symbol | None:
        """Extract function definition."""
        # Get declarator which contains name and parameters
        declarator = self._get_child_by_type(node, ["function_declarator"])
        if not declarator:
            # Try to find nested in pointer_declarator
            ptr_decl = self._get_child_by_type(node, ["pointer_declarator"])
            if ptr_decl:
                declarator = self._get_child_by_type(ptr_decl, ["function_declarator"])
        
        if not declarator:
            return None
        
        # Get function name
        name_node = self._get_child_by_type(declarator, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Get return type
        return_type = self._extract_return_type(node, source)
        
        # Get parameters
        params_node = self._get_child_by_type(declarator, ["parameter_list"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        # Build signature
        params_str = self._node_text(params_node, source) if params_node else "()"
        signature = f"{return_type} {name}{params_str}" if return_type else f"{name}{params_str}"
        
        # Get doc comment
        docstring = self._extract_doc_comment(node, source)
        
        # Check for static
        is_static = self._has_storage_class(node, source, "static")
        
        return Symbol(
            name=name,
            type="function",
            signature=signature.strip(),
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            parameters=parameters,
            return_type=return_type,
            decorators=["static"] if is_static else [],
            is_exported=not is_static
        )
    
    def _extract_declaration(self, node: Node, source: str) -> list[Symbol]:
        """Extract declarations (function prototypes, variables, typedefs)."""
        symbols = []
        
        # Check for typedef
        if self._node_text(node, source).strip().startswith("typedef"):
            typedef = self._extract_typedef(node, source)
            if typedef:
                symbols.append(typedef)
            return symbols
        
        # Check for function declaration (prototype)
        declarator = self._get_child_by_type(node, ["function_declarator"])
        if declarator:
            proto = self._extract_function_prototype(node, source)
            if proto:
                symbols.append(proto)
            return symbols
        
        # Check for struct declaration
        struct_spec = self._get_child_by_type(node, ["struct_specifier"])
        if struct_spec:
            struct = self._extract_struct(struct_spec, source)
            if struct:
                symbols.append(struct)
            return symbols
        
        # Check for enum declaration
        enum_spec = self._get_child_by_type(node, ["enum_specifier"])
        if enum_spec:
            enum = self._extract_enum(enum_spec, source)
            if enum:
                symbols.append(enum)
        
        return symbols
    
    def _extract_function_prototype(self, node: Node, source: str) -> Symbol | None:
        """Extract function prototype (declaration without body)."""
        declarator = self._get_child_by_type(node, ["function_declarator"])
        if not declarator:
            ptr_decl = self._get_child_by_type(node, ["pointer_declarator"])
            if ptr_decl:
                declarator = self._get_child_by_type(ptr_decl, ["function_declarator"])
        
        if not declarator:
            return None
        
        name_node = self._get_child_by_type(declarator, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        return_type = self._extract_return_type(node, source)
        
        params_node = self._get_child_by_type(declarator, ["parameter_list"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        params_str = self._node_text(params_node, source) if params_node else "()"
        signature = f"{return_type} {name}{params_str}" if return_type else f"{name}{params_str}"
        
        docstring = self._extract_doc_comment(node, source)
        is_extern = self._has_storage_class(node, source, "extern")
        
        return Symbol(
            name=name,
            type="function",
            signature=signature.strip(),
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parameters=parameters,
            return_type=return_type,
            decorators=["extern"] if is_extern else [],
            is_exported=is_extern or not self._has_storage_class(node, source, "static")
        )
    
    def _extract_struct(self, node: Node, source: str) -> Symbol | None:
        """Extract struct definition with field details."""
        name_node = self._get_child_by_type(node, ["type_identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Check if it has a body
        body = self._get_child_by_type(node, ["field_declaration_list"])
        if not body:
            return None  # Forward declaration only
        
        # Build signature
        signature = f"struct {name}"
        
        # Extract field details
        fields = []
        for field_decl in body.children:
            if field_decl.type == "field_declaration":
                field_info = self._extract_struct_field(field_decl, source)
                if field_info:
                    fields.append(field_info)
        
        docstring = self._extract_doc_comment(node, source)
        
        return Symbol(
            name=name,
            type="class",  # Treat struct as class for consistency
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parameters=[{"fields": len(fields)}],  # Keep backward compatibility
            is_exported=True,
            fields=fields
        )
    
    def _extract_struct_field(self, node: Node, source: str) -> dict | None:
        """Extract a single struct field with name and type."""
        # Get the type specifier
        type_parts = []
        for child in node.children:
            if child.type in ["primitive_type", "type_identifier", "sized_type_specifier"]:
                type_parts.append(self._node_text(child, source))
            elif child.type == "struct_specifier":
                struct_name = self._get_child_by_type(child, ["type_identifier"])
                if struct_name:
                    type_parts.append(f"struct {self._node_text(struct_name, source)}")
            elif child.type == "enum_specifier":
                enum_name = self._get_child_by_type(child, ["type_identifier"])
                if enum_name:
                    type_parts.append(f"enum {self._node_text(enum_name, source)}")
        
        field_type = " ".join(type_parts) if type_parts else "unknown"
        
        # Get field declarator (name and possible pointer)
        declarator = self._get_child_by_type(node, ["field_identifier"])
        pointer_declarator = self._get_child_by_type(node, ["pointer_declarator"])
        array_declarator = self._get_child_by_type(node, ["array_declarator"])
        
        if pointer_declarator:
            # Handle pointer fields like "int *ptr"
            field_name_node = self._get_child_by_type(pointer_declarator, ["field_identifier"])
            if field_name_node:
                field_name = self._node_text(field_name_node, source)
                # Count pointer levels
                ptr_count = self._node_text(pointer_declarator, source).count("*")
                field_type = field_type + "*" * ptr_count
            else:
                return None
        elif array_declarator:
            # Handle array fields like "int arr[10]"
            field_name_node = self._get_child_by_type(array_declarator, ["field_identifier"])
            if field_name_node:
                field_name = self._node_text(field_name_node, source)
                # Get array size
                size_node = self._get_child_by_type(array_declarator, ["number_literal"])
                if size_node:
                    field_type = f"{field_type}[{self._node_text(size_node, source)}]"
                else:
                    field_type = f"{field_type}[]"
            else:
                return None
        elif declarator:
            field_name = self._node_text(declarator, source)
        else:
            return None
        
        return {
            "name": field_name,
            "type": field_type
        }
    
    def _extract_enum(self, node: Node, source: str) -> Symbol | None:
        """Extract enum definition."""
        name_node = self._get_child_by_type(node, ["type_identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        body = self._get_child_by_type(node, ["enumerator_list"])
        if not body:
            return None
        
        signature = f"enum {name}"
        docstring = self._extract_doc_comment(node, source)
        
        return Symbol(
            name=name,
            type="class",  # Treat enum as class
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            is_exported=True
        )
    
    def _extract_typedef(self, node: Node, source: str) -> Symbol | None:
        """Extract typedef."""
        # typedef can be complex: typedef struct {...} Name; or typedef int MyInt;
        text = self._node_text(node, source)
        
        # Try to find the typedef name (last identifier before semicolon)
        declarator = None
        for child in node.children:
            if child.type == "type_identifier":
                declarator = child
            elif child.type == "pointer_declarator":
                inner = self._get_child_by_type(child, ["type_identifier"])
                if inner:
                    declarator = inner
        
        if not declarator:
            return None
        
        name = self._node_text(declarator, source)
        docstring = self._extract_doc_comment(node, source)
        
        return Symbol(
            name=name,
            type="type_alias",
            signature=text.strip().rstrip(";"),
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            is_exported=True
        )
    
    def _extract_macro_function(self, node: Node, source: str) -> Symbol | None:
        """Extract function-like macro."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Get parameters
        params_node = self._get_child_by_type(node, ["preproc_params"])
        params_str = self._node_text(params_node, source) if params_node else "()"
        
        signature = f"#define {name}{params_str}"
        
        return Symbol(
            name=name,
            type="function",  # Treat macro as function
            signature=signature,
            docstring=None,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            decorators=["macro"],
            is_exported=True
        )
    
    def _extract_macro(self, node: Node, source: str) -> Symbol | None:
        """Extract object-like macro."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Get value
        value_node = self._get_child_by_type(node, ["preproc_arg"])
        value = self._node_text(value_node, source).strip() if value_node else ""
        
        signature = f"#define {name} {value}".strip()
        
        return Symbol(
            name=name,
            type="variable",
            signature=signature,
            docstring=None,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            decorators=["macro"],
            is_exported=True
        )
    
    def _extract_return_type(self, node: Node, source: str) -> str | None:
        """Extract return type from function definition/declaration."""
        for child in node.children:
            if child.type in ("primitive_type", "type_identifier", "sized_type_specifier"):
                return self._node_text(child, source)
            elif child.type == "struct_specifier":
                name_node = self._get_child_by_type(child, ["type_identifier"])
                if name_node:
                    return f"struct {self._node_text(name_node, source)}"
            elif child.type == "enum_specifier":
                name_node = self._get_child_by_type(child, ["type_identifier"])
                if name_node:
                    return f"enum {self._node_text(name_node, source)}"
        
        # Check for pointer return type
        declarator = self._get_child_by_type(node, ["pointer_declarator"])
        if declarator:
            for child in node.children:
                if child.type in ("primitive_type", "type_identifier"):
                    return self._node_text(child, source) + " *"
        
        return None
    
    def _extract_parameters(self, params_node: Node, source: str) -> list[dict]:
        """Extract function parameters with types."""
        parameters = []
        
        for child in params_node.children:
            if child.type == "parameter_declaration":
                param = {"name": "", "type": None}
                
                # Get type
                for type_child in child.children:
                    if type_child.type in ("primitive_type", "type_identifier", "sized_type_specifier"):
                        param["type"] = self._node_text(type_child, source)
                        break
                    elif type_child.type == "struct_specifier":
                        name_node = self._get_child_by_type(type_child, ["type_identifier"])
                        if name_node:
                            param["type"] = f"struct {self._node_text(name_node, source)}"
                        break
                
                # Get name
                declarator = self._get_child_by_type(child, ["identifier", "pointer_declarator"])
                if declarator:
                    if declarator.type == "pointer_declarator":
                        id_node = self._get_child_by_type(declarator, ["identifier"])
                        if id_node:
                            param["name"] = self._node_text(id_node, source)
                            if param["type"]:
                                param["type"] += " *"
                    else:
                        param["name"] = self._node_text(declarator, source)
                
                if param["name"] or param["type"]:
                    parameters.append(param)
            elif child.type == "variadic_parameter":
                parameters.append({"name": "...", "type": "variadic"})
        
        return parameters
    
    def _extract_doc_comment(self, node: Node, source: str) -> str | None:
        """Extract documentation comment before a declaration (Doxygen style)."""
        lines = source[:node.start_byte].split('\n')
        
        doc_lines = []
        in_block = False
        
        for line in reversed(lines):
            stripped = line.strip()
            if stripped.endswith("*/"):
                in_block = True
                doc_lines.insert(0, stripped)
            elif in_block:
                doc_lines.insert(0, stripped)
                if stripped.startswith("/**") or stripped.startswith("/*!"):
                    break
                elif stripped.startswith("/*"):
                    # Regular comment, not doc comment
                    return None
            elif stripped.startswith("///") or stripped.startswith("//!"):
                doc_lines.insert(0, stripped)
            elif stripped and not in_block and not stripped.startswith("//"):
                break
        
        if doc_lines:
            # Check for Doxygen-style
            if doc_lines[0].startswith("/**") or doc_lines[0].startswith("/*!"):
                doc = "\n".join(doc_lines)
                doc = doc.replace("/**", "").replace("/*!", "").replace("*/", "").strip()
                doc = "\n".join(line.lstrip(" *").strip() for line in doc.split("\n"))
                return doc.strip() if doc.strip() else None
            elif doc_lines[0].startswith("///") or doc_lines[0].startswith("//!"):
                doc = "\n".join(
                    line.lstrip("/!").strip() for line in doc_lines
                )
                return doc.strip() if doc.strip() else None
        
        return None
    
    def _has_storage_class(self, node: Node, source: str, specifier: str) -> bool:
        """Check if a declaration has a specific storage class specifier."""
        for child in node.children:
            if child.type == "storage_class_specifier":
                if self._node_text(child, source) == specifier:
                    return True
        return False
    
    def _detect_patterns(
        self,
        symbols: list[Symbol],
        source: str,
        calls: list[FunctionCall] | None = None
    ) -> list[Pattern]:
        """Detect algorithmic and design patterns in code."""
        patterns = []
        
        # Build call graph lookup
        call_graph: dict[str, set[str]] = {}
        if calls:
            for call in calls:
                if call.caller_name not in call_graph:
                    call_graph[call.caller_name] = set()
                call_graph[call.caller_name].add(call.callee_name)
        
        for symbol in symbols:
            if symbol.type != "function":
                continue
            
            lines = source.split("\n")
            func_source = "\n".join(lines[symbol.start_line - 1:symbol.end_line])
            func_source_lower = func_source.lower()
            
            # Check algorithm patterns
            for pattern_name, pattern_info in ALGORITHM_PATTERNS.items():
                confidence = 0.0
                evidence_parts = []
                
                for kw in pattern_info["keywords"]:
                    if kw in symbol.name.lower():
                        confidence += 0.5
                        evidence_parts.append(f"keyword '{kw}' in function name")
                    if symbol.docstring and kw in symbol.docstring.lower():
                        confidence += 0.3
                        evidence_parts.append(f"keyword '{kw}' in doc comment")
                
                # Recursion detection
                if pattern_name == "recursion" and call_graph:
                    recursion_info = self._detect_recursion(symbol.name, call_graph)
                    if recursion_info["is_recursive"]:
                        confidence += 0.8
                        if recursion_info["is_direct"]:
                            evidence_parts.append("direct recursion detected")
                        else:
                            evidence_parts.append(f"indirect recursion: {' -> '.join(recursion_info['cycle_path'])}")
                elif pattern_name == "recursion":
                    if f"{symbol.name}(" in func_source:
                        count = func_source.count(f"{symbol.name}(")
                        if count > 1:
                            confidence += 0.3
                            evidence_parts.append("potential recursion")
                elif pattern_info["indicators"] and pattern_info["indicators"](func_source, symbol.name):
                    confidence += 0.4
                    evidence_parts.append("code structure matches pattern")
                
                if confidence >= 0.5:
                    patterns.append(Pattern(
                        pattern_type="algorithm",
                        pattern_name=pattern_name,
                        confidence=min(confidence, 1.0),
                        evidence=f"{symbol.name}: {'; '.join(evidence_parts)}"
                    ))
            
            # Check design patterns
            for pattern_name, pattern_info in DESIGN_PATTERNS.items():
                confidence = 0.0
                evidence_parts = []
                
                for kw in pattern_info["keywords"]:
                    if kw.lower() in symbol.name.lower() or kw.lower() in func_source_lower:
                        confidence += 0.3
                        evidence_parts.append(f"keyword '{kw}' found")
                
                if pattern_info["indicators"] and pattern_info["indicators"](func_source, symbol.name):
                    confidence += 0.5
                    evidence_parts.append("code structure matches pattern")
                
                if confidence >= 0.5:
                    patterns.append(Pattern(
                        pattern_type="design_pattern",
                        pattern_name=pattern_name,
                        confidence=min(confidence, 1.0),
                        evidence=f"{symbol.name}: {'; '.join(evidence_parts)}"
                    ))
        
        return patterns
    
    def _detect_recursion(
        self,
        symbol_name: str,
        call_graph: dict[str, set[str]],
        max_depth: int = 3
    ) -> dict:
        """Detect if a symbol is recursive using the call graph."""
        result = {"is_recursive": False, "is_direct": False, "cycle_path": []}
        
        if symbol_name not in call_graph:
            return result
        
        callees = call_graph.get(symbol_name, set())
        
        # Check direct recursion
        if symbol_name in callees:
            return {"is_recursive": True, "is_direct": True, "cycle_path": [symbol_name, symbol_name]}
        
        # Check indirect recursion
        visited: set[str] = {symbol_name}
        queue: list[tuple[str, list[str]]] = [(symbol_name, [symbol_name])]
        
        depth = 0
        while queue and depth < max_depth:
            next_queue: list[tuple[str, list[str]]] = []
            for current, path in queue:
                for callee in call_graph.get(current, set()):
                    if callee == symbol_name:
                        return {"is_recursive": True, "is_direct": False, "cycle_path": path + [callee]}
                    if callee not in visited and callee in call_graph:
                        visited.add(callee)
                        next_queue.append((callee, path + [callee]))
            queue = next_queue
            depth += 1
        
        return result
    
    def _extract_calls_from_symbols(
        self,
        symbols: list[Symbol],
        source: str,
        imports: list[Import]
    ) -> list[FunctionCall]:
        """Extract all function calls from the given symbols."""
        calls: list[FunctionCall] = []
        
        # Build imported names mapping
        imported_names: set[str] = set()
        for imp in imports:
            imported_names.add(imp.module.replace(".h", ""))
        
        # Build function names set
        function_names: set[str] = {s.name for s in symbols if s.type == "function"}
        
        lines = source.split("\n")
        
        for symbol in symbols:
            if symbol.type != "function":
                continue
            
            func_source = "\n".join(lines[symbol.start_line - 1:symbol.end_line])
            tree = self.parser.parse(bytes(func_source, "utf-8"))
            
            calls.extend(self._traverse_for_calls(
                tree.root_node,
                func_source,
                symbol.name,
                function_names,
                imported_names,
                symbol.start_line
            ))
        
        return calls
    
    def _traverse_for_calls(
        self,
        node: Node,
        source: str,
        caller_name: str,
        function_names: set[str],
        imported_names: set[str],
        line_offset: int
    ) -> list[FunctionCall]:
        """Traverse AST to find function calls."""
        calls: list[FunctionCall] = []
        
        if node.type == "call_expression":
            call = self._parse_call_expression(
                node, source, caller_name, function_names, imported_names, line_offset
            )
            if call:
                calls.append(call)
        
        for child in node.children:
            calls.extend(self._traverse_for_calls(
                child, source, caller_name, function_names, imported_names, line_offset
            ))
        
        return calls
    
    def _parse_call_expression(
        self,
        node: Node,
        source: str,
        caller_name: str,
        function_names: set[str],
        imported_names: set[str],
        line_offset: int
    ) -> FunctionCall | None:
        """Parse a function call expression."""
        func_node = self._get_child_by_type(node, ["identifier", "field_expression"])
        if not func_node:
            return None
        
        callee_name = self._node_text(func_node, source)
        line_number = line_offset + node.start_point[0]
        
        # Get arguments
        arguments: list[str] = []
        args_node = self._get_child_by_type(node, ["argument_list"])
        if args_node:
            for arg in args_node.children:
                if arg.type not in ("(", ")", ","):
                    arguments.append(self._node_text(arg, source))
        
        # Determine if external
        is_external = callee_name not in function_names
        
        # Determine call type
        call_type = "function"
        if func_node.type == "field_expression":
            call_type = "method"  # ptr->func() pattern
        
        return FunctionCall(
            caller_name=caller_name,
            callee_name=callee_name,
            call_type=call_type,
            line_number=line_number,
            is_external=is_external,
            module=None,
            arguments=arguments
        )
