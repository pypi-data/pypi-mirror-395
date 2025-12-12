"""C++ code parser using Tree-sitter."""

from pathlib import Path

import tree_sitter_cpp as tscpp
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


# Initialize C++ parser
CPP_LANGUAGE = Language(tscpp.language())
_parser = Parser(CPP_LANGUAGE)


# C++ specific pattern indicators
ALGORITHM_PATTERNS = {
    **BASE_ALGORITHM_PATTERNS,
    "dynamic_programming": {
        **BASE_ALGORITHM_PATTERNS["dynamic_programming"],
        "indicators": lambda code, name: (
            "memo" in code.lower() or
            "cache" in code.lower() or
            "dp[" in code or
            "std::map" in code or
            "std::unordered_map" in code
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
            ("std::lower_bound" in code or "std::upper_bound" in code) or
            ("mid" in code and ("low" in code or "left" in code))
        )
    },
    "sorting": {
        **BASE_ALGORITHM_PATTERNS["sorting"],
        "indicators": lambda code, name: (
            "std::sort(" in code or
            "std::stable_sort(" in code or
            "std::partial_sort(" in code
        )
    },
    "graph_traversal": {
        **BASE_ALGORITHM_PATTERNS["graph_traversal"],
        "indicators": lambda code, name: (
            ("std::queue" in code or "std::stack" in code) and
            "visited" in code.lower()
        )
    },
    "iterator_pattern": {
        "keywords": ["iterator", "begin", "end", "iter"],
        "indicators": lambda code, name: (
            ".begin()" in code or
            ".end()" in code or
            "std::begin" in code
        )
    },
}

DESIGN_PATTERNS = {
    **BASE_DESIGN_PATTERNS,
    "singleton": {
        **BASE_DESIGN_PATTERNS["singleton"],
        "indicators": lambda code, name: (
            "static" in code and
            ("instance" in code.lower() or "getInstance" in code) and
            "private" in code
        )
    },
    "factory": {
        **BASE_DESIGN_PATTERNS["factory"],
        "indicators": lambda code, name: (
            ("create" in name.lower() or "make" in name.lower() or "Factory" in name) and
            ("std::unique_ptr" in code or "std::shared_ptr" in code or "new " in code)
        )
    },
    "raii": {
        "keywords": ["raii", "resource", "guard", "lock", "scope"],
        "indicators": lambda code, name: (
            ("~" in code and name in code) or  # Destructor
            "std::lock_guard" in code or
            "std::unique_lock" in code or
            "std::scoped_lock" in code
        )
    },
    "smart_pointer": {
        "keywords": ["unique_ptr", "shared_ptr", "weak_ptr", "make_unique", "make_shared"],
        "indicators": lambda code, name: (
            "std::unique_ptr" in code or
            "std::shared_ptr" in code or
            "std::weak_ptr" in code or
            "std::make_unique" in code or
            "std::make_shared" in code
        )
    },
    "pimpl": {
        "keywords": ["pimpl", "impl", "private", "implementation"],
        "indicators": lambda code, name: (
            "class Impl" in code or
            "struct Impl" in code or
            "std::unique_ptr<Impl>" in code
        )
    },
    "observer": {
        **BASE_DESIGN_PATTERNS["observer"],
        "indicators": lambda code, name: (
            "subscribe" in code.lower() or
            "notify" in code.lower() or
            "listener" in code.lower() or
            "callback" in code.lower()
        )
    },
    "crtp": {
        "keywords": ["crtp", "static_polymorphism", "curiously_recurring"],
        "indicators": lambda code, name: (
            "template" in code and
            ": public" in code and
            "<" in code and ">" in code and
            name in code  # Class name appears in template parameter
        )
    },
}

# C++ version feature patterns
CPP_VERSION_PATTERNS = {
    "cpp11": [
        ("auto ", "auto type deduction"),
        ("nullptr", "nullptr"),
        ("constexpr", "constexpr"),
        ("override", "override specifier"),
        ("final", "final specifier"),
        ("noexcept", "noexcept"),
        ("static_assert", "static_assert"),
        ("std::thread", "std::thread"),
        ("std::mutex", "std::mutex"),
        ("std::unique_ptr", "unique_ptr"),
        ("std::shared_ptr", "shared_ptr"),
        ("std::move(", "std::move"),
        ("std::forward", "std::forward"),
        ("std::array", "std::array"),
        ("std::unordered_map", "unordered containers"),
        ("lambda", "lambda (detected)"),
    ],
    "cpp14": [
        ("decltype(auto)", "decltype(auto)"),
        ("std::make_unique", "make_unique"),
        ("'s", "digit separator (C++14)"),  # e.g., 1'000'000
    ],
    "cpp17": [
        ("if constexpr", "if constexpr"),
        ("std::optional", "std::optional"),
        ("std::variant", "std::variant"),
        ("std::any", "std::any"),
        ("std::string_view", "string_view"),
        ("std::filesystem", "std::filesystem"),
        ("[[nodiscard]]", "nodiscard attribute"),
        ("[[maybe_unused]]", "maybe_unused attribute"),
        ("[[fallthrough]]", "fallthrough attribute"),
        ("structured binding", "structured binding (detected)"),
    ],
    "cpp20": [
        ("concept ", "concepts"),
        ("requires", "requires clause"),
        ("co_await", "coroutines"),
        ("co_yield", "coroutines"),
        ("co_return", "coroutines"),
        ("std::span", "std::span"),
        ("std::ranges", "ranges"),
        ("[[likely]]", "likely attribute"),
        ("[[unlikely]]", "unlikely attribute"),
        ("<=>", "spaceship operator"),
        ("consteval", "consteval"),
        ("constinit", "constinit"),
    ],
    "cpp23": [
        ("std::expected", "std::expected"),
        ("std::print", "std::print"),
        ("import ", "modules"),
        ("export ", "modules"),
    ],
}


class CppParser(BaseParser):
    """Parse C++ source code using Tree-sitter."""
    
    def __init__(self):
        self.parser = _parser
    
    @property
    def language(self) -> str:
        return "cpp"
    
    @property
    def file_extensions(self) -> list[str]:
        return [".cpp", ".hpp", ".cc", ".cxx", ".hxx", ".h++", ".hh", ".c++"]
    
    def parse_file(self, file_path: Path) -> dict:
        """
        Parse a C++ file and extract all symbols, imports, and patterns.
        
        Args:
            file_path: Path to the C++ file
        
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
        Parse C++ source code string.
        
        Args:
            source: C++ source code
            file_name: Optional file name for context
            extract_calls: If True, extract function call graph
        
        Returns:
            Dict with symbols, imports, patterns, calls (if enabled), and metadata
        """
        tree = self.parser.parse(bytes(source, "utf-8"))
        root = tree.root_node
        
        symbols: list[Symbol] = []
        imports: list[Import] = []
        
        # Extract includes and using directives
        imports.extend(self._extract_imports(root, source))
        
        # Process top-level declarations
        self._process_node(root, source, symbols, None)
        
        # Detect patterns
        calls: list[FunctionCall] = []
        if extract_calls:
            calls = self._extract_calls_from_symbols(symbols, source, imports)
        
        patterns = self._detect_patterns(symbols, source, calls if extract_calls else None)
        
        # Add C++ version detection patterns
        version_patterns = self._detect_cpp_version(source)
        patterns.extend(version_patterns)
        
        return self._create_parse_result(
            file_name=file_name,
            source=source,
            symbols=symbols,
            imports=imports,
            patterns=patterns,
            calls=calls if extract_calls else None
        )
    
    def _process_node(
        self,
        node: Node,
        source: str,
        symbols: list[Symbol],
        parent_name: str | None,
        namespace_prefix: str = ""
    ):
        """Recursively process AST nodes to extract symbols."""
        for child in node.children:
            if child.type == "function_definition":
                func = self._extract_function(child, source, parent_name, namespace_prefix)
                if func:
                    symbols.append(func)
            elif child.type == "declaration":
                decl_symbols = self._extract_declaration(child, source, parent_name, namespace_prefix)
                symbols.extend(decl_symbols)
            elif child.type == "class_specifier":
                class_symbol, methods = self._extract_class(child, source, namespace_prefix)
                if class_symbol:
                    symbols.append(class_symbol)
                    symbols.extend(methods)
            elif child.type == "struct_specifier":
                struct_symbol, methods = self._extract_struct(child, source, namespace_prefix)
                if struct_symbol:
                    symbols.append(struct_symbol)
                    symbols.extend(methods)
            elif child.type == "enum_specifier":
                enum = self._extract_enum(child, source, namespace_prefix)
                if enum:
                    symbols.append(enum)
            elif child.type == "namespace_definition":
                ns_name = self._extract_namespace_name(child, source)
                new_prefix = f"{namespace_prefix}{ns_name}::" if ns_name else namespace_prefix
                # Process namespace body
                body = self._get_child_by_type(child, ["declaration_list"])
                if body:
                    self._process_node(body, source, symbols, None, new_prefix)
            elif child.type == "template_declaration":
                # Process the templated entity
                self._process_template(child, source, symbols, parent_name, namespace_prefix)
            elif child.type == "type_alias_declaration" or child.type == "alias_declaration":
                alias = self._extract_type_alias(child, source, namespace_prefix)
                if alias:
                    symbols.append(alias)
    
    def _extract_imports(self, root: Node, source: str) -> list[Import]:
        """Extract #include directives and using declarations."""
        imports = []
        
        for child in root.children:
            if child.type == "preproc_include":
                path_node = self._get_child_by_type(child, ["system_lib_string", "string_literal"])
                if path_node:
                    header = self._node_text(path_node, source)
                    is_system = header.startswith("<")
                    header_name = header.strip('<>"')
                    
                    imports.append(Import(
                        module=header_name,
                        alias=None,
                        imported_names=[header_name.split("/")[-1].replace(".h", "").replace(".hpp", "")],
                        is_relative=not is_system,
                        line_number=child.start_point[0] + 1,
                        import_type="cpp_include"
                    ))
            elif child.type == "using_declaration":
                # using std::cout;
                name = self._node_text(child, source).replace("using ", "").rstrip(";").strip()
                imports.append(Import(
                    module=name.rsplit("::", 1)[0] if "::" in name else "",
                    alias=None,
                    imported_names=[name.rsplit("::", 1)[-1]],
                    is_relative=False,
                    line_number=child.start_point[0] + 1,
                    import_type="cpp_using"
                ))
            elif child.type == "namespace_alias_definition":
                # namespace fs = std::filesystem;
                text = self._node_text(child, source)
                imports.append(Import(
                    module=text,
                    alias=None,
                    imported_names=[],
                    is_relative=False,
                    line_number=child.start_point[0] + 1,
                    import_type="cpp_namespace_alias"
                ))
        
        return imports
    
    def _extract_function(
        self,
        node: Node,
        source: str,
        parent_name: str | None,
        namespace_prefix: str = ""
    ) -> Symbol | None:
        """Extract function definition."""
        declarator = self._get_child_by_type(node, ["function_declarator"])
        if not declarator:
            # Check for pointer declarator
            ptr_decl = self._get_child_by_type(node, ["pointer_declarator", "reference_declarator"])
            if ptr_decl:
                declarator = self._get_child_by_type(ptr_decl, ["function_declarator"])
        
        if not declarator:
            return None
        
        # Get function name (may be qualified)
        name_node = self._get_child_by_type(declarator, ["identifier", "qualified_identifier",
                                                          "destructor_name", "operator_name",
                                                          "template_function"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Handle qualified names (ClassName::methodName)
        if "::" in name and not parent_name:
            parts = name.rsplit("::", 1)
            parent_name = parts[0]
            name = parts[1]
        
        # Get return type
        return_type = self._extract_return_type(node, source)
        
        # Get parameters
        params_node = self._get_child_by_type(declarator, ["parameter_list"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        # Get template parameters if any
        template_params = self._extract_template_params_from_parent(node, source)
        
        # Get specifiers
        specifiers = self._extract_specifiers(node, source)
        
        # Build signature
        sig_parts = []
        if template_params:
            sig_parts.append(f"template<{', '.join(template_params)}>")
        if "virtual" in specifiers:
            sig_parts.append("virtual")
        if "static" in specifiers:
            sig_parts.append("static")
        if "inline" in specifiers:
            sig_parts.append("inline")
        if "constexpr" in specifiers:
            sig_parts.append("constexpr")
        if return_type:
            sig_parts.append(return_type)
        
        full_name = f"{namespace_prefix}{name}" if namespace_prefix and not parent_name else name
        params_str = self._node_text(params_node, source) if params_node else "()"
        sig_parts.append(f"{full_name}{params_str}")
        
        if "const" in specifiers:
            sig_parts.append("const")
        if "noexcept" in specifiers:
            sig_parts.append("noexcept")
        if "override" in specifiers:
            sig_parts.append("override")
        if "final" in specifiers:
            sig_parts.append("final")
        
        signature = " ".join(sig_parts)
        
        docstring = self._extract_doc_comment(node, source)
        
        symbol_type = "method" if parent_name else "function"
        
        return Symbol(
            name=name,
            type=symbol_type,
            signature=signature.strip(),
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            parameters=parameters,
            return_type=return_type,
            decorators=specifiers,
            generic_params=template_params,
            is_exported="static" not in specifiers
        )
    
    def _extract_declaration(
        self,
        node: Node,
        source: str,
        parent_name: str | None,
        namespace_prefix: str = ""
    ) -> list[Symbol]:
        """Extract various declarations."""
        symbols = []
        
        # Check for function declaration (prototype)
        func_decl = self._get_child_by_type(node, ["function_declarator"])
        if func_decl:
            proto = self._extract_function_prototype(node, source, parent_name, namespace_prefix)
            if proto:
                symbols.append(proto)
            return symbols
        
        # Check for class/struct forward declaration
        class_spec = self._get_child_by_type(node, ["class_specifier"])
        if class_spec:
            cls, methods = self._extract_class(class_spec, source, namespace_prefix)
            if cls:
                symbols.append(cls)
                symbols.extend(methods)
            return symbols
        
        struct_spec = self._get_child_by_type(node, ["struct_specifier"])
        if struct_spec:
            struct, methods = self._extract_struct(struct_spec, source, namespace_prefix)
            if struct:
                symbols.append(struct)
                symbols.extend(methods)
            return symbols
        
        enum_spec = self._get_child_by_type(node, ["enum_specifier"])
        if enum_spec:
            enum = self._extract_enum(enum_spec, source, namespace_prefix)
            if enum:
                symbols.append(enum)
        
        return symbols
    
    def _extract_function_prototype(
        self,
        node: Node,
        source: str,
        parent_name: str | None,
        namespace_prefix: str = ""
    ) -> Symbol | None:
        """Extract function prototype."""
        func_decl = self._get_child_by_type(node, ["function_declarator"])
        if not func_decl:
            return None
        
        name_node = self._get_child_by_type(func_decl, ["identifier", "qualified_identifier",
                                                         "destructor_name", "operator_name"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        return_type = self._extract_return_type(node, source)
        
        params_node = self._get_child_by_type(func_decl, ["parameter_list"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        specifiers = self._extract_specifiers(node, source)
        
        params_str = self._node_text(params_node, source) if params_node else "()"
        sig_parts = []
        if "virtual" in specifiers:
            sig_parts.append("virtual")
        if return_type:
            sig_parts.append(return_type)
        sig_parts.append(f"{name}{params_str}")
        
        signature = " ".join(sig_parts)
        docstring = self._extract_doc_comment(node, source)
        
        symbol_type = "method" if parent_name else "function"
        
        return Symbol(
            name=name,
            type=symbol_type,
            signature=signature.strip(),
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            parameters=parameters,
            return_type=return_type,
            decorators=specifiers,
            is_exported="static" not in specifiers
        )
    
    def _extract_class(
        self,
        node: Node,
        source: str,
        namespace_prefix: str = ""
    ) -> tuple[Symbol | None, list[Symbol]]:
        """Extract class definition and its members."""
        name_node = self._get_child_by_type(node, ["type_identifier", "template_type"])
        if not name_node:
            return None, []
        
        name = self._node_text(name_node, source)
        full_name = f"{namespace_prefix}{name}" if namespace_prefix else name
        
        # Check for template parameters
        template_params = self._extract_template_params_from_parent(node, source)
        
        # Get base classes
        base_classes = self._extract_base_classes(node, source)
        
        # Build signature
        sig_parts = ["class", full_name]
        if template_params:
            sig_parts.insert(0, f"template<{', '.join(template_params)}>")
        if base_classes:
            sig_parts.append(f": {', '.join(base_classes)}")
        
        signature = " ".join(sig_parts)
        docstring = self._extract_doc_comment(node, source)
        
        # Extract methods and fields
        methods = []
        fields = []
        body = self._get_child_by_type(node, ["field_declaration_list"])
        if body:
            current_access = "private"  # Default for class
            for child in body.children:
                if child.type == "access_specifier":
                    current_access = self._node_text(child, source).rstrip(":")
                elif child.type == "function_definition":
                    method = self._extract_function(child, source, name, "")
                    if method:
                        if current_access not in method.decorators:
                            method.decorators.append(current_access)
                        methods.append(method)
                elif child.type == "declaration":
                    decl_symbols = self._extract_declaration(child, source, name, "")
                    for sym in decl_symbols:
                        if sym.type in ("function", "method"):
                            if current_access not in sym.decorators:
                                sym.decorators.append(current_access)
                    methods.extend(decl_symbols)
                elif child.type == "template_declaration":
                    self._process_template(child, source, methods, name, "")
                elif child.type == "field_declaration":
                    field_info = self._extract_class_field(child, source, current_access)
                    if field_info:
                        fields.append(field_info)
        
        class_symbol = Symbol(
            name=name,
            type="class",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parameters=[{"extends": base_classes[0]}] if base_classes else [],
            generic_params=template_params,
            is_exported=True,
            fields=fields
        )
        
        return class_symbol, methods
    
    def _extract_struct(
        self,
        node: Node,
        source: str,
        namespace_prefix: str = ""
    ) -> tuple[Symbol | None, list[Symbol]]:
        """Extract struct definition and its members."""
        name_node = self._get_child_by_type(node, ["type_identifier", "template_type"])
        if not name_node:
            return None, []
        
        name = self._node_text(name_node, source)
        full_name = f"{namespace_prefix}{name}" if namespace_prefix else name
        
        template_params = self._extract_template_params_from_parent(node, source)
        base_classes = self._extract_base_classes(node, source)
        
        sig_parts = ["struct", full_name]
        if template_params:
            sig_parts.insert(0, f"template<{', '.join(template_params)}>")
        if base_classes:
            sig_parts.append(f": {', '.join(base_classes)}")
        
        signature = " ".join(sig_parts)
        docstring = self._extract_doc_comment(node, source)
        
        methods = []
        fields = []
        body = self._get_child_by_type(node, ["field_declaration_list"])
        if body:
            current_access = "public"  # Default for struct
            for child in body.children:
                if child.type == "access_specifier":
                    current_access = self._node_text(child, source).rstrip(":")
                elif child.type == "function_definition":
                    method = self._extract_function(child, source, name, "")
                    if method:
                        if current_access not in method.decorators:
                            method.decorators.append(current_access)
                        methods.append(method)
                elif child.type == "declaration":
                    decl_symbols = self._extract_declaration(child, source, name, "")
                    for sym in decl_symbols:
                        if sym.type in ("function", "method"):
                            if current_access not in sym.decorators:
                                sym.decorators.append(current_access)
                    methods.extend(decl_symbols)
                elif child.type == "field_declaration":
                    field_info = self._extract_class_field(child, source, current_access)
                    if field_info:
                        fields.append(field_info)
        
        struct_symbol = Symbol(
            name=name,
            type="class",  # Treat struct as class
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            generic_params=template_params,
            is_exported=True,
            fields=fields
        )
        
        return struct_symbol, methods
    
    def _extract_class_field(self, node: Node, source: str, visibility: str = "public") -> dict | None:
        """Extract a single class/struct field with name, type, and visibility."""
        # Skip function declarations in field_declaration
        if self._get_child_by_type(node, ["function_declarator"]):
            return None
        
        # Get the type
        type_parts = []
        for child in node.children:
            if child.type in ["primitive_type", "type_identifier", "sized_type_specifier", 
                              "qualified_identifier", "template_type"]:
                type_parts.append(self._node_text(child, source))
            elif child.type == "struct_specifier":
                struct_name = self._get_child_by_type(child, ["type_identifier"])
                if struct_name:
                    type_parts.append(f"struct {self._node_text(struct_name, source)}")
            elif child.type == "class_specifier":
                class_name = self._get_child_by_type(child, ["type_identifier"])
                if class_name:
                    type_parts.append(f"class {self._node_text(class_name, source)}")
        
        field_type = " ".join(type_parts) if type_parts else "unknown"
        
        # Handle const, static, etc.
        text = self._node_text(node, source)
        if "const " in text and "const" not in field_type:
            field_type = "const " + field_type
        if "static " in text:
            field_type = "static " + field_type
        
        # Get field declarator (name and possible pointer/reference)
        declarator = self._get_child_by_type(node, ["field_identifier"])
        pointer_declarator = self._get_child_by_type(node, ["pointer_declarator"])
        reference_declarator = self._get_child_by_type(node, ["reference_declarator"])
        array_declarator = self._get_child_by_type(node, ["array_declarator"])
        init_declarator = self._get_child_by_type(node, ["init_declarator"])
        
        field_name = None
        
        if init_declarator:
            # Handle initialized fields: int x = 5;
            inner_ident = self._get_child_by_type(init_declarator, ["field_identifier", "identifier"])
            if inner_ident:
                field_name = self._node_text(inner_ident, source)
        elif pointer_declarator:
            # Handle pointer fields: int* ptr;
            field_name_node = self._get_child_by_type(pointer_declarator, ["field_identifier", "identifier"])
            if field_name_node:
                field_name = self._node_text(field_name_node, source)
                ptr_count = self._node_text(pointer_declarator, source).count("*")
                field_type = field_type + "*" * ptr_count
        elif reference_declarator:
            # Handle reference fields: int& ref;
            field_name_node = self._get_child_by_type(reference_declarator, ["field_identifier", "identifier"])
            if field_name_node:
                field_name = self._node_text(field_name_node, source)
                field_type = field_type + "&"
        elif array_declarator:
            # Handle array fields: int arr[10];
            field_name_node = self._get_child_by_type(array_declarator, ["field_identifier", "identifier"])
            if field_name_node:
                field_name = self._node_text(field_name_node, source)
                size_node = self._get_child_by_type(array_declarator, ["number_literal"])
                if size_node:
                    field_type = f"{field_type}[{self._node_text(size_node, source)}]"
                else:
                    field_type = f"{field_type}[]"
        elif declarator:
            field_name = self._node_text(declarator, source)
        
        if not field_name:
            return None
        
        return {
            "name": field_name,
            "type": field_type,
            "visibility": visibility
        }
    
    def _extract_enum(self, node: Node, source: str, namespace_prefix: str = "") -> Symbol | None:
        """Extract enum definition."""
        name_node = self._get_child_by_type(node, ["type_identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Check for enum class
        text = self._node_text(node, source)
        is_enum_class = "enum class" in text or "enum struct" in text
        
        signature = f"enum class {name}" if is_enum_class else f"enum {name}"
        docstring = self._extract_doc_comment(node, source)
        
        return Symbol(
            name=name,
            type="class",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            decorators=["enum_class"] if is_enum_class else ["enum"],
            is_exported=True
        )
    
    def _extract_namespace_name(self, node: Node, source: str) -> str:
        """Extract namespace name."""
        name_node = self._get_child_by_type(node, ["identifier", "namespace_identifier"])
        if name_node:
            return self._node_text(name_node, source)
        return ""
    
    def _extract_type_alias(
        self,
        node: Node,
        source: str,
        namespace_prefix: str = ""
    ) -> Symbol | None:
        """Extract using type alias."""
        text = self._node_text(node, source)
        
        # using MyType = SomeType;
        name_node = self._get_child_by_type(node, ["type_identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
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
    
    def _process_template(
        self,
        node: Node,
        source: str,
        symbols: list[Symbol],
        parent_name: str | None,
        namespace_prefix: str
    ):
        """Process template declaration."""
        # Find the templated entity
        for child in node.children:
            if child.type == "function_definition":
                func = self._extract_function(child, source, parent_name, namespace_prefix)
                if func:
                    # Add template parameters
                    template_params = self._extract_template_params(node, source)
                    func.generic_params = template_params
                    symbols.append(func)
            elif child.type == "declaration":
                decl_symbols = self._extract_declaration(child, source, parent_name, namespace_prefix)
                template_params = self._extract_template_params(node, source)
                for sym in decl_symbols:
                    sym.generic_params = template_params
                symbols.extend(decl_symbols)
            elif child.type == "class_specifier":
                cls, methods = self._extract_class(child, source, namespace_prefix)
                if cls:
                    template_params = self._extract_template_params(node, source)
                    cls.generic_params = template_params
                    symbols.append(cls)
                    symbols.extend(methods)
            elif child.type == "struct_specifier":
                struct, methods = self._extract_struct(child, source, namespace_prefix)
                if struct:
                    template_params = self._extract_template_params(node, source)
                    struct.generic_params = template_params
                    symbols.append(struct)
                    symbols.extend(methods)
    
    def _extract_template_params(self, node: Node, source: str) -> list[str]:
        """Extract template parameters from template declaration."""
        params = []
        param_list = self._get_child_by_type(node, ["template_parameter_list"])
        if param_list:
            for child in param_list.children:
                if child.type in ("type_parameter_declaration", "parameter_declaration",
                                  "variadic_type_parameter_declaration",
                                  "optional_type_parameter_declaration"):
                    params.append(self._node_text(child, source))
        return params
    
    def _extract_template_params_from_parent(self, node: Node, source: str) -> list[str]:
        """Check if parent is template and extract params."""
        # Look backwards in source for template<...>
        start_byte = node.start_byte
        prefix = source[max(0, start_byte - 200):start_byte]
        
        import re
        match = re.search(r'template\s*<([^>]+)>\s*$', prefix)
        if match:
            return [p.strip() for p in match.group(1).split(',')]
        return []
    
    def _extract_base_classes(self, node: Node, source: str) -> list[str]:
        """Extract base class specifications."""
        bases = []
        base_clause = self._get_child_by_type(node, ["base_class_clause"])
        if base_clause:
            for child in base_clause.children:
                if child.type == "base_class_specifier":
                    bases.append(self._node_text(child, source))
        return bases
    
    def _extract_return_type(self, node: Node, source: str) -> str | None:
        """Extract return type from function."""
        for child in node.children:
            if child.type in ("primitive_type", "type_identifier", "sized_type_specifier",
                              "template_type", "qualified_identifier", "auto"):
                return self._node_text(child, source)
            elif child.type == "placeholder_type_specifier":
                return self._node_text(child, source)  # auto, decltype(auto)
        return None
    
    def _extract_parameters(self, params_node: Node, source: str) -> list[dict]:
        """Extract function parameters."""
        parameters = []
        
        for child in params_node.children:
            if child.type in ("parameter_declaration", "optional_parameter_declaration"):
                param = {"name": "", "type": None, "default": None}
                
                # Get type
                for type_child in child.children:
                    if type_child.type in ("primitive_type", "type_identifier", "template_type",
                                           "qualified_identifier", "auto", "placeholder_type_specifier"):
                        param["type"] = self._node_text(type_child, source)
                        break
                
                # Get name
                declarator = self._get_child_by_type(child, ["identifier", "pointer_declarator",
                                                             "reference_declarator"])
                if declarator:
                    if declarator.type in ("pointer_declarator", "reference_declarator"):
                        id_node = self._get_child_by_type(declarator, ["identifier"])
                        if id_node:
                            param["name"] = self._node_text(id_node, source)
                    else:
                        param["name"] = self._node_text(declarator, source)
                
                # Get default value for optional parameters
                if child.type == "optional_parameter_declaration":
                    default_node = self._get_child_by_type(child, ["number_literal", "string_literal",
                                                                   "true", "false", "nullptr"])
                    if default_node:
                        param["default"] = self._node_text(default_node, source)
                
                if param["name"] or param["type"]:
                    parameters.append(param)
            elif child.type == "variadic_parameter_declaration":
                parameters.append({"name": "...", "type": "variadic"})
        
        return parameters
    
    def _extract_specifiers(self, node: Node, source: str) -> list[str]:
        """Extract function specifiers (virtual, static, const, etc.)."""
        specifiers = []
        text = self._node_text(node, source)
        
        keyword_specifiers = ["virtual", "static", "inline", "constexpr", "consteval",
                              "explicit", "friend", "extern"]
        for spec in keyword_specifiers:
            if f" {spec} " in f" {text} " or text.startswith(f"{spec} "):
                specifiers.append(spec)
        
        # Check for trailing specifiers
        if ") const" in text:
            specifiers.append("const")
        if "noexcept" in text:
            specifiers.append("noexcept")
        if "override" in text:
            specifiers.append("override")
        if "final" in text:
            specifiers.append("final")
        if "= 0" in text or "=0" in text:
            specifiers.append("pure_virtual")
        if "= default" in text:
            specifiers.append("default")
        if "= delete" in text:
            specifiers.append("deleted")
        
        return specifiers
    
    def _extract_doc_comment(self, node: Node, source: str) -> str | None:
        """Extract documentation comment (Doxygen style)."""
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
                    return None
            elif stripped.startswith("///") or stripped.startswith("//!"):
                doc_lines.insert(0, stripped)
            elif stripped and not in_block and not stripped.startswith("//"):
                break
        
        if doc_lines:
            if doc_lines[0].startswith("/**") or doc_lines[0].startswith("/*!"):
                doc = "\n".join(doc_lines)
                doc = doc.replace("/**", "").replace("/*!", "").replace("*/", "").strip()
                doc = "\n".join(line.lstrip(" *").strip() for line in doc.split("\n"))
                return doc.strip() if doc.strip() else None
            elif doc_lines[0].startswith("///") or doc_lines[0].startswith("//!"):
                doc = "\n".join(line.lstrip("/!").strip() for line in doc_lines)
                return doc.strip() if doc.strip() else None
        
        return None
    
    def _detect_patterns(
        self,
        symbols: list[Symbol],
        source: str,
        calls: list[FunctionCall] | None = None
    ) -> list[Pattern]:
        """Detect algorithmic and design patterns."""
        patterns = []
        
        call_graph: dict[str, set[str]] = {}
        if calls:
            for call in calls:
                if call.caller_name not in call_graph:
                    call_graph[call.caller_name] = set()
                call_graph[call.caller_name].add(call.callee_name)
        
        for symbol in symbols:
            if symbol.type not in ("function", "method"):
                continue
            
            symbol_full_name = f"{symbol.parent_name}::{symbol.name}" if symbol.parent_name else symbol.name
            
            lines = source.split("\n")
            func_source = "\n".join(lines[symbol.start_line - 1:symbol.end_line])
            func_source_lower = func_source.lower()
            
            for pattern_name, pattern_info in ALGORITHM_PATTERNS.items():
                confidence = 0.0
                evidence_parts = []
                
                for kw in pattern_info["keywords"]:
                    if kw in symbol.name.lower():
                        confidence += 0.5
                        evidence_parts.append(f"keyword '{kw}' in name")
                    if symbol.docstring and kw in symbol.docstring.lower():
                        confidence += 0.3
                        evidence_parts.append(f"keyword '{kw}' in doc")
                
                if pattern_name == "recursion" and call_graph:
                    recursion_info = self._detect_recursion(symbol_full_name, call_graph)
                    if recursion_info["is_recursive"]:
                        confidence += 0.8
                        evidence_parts.append("recursion detected")
                elif pattern_name == "recursion":
                    if f"{symbol.name}(" in func_source:
                        count = func_source.count(f"{symbol.name}(")
                        if count > 1:
                            confidence += 0.3
                            evidence_parts.append("potential recursion")
                elif pattern_info["indicators"] and pattern_info["indicators"](func_source, symbol.name):
                    confidence += 0.4
                    evidence_parts.append("code structure matches")
                
                if confidence >= 0.5:
                    patterns.append(Pattern(
                        pattern_type="algorithm",
                        pattern_name=pattern_name,
                        confidence=min(confidence, 1.0),
                        evidence=f"{symbol.name}: {'; '.join(evidence_parts)}"
                    ))
            
            for pattern_name, pattern_info in DESIGN_PATTERNS.items():
                confidence = 0.0
                evidence_parts = []
                
                for kw in pattern_info["keywords"]:
                    if kw.lower() in symbol.name.lower() or kw.lower() in func_source_lower:
                        confidence += 0.3
                        evidence_parts.append(f"keyword '{kw}' found")
                
                if pattern_info["indicators"] and pattern_info["indicators"](func_source, symbol.name):
                    confidence += 0.5
                    evidence_parts.append("code structure matches")
                
                if confidence >= 0.5:
                    patterns.append(Pattern(
                        pattern_type="design_pattern",
                        pattern_name=pattern_name,
                        confidence=min(confidence, 1.0),
                        evidence=f"{symbol.name}: {'; '.join(evidence_parts)}"
                    ))
        
        return patterns
    
    def _detect_cpp_version(self, source: str) -> list[Pattern]:
        """Detect C++ version features used in the code."""
        patterns = []
        detected_versions: dict[str, list[str]] = {}
        
        for version, features in CPP_VERSION_PATTERNS.items():
            found_features = []
            for pattern, description in features:
                if pattern in source:
                    found_features.append(description)
            if found_features:
                detected_versions[version] = found_features
        
        # Create patterns for detected versions
        for version, features in detected_versions.items():
            if len(features) >= 2:  # Only report if multiple features found
                patterns.append(Pattern(
                    pattern_type="cpp_version",
                    pattern_name=version,
                    confidence=min(0.5 + len(features) * 0.1, 1.0),
                    evidence=f"Features: {', '.join(features[:5])}"  # Limit evidence length
                ))
        
        return patterns
    
    def _detect_recursion(
        self,
        symbol_name: str,
        call_graph: dict[str, set[str]],
        max_depth: int = 3
    ) -> dict:
        """Detect recursion using call graph."""
        result = {"is_recursive": False, "is_direct": False, "cycle_path": []}
        
        if symbol_name not in call_graph:
            return result
        
        callees = call_graph.get(symbol_name, set())
        
        if symbol_name in callees:
            return {"is_recursive": True, "is_direct": True, "cycle_path": [symbol_name]}
        
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
        """Extract function calls from symbols."""
        calls: list[FunctionCall] = []
        
        function_names: set[str] = set()
        method_map: dict[str, set[str]] = {}
        
        for s in symbols:
            if s.type == "function":
                function_names.add(s.name)
            elif s.type == "method" and s.parent_name:
                if s.parent_name not in method_map:
                    method_map[s.parent_name] = set()
                method_map[s.parent_name].add(s.name)
        
        lines = source.split("\n")
        
        for symbol in symbols:
            if symbol.type not in ("function", "method"):
                continue
            
            func_source = "\n".join(lines[symbol.start_line - 1:symbol.end_line])
            tree = self.parser.parse(bytes(func_source, "utf-8"))
            
            caller_name = f"{symbol.parent_name}::{symbol.name}" if symbol.parent_name else symbol.name
            
            calls.extend(self._traverse_for_calls(
                tree.root_node,
                func_source,
                caller_name,
                function_names,
                method_map,
                symbol.start_line
            ))
        
        return calls
    
    def _traverse_for_calls(
        self,
        node: Node,
        source: str,
        caller_name: str,
        function_names: set[str],
        method_map: dict[str, set[str]],
        line_offset: int
    ) -> list[FunctionCall]:
        """Traverse AST to find function calls."""
        calls: list[FunctionCall] = []
        
        if node.type == "call_expression":
            call = self._parse_call_expression(
                node, source, caller_name, function_names, method_map, line_offset
            )
            if call:
                calls.append(call)
        
        for child in node.children:
            calls.extend(self._traverse_for_calls(
                child, source, caller_name, function_names, method_map, line_offset
            ))
        
        return calls
    
    def _parse_call_expression(
        self,
        node: Node,
        source: str,
        caller_name: str,
        function_names: set[str],
        method_map: dict[str, set[str]],
        line_offset: int
    ) -> FunctionCall | None:
        """Parse a call expression."""
        func_node = self._get_child_by_type(node, ["identifier", "qualified_identifier",
                                                    "field_expression", "template_function"])
        if not func_node:
            return None
        
        callee_name = self._node_text(func_node, source)
        line_number = line_offset + node.start_point[0]
        
        arguments: list[str] = []
        args_node = self._get_child_by_type(node, ["argument_list"])
        if args_node:
            for arg in args_node.children:
                if arg.type not in ("(", ")", ","):
                    arguments.append(self._node_text(arg, source))
        
        # Determine call type
        call_type = "function"
        is_external = True
        
        if func_node.type == "field_expression":
            call_type = "method"
        elif func_node.type == "qualified_identifier":
            # Could be static method or namespaced function
            if "::" in callee_name:
                call_type = "method"
        
        # Check if internal
        simple_name = callee_name.split("::")[-1] if "::" in callee_name else callee_name
        if simple_name in function_names:
            is_external = False
        for methods in method_map.values():
            if simple_name in methods:
                is_external = False
                break
        
        return FunctionCall(
            caller_name=caller_name,
            callee_name=callee_name,
            call_type=call_type,
            line_number=line_number,
            is_external=is_external,
            arguments=arguments
        )
