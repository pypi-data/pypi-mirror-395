"""Java code parser using Tree-sitter."""

from pathlib import Path

import tree_sitter_java as tsjava
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


# Initialize Java parser
JAVA_LANGUAGE = Language(tsjava.language())
_parser = Parser(JAVA_LANGUAGE)


# Java-specific pattern indicators (extending base patterns)
ALGORITHM_PATTERNS = {
    **BASE_ALGORITHM_PATTERNS,
    "dynamic_programming": {
        **BASE_ALGORITHM_PATTERNS["dynamic_programming"],
        "indicators": lambda code, name: "memo" in code.lower() or "cache" in code.lower() or "dp[" in code
    },
    "divide_and_conquer": {
        **BASE_ALGORITHM_PATTERNS["divide_and_conquer"],
        "indicators": lambda code, name: ("left" in code and "right" in code) or "mid" in code
    },
    "binary_search": {
        **BASE_ALGORITHM_PATTERNS["binary_search"],
        "indicators": lambda code, name: "mid" in code and ("low" in code or "left" in code) and ("high" in code or "right" in code)
    },
    "sorting": {
        **BASE_ALGORITHM_PATTERNS["sorting"],
        "indicators": lambda code, name: "Arrays.sort(" in code or "Collections.sort(" in code or ".sort(" in code
    },
    "graph_traversal": {
        **BASE_ALGORITHM_PATTERNS["graph_traversal"],
        "indicators": lambda code, name: ("Queue" in code or "Stack" in code) and "visited" in code.lower()
    },
    "greedy": {
        **BASE_ALGORITHM_PATTERNS["greedy"],
        "indicators": lambda code, name: "Math.max(" in code or "Math.min(" in code
    },
    "backtracking": {
        **BASE_ALGORITHM_PATTERNS["backtracking"],
        "indicators": lambda code, name: "undo" in code.lower() or "restore" in code.lower() or "backtrack" in code.lower()
    },
}

DESIGN_PATTERNS = {
    **BASE_DESIGN_PATTERNS,
    "singleton": {
        **BASE_DESIGN_PATTERNS["singleton"],
        "indicators": lambda code, name: "private static" in code and "getInstance" in code
    },
    "factory": {
        **BASE_DESIGN_PATTERNS["factory"],
        "indicators": lambda code, name: "create" in name.lower() or "Factory" in name
    },
    "builder": {
        "keywords": ["builder", "build", "Builder"],
        "indicators": lambda code, name: "Builder" in name or (".build()" in code and "return this" in code)
    },
    "observer": {
        **BASE_DESIGN_PATTERNS["observer"],
        "indicators": lambda code, name: "addListener" in code or "removeListener" in code or "notify" in code
    },
    "strategy": {
        **BASE_DESIGN_PATTERNS["strategy"],
        "indicators": lambda code, name: "Strategy" in name or "interface" in code
    },
    "dependency_injection": {
        "keywords": ["inject", "autowired", "Inject", "Autowired"],
        "indicators": lambda code, name: "@Inject" in code or "@Autowired" in code
    },
}


class JavaParser(BaseParser):
    """Parse Java source code using Tree-sitter."""
    
    def __init__(self):
        self.parser = _parser
    
    @property
    def language(self) -> str:
        return "java"
    
    @property
    def file_extensions(self) -> list[str]:
        return [".java"]
    
    def parse_file(self, file_path: Path) -> dict:
        """
        Parse a Java file and extract all symbols, imports, and patterns.
        
        Args:
            file_path: Path to the Java file
        
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
        Parse Java source code string.
        
        Args:
            source: Java source code
            file_name: Optional file name for context
            extract_calls: If True, extract function call graph
        
        Returns:
            Dict with symbols, imports, patterns, calls (if enabled), and metadata
        """
        tree = self.parser.parse(bytes(source, "utf-8"))
        root = tree.root_node
        
        symbols: list[Symbol] = []
        imports: list[Import] = []
        
        # Extract package and imports
        imports.extend(self._extract_imports(root, source))
        
        # Extract classes and interfaces
        for child in root.children:
            if child.type == "class_declaration":
                class_symbol, methods = self._extract_class(child, source)
                if class_symbol:
                    symbols.append(class_symbol)
                    symbols.extend(methods)
            elif child.type == "interface_declaration":
                interface_symbol, methods = self._extract_interface(child, source)
                if interface_symbol:
                    symbols.append(interface_symbol)
                    symbols.extend(methods)
            elif child.type == "enum_declaration":
                enum_symbol = self._extract_enum(child, source)
                if enum_symbol:
                    symbols.append(enum_symbol)
        
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
    
    def _extract_imports(self, root: Node, source: str) -> list[Import]:
        """Extract all import statements."""
        imports = []
        
        for child in root.children:
            if child.type == "import_declaration":
                # import com.example.ClassName;
                # import com.example.*;
                scoped_id = self._get_child_by_type(child, ["scoped_identifier"])
                if scoped_id:
                    module = self._node_text(scoped_id, source)
                    is_wildcard = "*" in self._node_text(child, source)
                    
                    # Split into package and class
                    parts = module.rsplit(".", 1)
                    package = parts[0] if len(parts) > 1 else ""
                    class_name = parts[-1] if not is_wildcard else "*"
                    
                    imports.append(Import(
                        module=package,
                        alias=None,
                        imported_names=[class_name],
                        is_relative=False,
                        line_number=child.start_point[0] + 1,
                        import_type="java"
                    ))
                else:
                    # Simple identifier import
                    identifier = self._get_child_by_type(child, ["identifier"])
                    if identifier:
                        imports.append(Import(
                            module="",
                            alias=None,
                            imported_names=[self._node_text(identifier, source)],
                            is_relative=False,
                            line_number=child.start_point[0] + 1,
                            import_type="java"
                        ))
        
        return imports
    
    def _extract_class(self, node: Node, source: str,
                       decorators: list[str] | None = None) -> tuple[Symbol | None, list[Symbol]]:
        """Extract class definition and its methods."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None, []
        
        name = self._node_text(name_node, source)
        
        # Get modifiers (public, private, abstract, etc.)
        modifiers = self._extract_modifiers(node, source)
        
        # Get generic type parameters
        type_params = self._extract_type_parameters(node, source)
        
        # Get superclass
        superclass = None
        superclass_node = self._get_child_by_type(node, ["superclass"])
        if superclass_node:
            type_node = self._get_child_by_type(superclass_node, ["type_identifier", "generic_type"])
            if type_node:
                superclass = self._node_text(type_node, source)
        
        # Get interfaces
        interfaces = []
        interfaces_node = self._get_child_by_type(node, ["super_interfaces"])
        if interfaces_node:
            for type_node in self._get_children_by_type(interfaces_node, ["type_identifier", "generic_type"]):
                interfaces.append(self._node_text(type_node, source))
        
        # Build signature
        signature = " ".join(modifiers) + " class " + name
        if type_params:
            signature += f"<{', '.join(type_params)}>"
        if superclass:
            signature += f" extends {superclass}"
        if interfaces:
            signature += f" implements {', '.join(interfaces)}"
        
        # Get Javadoc
        docstring = self._extract_javadoc(node, source)
        
        class_symbol = Symbol(
            name=name,
            type="class",
            signature=signature.strip(),
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=None,
            parameters=[{"extends": superclass}] if superclass else [],
            decorators=decorators or [],
            generic_params=type_params,
            is_exported="public" in modifiers
        )
        
        # Extract methods and fields
        methods = []
        body = self._get_child_by_type(node, ["class_body"])
        if body:
            for child in body.children:
                if child.type == "method_declaration":
                    method = self._extract_method(child, source, name)
                    if method:
                        methods.append(method)
                elif child.type == "constructor_declaration":
                    constructor = self._extract_constructor(child, source, name)
                    if constructor:
                        methods.append(constructor)
        
        return class_symbol, methods
    
    def _extract_interface(self, node: Node, source: str) -> tuple[Symbol | None, list[Symbol]]:
        """Extract interface definition and its method signatures."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None, []
        
        name = self._node_text(name_node, source)
        modifiers = self._extract_modifiers(node, source)
        type_params = self._extract_type_parameters(node, source)
        
        # Get extended interfaces
        extends = []
        extends_node = self._get_child_by_type(node, ["extends_interfaces"])
        if extends_node:
            for type_node in self._get_children_by_type(extends_node, ["type_identifier", "generic_type"]):
                extends.append(self._node_text(type_node, source))
        
        signature = " ".join(modifiers) + " interface " + name
        if type_params:
            signature += f"<{', '.join(type_params)}>"
        if extends:
            signature += f" extends {', '.join(extends)}"
        
        docstring = self._extract_javadoc(node, source)
        
        interface_symbol = Symbol(
            name=name,
            type="interface",
            signature=signature.strip(),
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=None,
            generic_params=type_params,
            is_exported="public" in modifiers
        )
        
        # Extract method signatures
        methods = []
        body = self._get_child_by_type(node, ["interface_body"])
        if body:
            for child in body.children:
                if child.type == "method_declaration":
                    method = self._extract_method(child, source, name)
                    if method:
                        methods.append(method)
        
        return interface_symbol, methods
    
    def _extract_enum(self, node: Node, source: str) -> Symbol | None:
        """Extract enum definition."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        modifiers = self._extract_modifiers(node, source)
        
        signature = " ".join(modifiers) + " enum " + name
        docstring = self._extract_javadoc(node, source)
        
        return Symbol(
            name=name,
            type="class",  # Treat enum as a special class
            signature=signature.strip(),
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            is_exported="public" in modifiers
        )
    
    def _extract_method(self, node: Node, source: str, parent_name: str) -> Symbol | None:
        """Extract method definition."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        modifiers = self._extract_modifiers(node, source)
        type_params = self._extract_type_parameters(node, source)
        
        # Get return type
        return_type = None
        for child in node.children:
            if child.type in ("type_identifier", "generic_type", "void_type", 
                              "integral_type", "floating_point_type", "boolean_type", "array_type"):
                return_type = self._node_text(child, source)
                break
        
        # Get parameters
        params_node = self._get_child_by_type(node, ["formal_parameters"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        # Build signature
        sig_parts = modifiers.copy()
        if type_params:
            sig_parts.append(f"<{', '.join(type_params)}>")
        if return_type:
            sig_parts.append(return_type)
        sig_parts.append(name)
        
        params_str = self._node_text(params_node, source) if params_node else "()"
        signature = " ".join(sig_parts) + params_str
        
        docstring = self._extract_javadoc(node, source)
        
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
            decorators=modifiers,
            generic_params=type_params,
            is_exported="public" in modifiers
        )
    
    def _extract_constructor(self, node: Node, source: str, parent_name: str) -> Symbol | None:
        """Extract constructor definition."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        modifiers = self._extract_modifiers(node, source)
        
        params_node = self._get_child_by_type(node, ["formal_parameters"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        params_str = self._node_text(params_node, source) if params_node else "()"
        signature = " ".join(modifiers) + " " + name + params_str
        
        docstring = self._extract_javadoc(node, source)
        
        return Symbol(
            name=name,
            type="method",
            signature=signature.strip(),
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            parameters=parameters,
            decorators=modifiers,
            is_exported="public" in modifiers
        )
    
    def _extract_modifiers(self, node: Node, source: str) -> list[str]:
        """Extract modifiers (public, private, static, etc.)."""
        modifiers = []
        for child in node.children:
            if child.type == "modifiers":
                for mod in child.children:
                    if mod.type in ("public", "private", "protected", "static", 
                                    "final", "abstract", "synchronized", "native",
                                    "strictfp", "transient", "volatile", "default"):
                        modifiers.append(mod.type)
                    elif mod.type == "marker_annotation" or mod.type == "annotation":
                        modifiers.append(self._node_text(mod, source))
        return modifiers
    
    def _extract_type_parameters(self, node: Node, source: str) -> list[str]:
        """Extract generic type parameters."""
        params = []
        type_params_node = self._get_child_by_type(node, ["type_parameters"])
        if type_params_node:
            for child in type_params_node.children:
                if child.type == "type_parameter":
                    params.append(self._node_text(child, source))
        return params
    
    def _extract_parameters(self, params_node: Node, source: str) -> list[dict]:
        """Extract method parameters with types."""
        parameters = []
        
        for child in params_node.children:
            if child.type == "formal_parameter" or child.type == "spread_parameter":
                param = {"name": "", "type": None}
                
                # Get type
                for type_child in child.children:
                    if type_child.type in ("type_identifier", "generic_type", 
                                           "integral_type", "floating_point_type",
                                           "boolean_type", "array_type"):
                        param["type"] = self._node_text(type_child, source)
                        break
                
                # Get name
                name_node = self._get_child_by_type(child, ["identifier"])
                if name_node:
                    param["name"] = self._node_text(name_node, source)
                
                if child.type == "spread_parameter":
                    param["name"] = "..." + param["name"]
                
                if param["name"]:
                    parameters.append(param)
        
        return parameters
    
    def _extract_javadoc(self, node: Node, source: str) -> str | None:
        """Extract Javadoc comment before a declaration."""
        # Look for block_comment that starts with /** before the node
        lines = source[:node.start_byte].split('\n')
        
        # Search backwards for Javadoc
        javadoc_lines = []
        in_javadoc = False
        
        for line in reversed(lines):
            stripped = line.strip()
            if stripped.endswith("*/"):
                in_javadoc = True
                javadoc_lines.insert(0, stripped)
            elif in_javadoc:
                javadoc_lines.insert(0, stripped)
                if stripped.startswith("/**"):
                    break
                elif stripped.startswith("/*"):
                    # Regular comment, not Javadoc
                    return None
            elif stripped and not in_javadoc:
                # Hit non-empty line before finding Javadoc
                break
        
        if javadoc_lines and javadoc_lines[0].startswith("/**"):
            # Clean up Javadoc
            doc = "\n".join(javadoc_lines)
            doc = doc.replace("/**", "").replace("*/", "").strip()
            doc = "\n".join(line.lstrip(" *").strip() for line in doc.split("\n"))
            return doc.strip() if doc.strip() else None
        
        return None
    
    def _detect_patterns(
        self,
        symbols: list[Symbol],
        source: str,
        calls: list[FunctionCall] | None = None
    ) -> list[Pattern]:
        """Detect algorithmic patterns in code."""
        patterns = []
        
        # Build call graph lookup for recursion detection
        call_graph: dict[str, set[str]] = {}
        if calls:
            for call in calls:
                if call.caller_name not in call_graph:
                    call_graph[call.caller_name] = set()
                call_graph[call.caller_name].add(call.callee_name)
        
        for symbol in symbols:
            if symbol.type != "method":
                continue
            
            # Determine fully qualified symbol name
            symbol_full_name = f"{symbol.parent_name}.{symbol.name}" if symbol.parent_name else symbol.name
            
            # Get method source code
            lines = source.split("\n")
            method_source = "\n".join(lines[symbol.start_line - 1:symbol.end_line])
            method_source_lower = method_source.lower()
            
            # Check algorithm patterns
            for pattern_name, pattern_info in ALGORITHM_PATTERNS.items():
                confidence = 0.0
                evidence_parts = []
                
                for kw in pattern_info["keywords"]:
                    if kw in symbol.name.lower():
                        confidence += 0.5
                        evidence_parts.append(f"keyword '{kw}' in method name")
                    if symbol.docstring and kw in symbol.docstring.lower():
                        confidence += 0.3
                        evidence_parts.append(f"keyword '{kw}' in Javadoc")
                
                # Recursion detection
                if pattern_name == "recursion" and call_graph:
                    recursion_info = self._detect_recursion(symbol_full_name, call_graph)
                    if recursion_info["is_recursive"]:
                        confidence += 0.8
                        if recursion_info["is_direct"]:
                            evidence_parts.append("direct recursion detected")
                        else:
                            evidence_parts.append(f"indirect recursion: {' -> '.join(recursion_info['cycle_path'])}")
                elif pattern_name == "recursion":
                    # Fallback detection
                    if f"this.{symbol.name}(" in method_source or f"{symbol.name}(" in method_source:
                        count = method_source.count(f"{symbol.name}(")
                        if count > 1:
                            confidence += 0.3
                            evidence_parts.append("potential recursion")
                elif pattern_info["indicators"] and pattern_info["indicators"](method_source, symbol.name):
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
                    if kw.lower() in symbol.name.lower() or kw.lower() in method_source_lower:
                        confidence += 0.3
                        evidence_parts.append(f"keyword '{kw}' found")
                
                if pattern_info["indicators"] and pattern_info["indicators"](method_source, symbol.name):
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
        """Extract all method calls from the given symbols."""
        calls: list[FunctionCall] = []
        
        # Build imported names mapping
        imported_names: dict[str, str] = {}
        for imp in imports:
            for name in imp.imported_names:
                if name != "*":
                    imported_names[name] = imp.module
        
        # Build class methods mapping
        class_methods: dict[str, set[str]] = {}
        for symbol in symbols:
            if symbol.type == "method" and symbol.parent_name:
                if symbol.parent_name not in class_methods:
                    class_methods[symbol.parent_name] = set()
                class_methods[symbol.parent_name].add(symbol.name)
        
        lines = source.split("\n")
        
        for symbol in symbols:
            if symbol.type != "method":
                continue
            
            method_source = "\n".join(lines[symbol.start_line - 1:symbol.end_line])
            tree = self.parser.parse(bytes(method_source, "utf-8"))
            
            caller_name = f"{symbol.parent_name}.{symbol.name}" if symbol.parent_name else symbol.name
            
            calls.extend(self._traverse_for_calls(
                tree.root_node,
                method_source,
                caller_name,
                symbol.parent_name,
                class_methods,
                imported_names,
                symbol.start_line
            ))
        
        return calls
    
    def _traverse_for_calls(
        self,
        node: Node,
        source: str,
        caller_name: str,
        parent_class: str | None,
        class_methods: dict[str, set[str]],
        imported_names: dict[str, str],
        line_offset: int
    ) -> list[FunctionCall]:
        """Traverse AST to find method invocations."""
        calls: list[FunctionCall] = []
        
        if node.type == "method_invocation":
            call = self._parse_method_invocation(
                node, source, caller_name, parent_class,
                class_methods, imported_names, line_offset
            )
            if call:
                calls.append(call)
        elif node.type == "object_creation_expression":
            call = self._parse_constructor_call(
                node, source, caller_name, imported_names, line_offset
            )
            if call:
                calls.append(call)
        
        for child in node.children:
            calls.extend(self._traverse_for_calls(
                child, source, caller_name, parent_class,
                class_methods, imported_names, line_offset
            ))
        
        return calls
    
    def _parse_method_invocation(
        self,
        node: Node,
        source: str,
        caller_name: str,
        parent_class: str | None,
        class_methods: dict[str, set[str]],
        imported_names: dict[str, str],
        line_offset: int
    ) -> FunctionCall | None:
        """Parse a method invocation node."""
        method_name_node = self._get_child_by_type(node, ["identifier"])
        if not method_name_node:
            return None
        
        method_name = self._node_text(method_name_node, source)
        line_number = line_offset + node.start_point[0]
        
        # Get arguments
        arguments: list[str] = []
        args_node = self._get_child_by_type(node, ["argument_list"])
        if args_node:
            for arg in args_node.children:
                if arg.type not in ("(", ")", ","):
                    arguments.append(self._node_text(arg, source))
        
        # Determine callee and if external
        callee_name = method_name
        is_external = False
        module = None
        call_type = "method"
        
        # Check for object.method() pattern
        obj_node = None
        for child in node.children:
            if child.type in ("identifier", "this", "field_access"):
                obj_node = child
                break
        
        if obj_node:
            obj_text = self._node_text(obj_node, source)
            if obj_text == "this":
                callee_name = f"{parent_class}.{method_name}" if parent_class else method_name
            else:
                callee_name = f"{obj_text}.{method_name}"
                if obj_text in imported_names:
                    is_external = True
                    module = imported_names[obj_text]
        
        return FunctionCall(
            caller_name=caller_name,
            callee_name=callee_name,
            call_type=call_type,
            line_number=line_number,
            is_external=is_external,
            module=module,
            arguments=arguments
        )
    
    def _parse_constructor_call(
        self,
        node: Node,
        source: str,
        caller_name: str,
        imported_names: dict[str, str],
        line_offset: int
    ) -> FunctionCall | None:
        """Parse a constructor (new) call."""
        type_node = self._get_child_by_type(node, ["type_identifier", "generic_type"])
        if not type_node:
            return None
        
        class_name = self._node_text(type_node, source)
        line_number = line_offset + node.start_point[0]
        
        arguments: list[str] = []
        args_node = self._get_child_by_type(node, ["argument_list"])
        if args_node:
            for arg in args_node.children:
                if arg.type not in ("(", ")", ","):
                    arguments.append(self._node_text(arg, source))
        
        is_external = class_name in imported_names
        module = imported_names.get(class_name)
        
        return FunctionCall(
            caller_name=caller_name,
            callee_name=f"new {class_name}",
            call_type="constructor",
            line_number=line_number,
            is_external=is_external,
            module=module,
            arguments=arguments
        )
