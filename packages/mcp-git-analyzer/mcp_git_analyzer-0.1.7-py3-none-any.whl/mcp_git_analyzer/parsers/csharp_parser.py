"""C# code parser using Tree-sitter."""

from pathlib import Path

import tree_sitter_c_sharp as tscsharp
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


# Initialize C# parser
CSHARP_LANGUAGE = Language(tscsharp.language())
_parser = Parser(CSHARP_LANGUAGE)


# C# specific pattern indicators
ALGORITHM_PATTERNS = {
    **BASE_ALGORITHM_PATTERNS,
    "dynamic_programming": {
        **BASE_ALGORITHM_PATTERNS["dynamic_programming"],
        "indicators": lambda code, name: (
            "memo" in code.lower() or
            "cache" in code.lower() or
            "Dictionary<" in code or
            "dp[" in code
        )
    },
    "binary_search": {
        **BASE_ALGORITHM_PATTERNS["binary_search"],
        "indicators": lambda code, name: (
            "Array.BinarySearch" in code or
            "List.BinarySearch" in code or
            ("mid" in code and ("low" in code or "left" in code))
        )
    },
    "sorting": {
        **BASE_ALGORITHM_PATTERNS["sorting"],
        "indicators": lambda code, name: (
            ".Sort(" in code or
            ".OrderBy(" in code or
            ".OrderByDescending(" in code or
            "Array.Sort(" in code
        )
    },
    "linq_query": {
        "keywords": ["linq", "query", "select", "where", "from"],
        "indicators": lambda code, name: (
            "from " in code and " select " in code or
            ".Where(" in code or
            ".Select(" in code or
            ".GroupBy(" in code or
            ".Join(" in code
        )
    },
}

DESIGN_PATTERNS = {
    **BASE_DESIGN_PATTERNS,
    "singleton": {
        **BASE_DESIGN_PATTERNS["singleton"],
        "indicators": lambda code, name: (
            "private static" in code and
            ("Instance" in code or "instance" in code) and
            "private " in code  # private constructor
        )
    },
    "factory": {
        **BASE_DESIGN_PATTERNS["factory"],
        "indicators": lambda code, name: (
            ("Create" in name or "Factory" in name or "Make" in name) and
            "return new " in code
        )
    },
    "dependency_injection": {
        "keywords": ["inject", "dependency", "service", "IoC"],
        "indicators": lambda code, name: (
            "[Inject]" in code or
            "IServiceProvider" in code or
            "services.Add" in code or
            "IServiceCollection" in code
        )
    },
    "async_await": {
        "keywords": ["async", "await", "Task"],
        "indicators": lambda code, name: (
            "async " in code and
            ("await " in code or "Task" in code)
        )
    },
    "dispose_pattern": {
        "keywords": ["dispose", "IDisposable", "using"],
        "indicators": lambda code, name: (
            "IDisposable" in code or
            "Dispose(" in code or
            "protected virtual void Dispose" in code
        )
    },
    "observer": {
        **BASE_DESIGN_PATTERNS["observer"],
        "indicators": lambda code, name: (
            "event " in code or
            "EventHandler" in code or
            "+=" in code and "Handler" in code
        )
    },
    "repository": {
        "keywords": ["repository", "IRepository", "Repository"],
        "indicators": lambda code, name: (
            "Repository" in name or
            "IRepository" in code
        )
    },
    "unit_of_work": {
        "keywords": ["UnitOfWork", "IUnitOfWork", "SaveChanges"],
        "indicators": lambda code, name: (
            "UnitOfWork" in name or
            "SaveChanges" in code or
            "CommitAsync" in code
        )
    },
}


class CSharpParser(BaseParser):
    """Parse C# source code using Tree-sitter."""
    
    def __init__(self):
        self.parser = _parser
    
    @property
    def language(self) -> str:
        return "csharp"
    
    @property
    def file_extensions(self) -> list[str]:
        return [".cs"]
    
    def parse_file(self, file_path: Path) -> dict:
        """
        Parse a C# file and extract all symbols, imports, and patterns.
        
        Args:
            file_path: Path to the C# file
        
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
        Parse C# source code string.
        
        Args:
            source: C# source code
            file_name: Optional file name for context
            extract_calls: If True, extract function call graph
        
        Returns:
            Dict with symbols, imports, patterns, calls (if enabled), and metadata
        """
        tree = self.parser.parse(bytes(source, "utf-8"))
        root = tree.root_node
        
        symbols: list[Symbol] = []
        imports: list[Import] = []
        
        # Extract using directives
        imports.extend(self._extract_usings(root, source))
        
        # Process all declarations
        self._process_node(root, source, symbols, None, "")
        
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
    
    def _process_node(
        self,
        node: Node,
        source: str,
        symbols: list[Symbol],
        parent_name: str | None,
        namespace_prefix: str
    ):
        """Recursively process AST nodes."""
        for child in node.children:
            if child.type == "namespace_declaration":
                ns_name = self._extract_namespace_name(child, source)
                new_prefix = f"{namespace_prefix}{ns_name}." if ns_name else namespace_prefix
                # Process namespace body
                body = self._get_child_by_type(child, ["declaration_list"])
                if body:
                    self._process_node(body, source, symbols, None, new_prefix)
            elif child.type == "file_scoped_namespace_declaration":
                ns_name = self._extract_namespace_name(child, source)
                namespace_prefix = f"{ns_name}." if ns_name else ""
                # Continue processing at current level
                self._process_node(child, source, symbols, None, namespace_prefix)
            elif child.type == "class_declaration":
                class_symbol, members = self._extract_class(child, source, namespace_prefix)
                if class_symbol:
                    symbols.append(class_symbol)
                    symbols.extend(members)
            elif child.type == "struct_declaration":
                struct_symbol, members = self._extract_struct(child, source, namespace_prefix)
                if struct_symbol:
                    symbols.append(struct_symbol)
                    symbols.extend(members)
            elif child.type == "interface_declaration":
                interface_symbol, members = self._extract_interface(child, source, namespace_prefix)
                if interface_symbol:
                    symbols.append(interface_symbol)
                    symbols.extend(members)
            elif child.type == "enum_declaration":
                enum_symbol = self._extract_enum(child, source, namespace_prefix)
                if enum_symbol:
                    symbols.append(enum_symbol)
            elif child.type == "record_declaration":
                record_symbol, members = self._extract_record(child, source, namespace_prefix)
                if record_symbol:
                    symbols.append(record_symbol)
                    symbols.extend(members)
            elif child.type == "delegate_declaration":
                delegate_symbol = self._extract_delegate(child, source, namespace_prefix)
                if delegate_symbol:
                    symbols.append(delegate_symbol)
            elif child.type == "method_declaration":
                method = self._extract_method(child, source, parent_name)
                if method:
                    symbols.append(method)
            elif child.type == "global_statement":
                # Top-level statements (C# 9+)
                self._process_node(child, source, symbols, None, namespace_prefix)
            elif child.type == "local_function_statement":
                func = self._extract_local_function(child, source, parent_name)
                if func:
                    symbols.append(func)
    
    def _extract_usings(self, root: Node, source: str) -> list[Import]:
        """Extract using directives."""
        imports = []
        
        def find_usings(node: Node):
            for child in node.children:
                if child.type == "using_directive":
                    namespace = ""
                    alias = None
                    
                    # Check for using alias
                    name_equals = self._get_child_by_type(child, ["name_equals"])
                    if name_equals:
                        alias_node = self._get_child_by_type(name_equals, ["identifier"])
                        if alias_node:
                            alias = self._node_text(alias_node, source)
                    
                    # Get namespace
                    name_node = self._get_child_by_type(child, ["qualified_name", "identifier"])
                    if name_node:
                        namespace = self._node_text(name_node, source)
                    
                    # Check for static using
                    is_static = "static" in self._node_text(child, source)
                    
                    imports.append(Import(
                        module=namespace,
                        alias=alias,
                        imported_names=[namespace.split(".")[-1]] if namespace else [],
                        is_relative=False,
                        line_number=child.start_point[0] + 1,
                        import_type="csharp_static" if is_static else "csharp"
                    ))
                elif child.type in ("namespace_declaration", "file_scoped_namespace_declaration"):
                    find_usings(child)
        
        find_usings(root)
        return imports
    
    def _extract_namespace_name(self, node: Node, source: str) -> str:
        """Extract namespace name."""
        name_node = self._get_child_by_type(node, ["qualified_name", "identifier"])
        if name_node:
            return self._node_text(name_node, source)
        return ""
    
    def _extract_class(
        self,
        node: Node,
        source: str,
        namespace_prefix: str
    ) -> tuple[Symbol | None, list[Symbol]]:
        """Extract class declaration and its members."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None, []
        
        name = self._node_text(name_node, source)
        
        # Get modifiers
        modifiers = self._extract_modifiers(node, source)
        
        # Get generic type parameters
        type_params = self._extract_type_parameters(node, source)
        
        # Get base types
        base_types = self._extract_base_types(node, source)
        
        # Get attributes
        attributes = self._extract_attributes(node, source)
        
        # Build signature
        sig_parts = []
        if attributes:
            sig_parts.append(f"[{', '.join(attributes)}]")
        sig_parts.extend(modifiers)
        sig_parts.append("class")
        sig_parts.append(name)
        if type_params:
            sig_parts[-1] += f"<{', '.join(type_params)}>"
        if base_types:
            sig_parts.append(f": {', '.join(base_types)}")
        
        signature = " ".join(sig_parts)
        docstring = self._extract_xml_doc(node, source)
        
        class_symbol = Symbol(
            name=name,
            type="class",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parameters=[{"extends": base_types[0]}] if base_types else [],
            decorators=modifiers + attributes,
            generic_params=type_params,
            is_exported="public" in modifiers or "internal" in modifiers
        )
        
        # Extract members
        members = []
        body = self._get_child_by_type(node, ["declaration_list"])
        if body:
            self._extract_class_members(body, source, name, members)
        
        return class_symbol, members
    
    def _extract_struct(
        self,
        node: Node,
        source: str,
        namespace_prefix: str
    ) -> tuple[Symbol | None, list[Symbol]]:
        """Extract struct declaration."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None, []
        
        name = self._node_text(name_node, source)
        modifiers = self._extract_modifiers(node, source)
        type_params = self._extract_type_parameters(node, source)
        base_types = self._extract_base_types(node, source)
        attributes = self._extract_attributes(node, source)
        
        sig_parts = []
        if attributes:
            sig_parts.append(f"[{', '.join(attributes)}]")
        sig_parts.extend(modifiers)
        sig_parts.append("struct")
        sig_parts.append(name)
        if type_params:
            sig_parts[-1] += f"<{', '.join(type_params)}>"
        if base_types:
            sig_parts.append(f": {', '.join(base_types)}")
        
        signature = " ".join(sig_parts)
        docstring = self._extract_xml_doc(node, source)
        
        struct_symbol = Symbol(
            name=name,
            type="class",  # Treat struct as class
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            decorators=modifiers + attributes + ["struct"],
            generic_params=type_params,
            is_exported="public" in modifiers
        )
        
        members = []
        body = self._get_child_by_type(node, ["declaration_list"])
        if body:
            self._extract_class_members(body, source, name, members)
        
        return struct_symbol, members
    
    def _extract_interface(
        self,
        node: Node,
        source: str,
        namespace_prefix: str
    ) -> tuple[Symbol | None, list[Symbol]]:
        """Extract interface declaration."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None, []
        
        name = self._node_text(name_node, source)
        modifiers = self._extract_modifiers(node, source)
        type_params = self._extract_type_parameters(node, source)
        base_types = self._extract_base_types(node, source)
        attributes = self._extract_attributes(node, source)
        
        sig_parts = []
        if attributes:
            sig_parts.append(f"[{', '.join(attributes)}]")
        sig_parts.extend(modifiers)
        sig_parts.append("interface")
        sig_parts.append(name)
        if type_params:
            sig_parts[-1] += f"<{', '.join(type_params)}>"
        if base_types:
            sig_parts.append(f": {', '.join(base_types)}")
        
        signature = " ".join(sig_parts)
        docstring = self._extract_xml_doc(node, source)
        
        interface_symbol = Symbol(
            name=name,
            type="interface",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            decorators=modifiers + attributes,
            generic_params=type_params,
            is_exported="public" in modifiers
        )
        
        # Extract interface members (method signatures)
        members = []
        body = self._get_child_by_type(node, ["declaration_list"])
        if body:
            self._extract_interface_members(body, source, name, members)
        
        return interface_symbol, members
    
    def _extract_enum(self, node: Node, source: str, namespace_prefix: str) -> Symbol | None:
        """Extract enum declaration."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        modifiers = self._extract_modifiers(node, source)
        attributes = self._extract_attributes(node, source)
        
        sig_parts = []
        if attributes:
            sig_parts.append(f"[{', '.join(attributes)}]")
        sig_parts.extend(modifiers)
        sig_parts.append("enum")
        sig_parts.append(name)
        
        signature = " ".join(sig_parts)
        docstring = self._extract_xml_doc(node, source)
        
        return Symbol(
            name=name,
            type="class",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            decorators=modifiers + attributes + ["enum"],
            is_exported="public" in modifiers
        )
    
    def _extract_record(
        self,
        node: Node,
        source: str,
        namespace_prefix: str
    ) -> tuple[Symbol | None, list[Symbol]]:
        """Extract record declaration (C# 9+)."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None, []
        
        name = self._node_text(name_node, source)
        modifiers = self._extract_modifiers(node, source)
        type_params = self._extract_type_parameters(node, source)
        attributes = self._extract_attributes(node, source)
        
        # Get primary constructor parameters if any
        params_node = self._get_child_by_type(node, ["parameter_list"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        sig_parts = []
        if attributes:
            sig_parts.append(f"[{', '.join(attributes)}]")
        sig_parts.extend(modifiers)
        sig_parts.append("record")
        sig_parts.append(name)
        if type_params:
            sig_parts[-1] += f"<{', '.join(type_params)}>"
        if params_node:
            sig_parts.append(self._node_text(params_node, source))
        
        signature = " ".join(sig_parts)
        docstring = self._extract_xml_doc(node, source)
        
        record_symbol = Symbol(
            name=name,
            type="class",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parameters=parameters,
            decorators=modifiers + attributes + ["record"],
            generic_params=type_params,
            is_exported="public" in modifiers
        )
        
        members = []
        body = self._get_child_by_type(node, ["declaration_list"])
        if body:
            self._extract_class_members(body, source, name, members)
        
        return record_symbol, members
    
    def _extract_delegate(self, node: Node, source: str, namespace_prefix: str) -> Symbol | None:
        """Extract delegate declaration."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        modifiers = self._extract_modifiers(node, source)
        type_params = self._extract_type_parameters(node, source)
        
        # Get return type
        return_type = None
        for child in node.children:
            if child.type in ("predefined_type", "identifier", "generic_name", "nullable_type"):
                return_type = self._node_text(child, source)
                break
        
        params_node = self._get_child_by_type(node, ["parameter_list"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        sig_parts = modifiers + ["delegate"]
        if return_type:
            sig_parts.append(return_type)
        sig_parts.append(name)
        if type_params:
            sig_parts[-1] += f"<{', '.join(type_params)}>"
        sig_parts.append(self._node_text(params_node, source) if params_node else "()")
        
        signature = " ".join(sig_parts)
        docstring = self._extract_xml_doc(node, source)
        
        return Symbol(
            name=name,
            type="type_alias",  # Delegates are similar to type aliases
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parameters=parameters,
            return_type=return_type,
            decorators=modifiers + ["delegate"],
            generic_params=type_params,
            is_exported="public" in modifiers
        )
    
    def _extract_class_members(
        self,
        body: Node,
        source: str,
        parent_name: str,
        members: list[Symbol]
    ):
        """Extract members from class/struct body."""
        for child in body.children:
            if child.type == "method_declaration":
                method = self._extract_method(child, source, parent_name)
                if method:
                    members.append(method)
            elif child.type == "constructor_declaration":
                ctor = self._extract_constructor(child, source, parent_name)
                if ctor:
                    members.append(ctor)
            elif child.type == "property_declaration":
                prop = self._extract_property(child, source, parent_name)
                if prop:
                    members.append(prop)
            elif child.type == "event_declaration":
                event = self._extract_event(child, source, parent_name)
                if event:
                    members.append(event)
            elif child.type == "indexer_declaration":
                indexer = self._extract_indexer(child, source, parent_name)
                if indexer:
                    members.append(indexer)
            elif child.type == "operator_declaration":
                op = self._extract_operator(child, source, parent_name)
                if op:
                    members.append(op)
    
    def _extract_interface_members(
        self,
        body: Node,
        source: str,
        parent_name: str,
        members: list[Symbol]
    ):
        """Extract members from interface body."""
        for child in body.children:
            if child.type == "method_declaration":
                method = self._extract_method(child, source, parent_name)
                if method:
                    members.append(method)
            elif child.type == "property_declaration":
                prop = self._extract_property(child, source, parent_name)
                if prop:
                    members.append(prop)
            elif child.type == "event_declaration":
                event = self._extract_event(child, source, parent_name)
                if event:
                    members.append(event)
    
    def _extract_method(self, node: Node, source: str, parent_name: str | None) -> Symbol | None:
        """Extract method declaration."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        modifiers = self._extract_modifiers(node, source)
        type_params = self._extract_type_parameters(node, source)
        attributes = self._extract_attributes(node, source)
        
        # Get return type
        return_type = None
        for child in node.children:
            if child.type in ("predefined_type", "identifier", "generic_name", 
                              "nullable_type", "array_type", "tuple_type"):
                return_type = self._node_text(child, source)
                break
        
        params_node = self._get_child_by_type(node, ["parameter_list"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        # Build signature
        sig_parts = []
        if attributes:
            sig_parts.append(f"[{', '.join(attributes)}]")
        sig_parts.extend(modifiers)
        if return_type:
            sig_parts.append(return_type)
        sig_parts.append(name)
        if type_params:
            sig_parts[-1] += f"<{', '.join(type_params)}>"
        sig_parts.append(self._node_text(params_node, source) if params_node else "()")
        
        signature = " ".join(sig_parts)
        docstring = self._extract_xml_doc(node, source)
        
        is_async = "async" in modifiers
        
        return Symbol(
            name=name,
            type="method",
            signature=signature.strip(),
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            parameters=parameters,
            return_type=return_type,
            decorators=modifiers + attributes,
            generic_params=type_params,
            is_async=is_async,
            is_exported="public" in modifiers
        )
    
    def _extract_constructor(self, node: Node, source: str, parent_name: str) -> Symbol | None:
        """Extract constructor declaration."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        modifiers = self._extract_modifiers(node, source)
        attributes = self._extract_attributes(node, source)
        
        params_node = self._get_child_by_type(node, ["parameter_list"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        sig_parts = []
        if attributes:
            sig_parts.append(f"[{', '.join(attributes)}]")
        sig_parts.extend(modifiers)
        sig_parts.append(name)
        sig_parts.append(self._node_text(params_node, source) if params_node else "()")
        
        signature = " ".join(sig_parts)
        docstring = self._extract_xml_doc(node, source)
        
        return Symbol(
            name=name,
            type="method",
            signature=signature.strip(),
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            parameters=parameters,
            decorators=modifiers + attributes + ["constructor"],
            is_exported="public" in modifiers
        )
    
    def _extract_property(self, node: Node, source: str, parent_name: str | None) -> Symbol | None:
        """Extract property declaration."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        modifiers = self._extract_modifiers(node, source)
        attributes = self._extract_attributes(node, source)
        
        # Get property type
        prop_type = None
        for child in node.children:
            if child.type in ("predefined_type", "identifier", "generic_name", 
                              "nullable_type", "array_type"):
                prop_type = self._node_text(child, source)
                break
        
        # Check accessors
        accessors = []
        accessor_list = self._get_child_by_type(node, ["accessor_list"])
        if accessor_list:
            for acc in accessor_list.children:
                if acc.type == "accessor_declaration":
                    acc_text = self._node_text(acc, source)
                    if "get" in acc_text:
                        accessors.append("get")
                    if "set" in acc_text:
                        accessors.append("set")
                    if "init" in acc_text:
                        accessors.append("init")
        
        sig_parts = []
        if attributes:
            sig_parts.append(f"[{', '.join(attributes)}]")
        sig_parts.extend(modifiers)
        if prop_type:
            sig_parts.append(prop_type)
        sig_parts.append(name)
        if accessors:
            sig_parts.append(f"{{ {'; '.join(accessors)}; }}")
        
        signature = " ".join(sig_parts)
        docstring = self._extract_xml_doc(node, source)
        
        return Symbol(
            name=name,
            type="method",  # Treat as method for consistency
            signature=signature.strip(),
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            return_type=prop_type,
            decorators=modifiers + attributes + ["property"],
            is_exported="public" in modifiers
        )
    
    def _extract_event(self, node: Node, source: str, parent_name: str | None) -> Symbol | None:
        """Extract event declaration."""
        # Find variable declarator for event name
        var_decl = self._get_child_by_type(node, ["variable_declaration"])
        if var_decl:
            name_node = self._get_child_by_type(var_decl, ["variable_declarator"])
            if name_node:
                id_node = self._get_child_by_type(name_node, ["identifier"])
                if id_node:
                    name = self._node_text(id_node, source)
                else:
                    return None
            else:
                return None
        else:
            return None
        
        modifiers = self._extract_modifiers(node, source)
        
        signature = self._node_text(node, source).strip().rstrip(";")
        docstring = self._extract_xml_doc(node, source)
        
        return Symbol(
            name=name,
            type="method",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            decorators=modifiers + ["event"],
            is_exported="public" in modifiers
        )
    
    def _extract_indexer(self, node: Node, source: str, parent_name: str | None) -> Symbol | None:
        """Extract indexer declaration."""
        modifiers = self._extract_modifiers(node, source)
        
        # Get return type
        return_type = None
        for child in node.children:
            if child.type in ("predefined_type", "identifier", "generic_name"):
                return_type = self._node_text(child, source)
                break
        
        params_node = self._get_child_by_type(node, ["bracketed_parameter_list"])
        
        sig_parts = modifiers.copy()
        if return_type:
            sig_parts.append(return_type)
        sig_parts.append("this")
        sig_parts.append(self._node_text(params_node, source) if params_node else "[]")
        
        signature = " ".join(sig_parts)
        docstring = self._extract_xml_doc(node, source)
        
        return Symbol(
            name="this",
            type="method",
            signature=signature.strip(),
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            return_type=return_type,
            decorators=modifiers + ["indexer"],
            is_exported="public" in modifiers
        )
    
    def _extract_operator(self, node: Node, source: str, parent_name: str) -> Symbol | None:
        """Extract operator declaration."""
        modifiers = self._extract_modifiers(node, source)
        
        # Get operator symbol
        op_text = self._node_text(node, source)
        
        signature = " ".join(modifiers) + " " + op_text.split("{")[0].strip()
        
        return Symbol(
            name="operator",
            type="method",
            signature=signature.strip(),
            docstring=None,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            decorators=modifiers + ["operator"],
            is_exported="public" in modifiers
        )
    
    def _extract_local_function(self, node: Node, source: str, parent_name: str | None) -> Symbol | None:
        """Extract local function (C# 7+)."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        modifiers = self._extract_modifiers(node, source)
        
        return_type = None
        for child in node.children:
            if child.type in ("predefined_type", "identifier", "generic_name"):
                return_type = self._node_text(child, source)
                break
        
        params_node = self._get_child_by_type(node, ["parameter_list"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        sig_parts = modifiers.copy()
        if return_type:
            sig_parts.append(return_type)
        sig_parts.append(name)
        sig_parts.append(self._node_text(params_node, source) if params_node else "()")
        
        signature = " ".join(sig_parts)
        
        return Symbol(
            name=name,
            type="function",
            signature=signature.strip(),
            docstring=None,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            parameters=parameters,
            return_type=return_type,
            decorators=modifiers + ["local"],
            is_async="async" in modifiers,
            is_exported=False
        )
    
    def _extract_modifiers(self, node: Node, source: str) -> list[str]:
        """Extract modifiers from declaration."""
        modifiers = []
        modifier_keywords = {
            "public", "private", "protected", "internal", "static", "readonly",
            "const", "volatile", "virtual", "override", "abstract", "sealed",
            "extern", "new", "async", "partial", "unsafe", "ref", "required"
        }
        
        for child in node.children:
            if child.type == "modifier":
                mod_text = self._node_text(child, source)
                if mod_text in modifier_keywords:
                    modifiers.append(mod_text)
        
        return modifiers
    
    def _extract_type_parameters(self, node: Node, source: str) -> list[str]:
        """Extract generic type parameters."""
        params = []
        type_params = self._get_child_by_type(node, ["type_parameter_list"])
        if type_params:
            for child in type_params.children:
                if child.type == "type_parameter":
                    params.append(self._node_text(child, source))
        return params
    
    def _extract_base_types(self, node: Node, source: str) -> list[str]:
        """Extract base types (inheritance)."""
        bases = []
        base_list = self._get_child_by_type(node, ["base_list"])
        if base_list:
            for child in base_list.children:
                if child.type in ("identifier", "generic_name", "qualified_name"):
                    bases.append(self._node_text(child, source))
                elif child.type == "simple_base_type":
                    bases.append(self._node_text(child, source))
        return bases
    
    def _extract_attributes(self, node: Node, source: str) -> list[str]:
        """Extract attributes."""
        attributes = []
        for child in node.children:
            if child.type == "attribute_list":
                for attr in child.children:
                    if attr.type == "attribute":
                        attributes.append(self._node_text(attr, source))
        return attributes
    
    def _extract_parameters(self, params_node: Node, source: str) -> list[dict]:
        """Extract method parameters."""
        parameters = []
        
        for child in params_node.children:
            if child.type == "parameter":
                param = {"name": "", "type": None, "modifier": None, "default": None}
                
                # Get modifiers (ref, out, in, params)
                for mod in child.children:
                    if mod.type == "parameter_modifier":
                        param["modifier"] = self._node_text(mod, source)
                
                # Get type
                for type_child in child.children:
                    if type_child.type in ("predefined_type", "identifier", "generic_name",
                                           "nullable_type", "array_type", "tuple_type"):
                        param["type"] = self._node_text(type_child, source)
                        break
                
                # Get name
                name_node = self._get_child_by_type(child, ["identifier"])
                if name_node:
                    param["name"] = self._node_text(name_node, source)
                
                # Get default value
                equals_value = self._get_child_by_type(child, ["equals_value_clause"])
                if equals_value:
                    param["default"] = self._node_text(equals_value, source).lstrip("= ")
                
                if param["name"] or param["type"]:
                    parameters.append(param)
        
        return parameters
    
    def _extract_xml_doc(self, node: Node, source: str) -> str | None:
        """Extract XML documentation comments (///)."""
        lines = source[:node.start_byte].split('\n')
        
        doc_lines = []
        for line in reversed(lines):
            stripped = line.strip()
            if stripped.startswith("///"):
                doc_lines.insert(0, stripped[3:].strip())
            elif stripped and not stripped.startswith("//"):
                break
        
        if doc_lines:
            doc = "\n".join(doc_lines)
            # Simple XML stripping
            import re
            doc = re.sub(r'<[^>]+>', '', doc)
            return doc.strip() if doc.strip() else None
        
        return None
    
    def _detect_patterns(
        self,
        symbols: list[Symbol],
        source: str,
        calls: list[FunctionCall] | None = None
    ) -> list[Pattern]:
        """Detect patterns in the code."""
        patterns = []
        
        call_graph: dict[str, set[str]] = {}
        if calls:
            for call in calls:
                if call.caller_name not in call_graph:
                    call_graph[call.caller_name] = set()
                call_graph[call.caller_name].add(call.callee_name)
        
        for symbol in symbols:
            if symbol.type not in ("method", "function"):
                continue
            
            symbol_full_name = f"{symbol.parent_name}.{symbol.name}" if symbol.parent_name else symbol.name
            
            lines = source.split("\n")
            method_source = "\n".join(lines[symbol.start_line - 1:symbol.end_line])
            method_source_lower = method_source.lower()
            
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
                    if f"{symbol.name}(" in method_source:
                        count = method_source.count(f"{symbol.name}(")
                        if count > 1:
                            confidence += 0.3
                            evidence_parts.append("potential recursion")
                elif pattern_info["indicators"] and pattern_info["indicators"](method_source, symbol.name):
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
                    if kw.lower() in symbol.name.lower() or kw.lower() in method_source_lower:
                        confidence += 0.3
                        evidence_parts.append(f"keyword '{kw}' found")
                
                if pattern_info["indicators"] and pattern_info["indicators"](method_source, symbol.name):
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
    
    def _detect_recursion(
        self,
        symbol_name: str,
        call_graph: dict[str, set[str]],
        max_depth: int = 3
    ) -> dict:
        """Detect recursion."""
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
        """Extract function calls."""
        calls: list[FunctionCall] = []
        
        method_names: set[str] = set()
        class_methods: dict[str, set[str]] = {}
        
        for s in symbols:
            if s.type == "function":
                method_names.add(s.name)
            elif s.type == "method" and s.parent_name:
                if s.parent_name not in class_methods:
                    class_methods[s.parent_name] = set()
                class_methods[s.parent_name].add(s.name)
        
        lines = source.split("\n")
        
        for symbol in symbols:
            if symbol.type not in ("method", "function"):
                continue
            
            method_source = "\n".join(lines[symbol.start_line - 1:symbol.end_line])
            tree = self.parser.parse(bytes(method_source, "utf-8"))
            
            caller_name = f"{symbol.parent_name}.{symbol.name}" if symbol.parent_name else symbol.name
            
            calls.extend(self._traverse_for_calls(
                tree.root_node,
                method_source,
                caller_name,
                method_names,
                class_methods,
                symbol.start_line
            ))
        
        return calls
    
    def _traverse_for_calls(
        self,
        node: Node,
        source: str,
        caller_name: str,
        method_names: set[str],
        class_methods: dict[str, set[str]],
        line_offset: int
    ) -> list[FunctionCall]:
        """Traverse AST for calls."""
        calls: list[FunctionCall] = []
        
        if node.type == "invocation_expression":
            call = self._parse_invocation(
                node, source, caller_name, method_names, class_methods, line_offset
            )
            if call:
                calls.append(call)
        elif node.type == "object_creation_expression":
            call = self._parse_object_creation(
                node, source, caller_name, line_offset
            )
            if call:
                calls.append(call)
        
        for child in node.children:
            calls.extend(self._traverse_for_calls(
                child, source, caller_name, method_names, class_methods, line_offset
            ))
        
        return calls
    
    def _parse_invocation(
        self,
        node: Node,
        source: str,
        caller_name: str,
        method_names: set[str],
        class_methods: dict[str, set[str]],
        line_offset: int
    ) -> FunctionCall | None:
        """Parse invocation expression."""
        # Get the function/method being called
        func_node = None
        for child in node.children:
            if child.type in ("identifier", "member_access_expression", "generic_name"):
                func_node = child
                break
        
        if not func_node:
            return None
        
        callee_name = self._node_text(func_node, source)
        line_number = line_offset + node.start_point[0]
        
        arguments: list[str] = []
        args_node = self._get_child_by_type(node, ["argument_list"])
        if args_node:
            for arg in args_node.children:
                if arg.type == "argument":
                    arguments.append(self._node_text(arg, source))
        
        # Determine call type and if external
        call_type = "method" if "." in callee_name else "function"
        simple_name = callee_name.split(".")[-1] if "." in callee_name else callee_name
        
        is_external = simple_name not in method_names
        for methods in class_methods.values():
            if simple_name in methods:
                is_external = False
                break
        
        # Check for await
        is_async_call = False
        parent = node.parent
        while parent:
            if parent.type == "await_expression":
                is_async_call = True
                break
            parent = parent.parent
        
        return FunctionCall(
            caller_name=caller_name,
            callee_name=callee_name,
            call_type=call_type,
            line_number=line_number,
            is_external=is_external,
            arguments=arguments,
            is_async_call=is_async_call
        )
    
    def _parse_object_creation(
        self,
        node: Node,
        source: str,
        caller_name: str,
        line_offset: int
    ) -> FunctionCall | None:
        """Parse object creation (new) expression."""
        type_node = self._get_child_by_type(node, ["identifier", "generic_name", "qualified_name"])
        if not type_node:
            return None
        
        type_name = self._node_text(type_node, source)
        line_number = line_offset + node.start_point[0]
        
        arguments: list[str] = []
        args_node = self._get_child_by_type(node, ["argument_list"])
        if args_node:
            for arg in args_node.children:
                if arg.type == "argument":
                    arguments.append(self._node_text(arg, source))
        
        return FunctionCall(
            caller_name=caller_name,
            callee_name=f"new {type_name}",
            call_type="constructor",
            line_number=line_number,
            is_external=True,  # Constructors are typically external
            arguments=arguments
        )
