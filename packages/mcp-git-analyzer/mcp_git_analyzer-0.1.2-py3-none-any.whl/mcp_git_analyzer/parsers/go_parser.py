"""Go code parser using Tree-sitter."""

from pathlib import Path

import tree_sitter_go as tsgo
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


# Initialize Go parser
GO_LANGUAGE = Language(tsgo.language())
_parser = Parser(GO_LANGUAGE)


# Go-specific pattern indicators (extending base patterns)
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
        "indicators": lambda code, name: "sort.Slice(" in code or "sort.Sort(" in code or "sort.Ints(" in code
    },
    "graph_traversal": {
        **BASE_ALGORITHM_PATTERNS["graph_traversal"],
        "indicators": lambda code, name: "visited" in code.lower() and ("queue" in code.lower() or "stack" in code.lower())
    },
    "greedy": {
        **BASE_ALGORITHM_PATTERNS["greedy"],
        "indicators": lambda code, name: "math.Max(" in code or "math.Min(" in code
    },
    "backtracking": {
        **BASE_ALGORITHM_PATTERNS["backtracking"],
        "indicators": lambda code, name: "backtrack" in code.lower() or ("defer" in code and "restore" in code.lower())
    },
}

DESIGN_PATTERNS = {
    **BASE_DESIGN_PATTERNS,
    "singleton": {
        **BASE_DESIGN_PATTERNS["singleton"],
        "indicators": lambda code, name: "sync.Once" in code or ("once.Do" in code)
    },
    "factory": {
        **BASE_DESIGN_PATTERNS["factory"],
        "indicators": lambda code, name: name.startswith("New") or name.startswith("Create")
    },
    "builder": {
        "keywords": ["builder", "Builder", "Build"],
        "indicators": lambda code, name: "Builder" in name or ("return" in code and "*" + name.replace("Build", "") in code)
    },
    "decorator_pattern": {
        **BASE_DESIGN_PATTERNS["decorator_pattern"],
        "indicators": lambda code, name: "wrapper" in code.lower() or "Wrapper" in code
    },
    "interface_pattern": {
        "keywords": ["interface", "Interface"],
        "indicators": lambda code, name: "interface{}" in code or "type " in code and " interface" in code
    },
    "goroutine_pattern": {
        "keywords": ["goroutine", "go ", "channel", "chan"],
        "indicators": lambda code, name: "go func" in code or "make(chan" in code
    },
    "context_pattern": {
        "keywords": ["context", "ctx", "Context"],
        "indicators": lambda code, name: "context.Context" in code or "ctx context.Context" in code
    },
    "error_handling": {
        "keywords": ["error", "err", "Error"],
        "indicators": lambda code, name: "if err != nil" in code or "return err" in code
    },
}


class GoParser(BaseParser):
    """Parse Go source code using Tree-sitter."""
    
    def __init__(self):
        self.parser = _parser
    
    @property
    def language(self) -> str:
        return "go"
    
    @property
    def file_extensions(self) -> list[str]:
        return [".go"]
    
    def parse_file(self, file_path: Path) -> dict:
        """
        Parse a Go file and extract all symbols, imports, and patterns.
        
        Args:
            file_path: Path to the Go file
        
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
        Parse Go source code string.
        
        Args:
            source: Go source code
            file_name: Optional file name for context
            extract_calls: If True, extract function call graph
        
        Returns:
            Dict with symbols, imports, patterns, calls (if enabled), and metadata
        """
        tree = self.parser.parse(bytes(source, "utf-8"))
        root = tree.root_node
        
        symbols: list[Symbol] = []
        imports: list[Import] = []
        
        # Extract imports
        imports.extend(self._extract_imports(root, source))
        
        # Extract package-level declarations
        for child in root.children:
            if child.type == "function_declaration":
                symbol = self._extract_function(child, source, None)
                if symbol:
                    symbols.append(symbol)
            elif child.type == "method_declaration":
                symbol = self._extract_method(child, source)
                if symbol:
                    symbols.append(symbol)
            elif child.type == "type_declaration":
                type_symbols = self._extract_type_declaration(child, source)
                symbols.extend(type_symbols)
        
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
                import_spec_list = self._get_child_by_type(child, ["import_spec_list"])
                if import_spec_list:
                    # Multiple imports: import ( ... )
                    for spec in import_spec_list.children:
                        if spec.type == "import_spec":
                            imp = self._parse_import_spec(spec, source)
                            if imp:
                                imports.append(imp)
                else:
                    # Single import: import "package"
                    spec = self._get_child_by_type(child, ["import_spec"])
                    if spec:
                        imp = self._parse_import_spec(spec, source)
                        if imp:
                            imports.append(imp)
        
        return imports
    
    def _parse_import_spec(self, node: Node, source: str) -> Import | None:
        """Parse an import spec node."""
        path_node = self._get_child_by_type(node, ["interpreted_string_literal"])
        if not path_node:
            return None
        
        path = self._node_text(path_node, source).strip('"')
        
        # Get alias if present
        alias = None
        name_node = self._get_child_by_type(node, ["package_identifier", "dot", "blank_identifier"])
        if name_node:
            alias = self._node_text(name_node, source)
        
        # Extract package name from path
        parts = path.rsplit("/", 1)
        package_name = parts[-1] if parts else path
        
        return Import(
            module=path,
            alias=alias,
            imported_names=[package_name],
            is_relative=False,
            line_number=node.start_point[0] + 1,
            import_type="go"
        )
    
    def _extract_function(self, node: Node, source: str, parent_name: str | None) -> Symbol | None:
        """Extract function declaration."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Get type parameters (generics)
        type_params = self._extract_type_params(node, source)
        
        # Get parameters
        params_node = self._get_child_by_type(node, ["parameter_list"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        # Get return type
        return_type = None
        result_node = self._get_child_by_type(node, ["parameter_list"], skip=1)  # Second parameter_list is return
        if result_node:
            return_type = self._node_text(result_node, source)
        else:
            # Check for simple return type
            for child in node.children:
                if child.type in ("type_identifier", "pointer_type", "slice_type", 
                                  "map_type", "channel_type", "function_type",
                                  "interface_type", "struct_type", "qualified_type"):
                    return_type = self._node_text(child, source)
                    break
        
        # Build signature
        params_str = self._node_text(params_node, source) if params_node else "()"
        signature = f"func {name}"
        if type_params:
            signature += f"[{', '.join(type_params)}]"
        signature += params_str
        if return_type:
            signature += f" {return_type}"
        
        # Get doc comment
        docstring = self._extract_doc_comment(node, source)
        
        return Symbol(
            name=name,
            type="function",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            parameters=parameters,
            return_type=return_type,
            generic_params=type_params,
            is_exported=name[0].isupper() if name else False
        )
    
    def _extract_method(self, node: Node, source: str) -> Symbol | None:
        """Extract method declaration (function with receiver)."""
        name_node = self._get_child_by_type(node, ["field_identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Get receiver
        receiver_node = self._get_child_by_type(node, ["parameter_list"])
        receiver_type = None
        if receiver_node:
            # Extract receiver type
            for child in receiver_node.children:
                if child.type == "parameter_declaration":
                    type_node = self._get_child_by_type(child, ["type_identifier", "pointer_type"])
                    if type_node:
                        receiver_type = self._node_text(type_node, source)
                        # Clean pointer type
                        if receiver_type.startswith("*"):
                            receiver_type = receiver_type[1:]
                        break
        
        # Get parameters (second parameter_list)
        params_node = self._get_child_by_type(node, ["parameter_list"], skip=1)
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        # Get return type
        return_type = None
        result_node = self._get_child_by_type(node, ["parameter_list"], skip=2)
        if result_node:
            return_type = self._node_text(result_node, source)
        else:
            for child in node.children:
                if child.type in ("type_identifier", "pointer_type", "slice_type",
                                  "map_type", "channel_type", "qualified_type"):
                    return_type = self._node_text(child, source)
                    break
        
        # Build signature
        receiver_str = self._node_text(receiver_node, source) if receiver_node else ""
        params_str = self._node_text(params_node, source) if params_node else "()"
        signature = f"func {receiver_str} {name}{params_str}"
        if return_type:
            signature += f" {return_type}"
        
        docstring = self._extract_doc_comment(node, source)
        
        return Symbol(
            name=name,
            type="method",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=receiver_type,
            parameters=parameters,
            return_type=return_type,
            is_exported=name[0].isupper() if name else False
        )
    
    def _extract_type_declaration(self, node: Node, source: str) -> list[Symbol]:
        """Extract type declarations (struct, interface, type alias)."""
        symbols = []
        
        for child in node.children:
            if child.type == "type_spec":
                symbol = self._parse_type_spec(child, source)
                if symbol:
                    symbols.append(symbol)
        
        return symbols
    
    def _parse_type_spec(self, node: Node, source: str) -> Symbol | None:
        """Parse a type specification."""
        name_node = self._get_child_by_type(node, ["type_identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        type_params = self._extract_type_params(node, source)
        
        # Determine type kind
        type_kind = "type_alias"
        signature_suffix = ""
        
        struct_node = self._get_child_by_type(node, ["struct_type"])
        interface_node = self._get_child_by_type(node, ["interface_type"])
        
        if struct_node:
            type_kind = "class"  # Map struct to class for consistency
            signature_suffix = " struct { ... }"
        elif interface_node:
            type_kind = "interface"
            signature_suffix = " interface { ... }"
        else:
            # Type alias
            for child in node.children:
                if child.type not in ("type_identifier", "type_parameter_list"):
                    signature_suffix = f" = {self._node_text(child, source)}"
                    break
        
        signature = f"type {name}"
        if type_params:
            signature += f"[{', '.join(type_params)}]"
        signature += signature_suffix
        
        docstring = self._extract_doc_comment(node.parent if node.parent else node, source)
        
        return Symbol(
            name=name,
            type=type_kind,
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            generic_params=type_params,
            is_exported=name[0].isupper() if name else False
        )
    
    def _extract_type_params(self, node: Node, source: str) -> list[str]:
        """Extract generic type parameters."""
        params = []
        type_params_node = self._get_child_by_type(node, ["type_parameter_list"])
        if type_params_node:
            for child in type_params_node.children:
                if child.type == "type_parameter_declaration":
                    params.append(self._node_text(child, source))
        return params
    
    def _extract_parameters(self, params_node: Node, source: str) -> list[dict]:
        """Extract function/method parameters."""
        parameters = []
        
        for child in params_node.children:
            if child.type == "parameter_declaration":
                param_type = None
                names = []
                
                # Extract names
                for sub in child.children:
                    if sub.type == "identifier":
                        names.append(self._node_text(sub, source))
                    elif sub.type in ("type_identifier", "pointer_type", "slice_type",
                                      "map_type", "channel_type", "function_type",
                                      "interface_type", "struct_type", "qualified_type",
                                      "variadic_parameter_declaration"):
                        param_type = self._node_text(sub, source)
                
                if not names:
                    # Type-only parameter
                    names = [""]
                
                for name in names:
                    parameters.append({"name": name, "type": param_type})
            elif child.type == "variadic_parameter_declaration":
                # ...T parameters
                name = ""
                param_type = None
                for sub in child.children:
                    if sub.type == "identifier":
                        name = self._node_text(sub, source)
                    elif sub.type.endswith("_type") or sub.type == "type_identifier":
                        param_type = "..." + self._node_text(sub, source)
                parameters.append({"name": name, "type": param_type})
        
        return parameters
    
    def _extract_doc_comment(self, node: Node, source: str) -> str | None:
        """Extract Go doc comment (// comments before declaration)."""
        # Look for comment lines immediately before the node
        lines = source[:node.start_byte].split('\n')
        
        doc_lines = []
        for line in reversed(lines):
            stripped = line.strip()
            if stripped.startswith("//"):
                doc_lines.insert(0, stripped[2:].strip())
            elif stripped:
                # Hit non-comment, non-empty line
                break
        
        if doc_lines:
            return "\n".join(doc_lines)
        return None
    
    def _detect_patterns(
        self,
        symbols: list[Symbol],
        source: str,
        calls: list[FunctionCall] | None = None
    ) -> list[Pattern]:
        """Detect algorithmic patterns in code."""
        patterns = []
        
        # Build call graph lookup
        call_graph: dict[str, set[str]] = {}
        if calls:
            for call in calls:
                if call.caller_name not in call_graph:
                    call_graph[call.caller_name] = set()
                call_graph[call.caller_name].add(call.callee_name)
        
        for symbol in symbols:
            if symbol.type not in ("function", "method"):
                continue
            
            symbol_full_name = f"{symbol.parent_name}.{symbol.name}" if symbol.parent_name else symbol.name
            
            lines = source.split("\n")
            func_source = "\n".join(lines[symbol.start_line - 1:symbol.end_line])
            func_source_lower = func_source.lower()
            
            # Check algorithm patterns
            for pattern_name, pattern_info in ALGORITHM_PATTERNS.items():
                confidence = 0.0
                evidence_parts = []
                
                for kw in pattern_info["keywords"]:
                    if kw.lower() in symbol.name.lower():
                        confidence += 0.5
                        evidence_parts.append(f"keyword '{kw}' in name")
                    if symbol.docstring and kw.lower() in symbol.docstring.lower():
                        confidence += 0.3
                        evidence_parts.append(f"keyword '{kw}' in doc")
                
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
            
            # Check design patterns (including Go-specific)
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
        
        if symbol_name in callees:
            return {"is_recursive": True, "is_direct": True, "cycle_path": [symbol_name, symbol_name]}
        
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
        """Extract all function/method calls from the given symbols."""
        calls: list[FunctionCall] = []
        
        # Build imported packages mapping
        imported_packages: dict[str, str] = {}
        for imp in imports:
            package_name = imp.alias if imp.alias and imp.alias != "." else imp.imported_names[0] if imp.imported_names else ""
            if package_name:
                imported_packages[package_name] = imp.module
        
        lines = source.split("\n")
        
        for symbol in symbols:
            if symbol.type not in ("function", "method"):
                continue
            
            func_source = "\n".join(lines[symbol.start_line - 1:symbol.end_line])
            tree = self.parser.parse(bytes(func_source, "utf-8"))
            
            caller_name = f"{symbol.parent_name}.{symbol.name}" if symbol.parent_name else symbol.name
            
            calls.extend(self._traverse_for_calls(
                tree.root_node,
                func_source,
                caller_name,
                imported_packages,
                symbol.start_line
            ))
        
        return calls
    
    def _traverse_for_calls(
        self,
        node: Node,
        source: str,
        caller_name: str,
        imported_packages: dict[str, str],
        line_offset: int
    ) -> list[FunctionCall]:
        """Traverse AST to find function calls."""
        calls: list[FunctionCall] = []
        
        if node.type == "call_expression":
            call = self._parse_call_expression(
                node, source, caller_name, imported_packages, line_offset
            )
            if call:
                calls.append(call)
        
        for child in node.children:
            calls.extend(self._traverse_for_calls(
                child, source, caller_name, imported_packages, line_offset
            ))
        
        return calls
    
    def _parse_call_expression(
        self,
        node: Node,
        source: str,
        caller_name: str,
        imported_packages: dict[str, str],
        line_offset: int
    ) -> FunctionCall | None:
        """Parse a call expression node."""
        if not node.children:
            return None
        
        function_part = node.children[0]
        line_number = line_offset + node.start_point[0]
        
        # Get arguments
        arguments: list[str] = []
        args_node = self._get_child_by_type(node, ["argument_list"])
        if args_node:
            for arg in args_node.children:
                if arg.type not in ("(", ")", ","):
                    arguments.append(self._node_text(arg, source))
        
        callee_name = ""
        call_type = "function"
        is_external = False
        module = None
        is_async_call = False
        
        if function_part.type == "identifier":
            # Direct function call: foo()
            callee_name = self._node_text(function_part, source)
        elif function_part.type == "selector_expression":
            # Package or receiver call: pkg.Func() or obj.Method()
            call_type = "method"
            obj_node = function_part.children[0] if function_part.children else None
            method_node = self._get_child_by_type(function_part, ["field_identifier"])
            
            if obj_node and method_node:
                obj_text = self._node_text(obj_node, source)
                method_name = self._node_text(method_node, source)
                callee_name = f"{obj_text}.{method_name}"
                
                # Check if it's a package call
                if obj_text in imported_packages:
                    is_external = True
                    module = imported_packages[obj_text]
        elif function_part.type == "parenthesized_expression":
            # Type assertion or conversion
            callee_name = self._node_text(function_part, source)
            call_type = "function"
        else:
            callee_name = self._node_text(function_part, source)
        
        # Check for go keyword (goroutine)
        parent = node.parent
        if parent and parent.type == "go_statement":
            is_async_call = True
        
        if not callee_name:
            return None
        
        return FunctionCall(
            caller_name=caller_name,
            callee_name=callee_name,
            call_type=call_type,
            line_number=line_number,
            is_external=is_external,
            module=module,
            arguments=arguments,
            is_async_call=is_async_call
        )
