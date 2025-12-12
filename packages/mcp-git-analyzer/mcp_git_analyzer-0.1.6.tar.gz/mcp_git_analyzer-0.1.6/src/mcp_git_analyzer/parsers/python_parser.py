"""Python code parser using Tree-sitter."""

from pathlib import Path

import tree_sitter_python as tspython
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


# Initialize Python parser
PY_LANGUAGE = Language(tspython.language())
_parser = Parser(PY_LANGUAGE)


# Python-specific pattern indicators (extending base patterns)
ALGORITHM_PATTERNS = {
    **BASE_ALGORITHM_PATTERNS,
    "dynamic_programming": {
        **BASE_ALGORITHM_PATTERNS["dynamic_programming"],
        "indicators": lambda code, name: "memo" in code.lower() or "@cache" in code or "@lru_cache" in code
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
        "indicators": lambda code, name: ".sort(" in code or "sorted(" in code
    },
    "graph_traversal": {
        **BASE_ALGORITHM_PATTERNS["graph_traversal"],
        "indicators": lambda code, name: ("queue" in code.lower() or "stack" in code.lower()) and ("visited" in code.lower())
    },
    "greedy": {
        **BASE_ALGORITHM_PATTERNS["greedy"],
        "indicators": lambda code, name: "max(" in code or "min(" in code
    },
    "backtracking": {
        **BASE_ALGORITHM_PATTERNS["backtracking"],
        "indicators": lambda code, name: "undo" in code.lower() or "restore" in code.lower()
    },
}

DESIGN_PATTERNS = {
    **BASE_DESIGN_PATTERNS,
    "singleton": {
        **BASE_DESIGN_PATTERNS["singleton"],
        "indicators": lambda code, name: "_instance" in code and "cls._instance" in code
    },
    "factory": {
        **BASE_DESIGN_PATTERNS["factory"],
        "indicators": lambda code, name: "create_" in name.lower() or "make_" in name.lower()
    },
    "decorator_pattern": {
        **BASE_DESIGN_PATTERNS["decorator_pattern"],
        "indicators": lambda code, name: "wrapper" in code and "functools" in code
    },
    "iterator": {
        "keywords": ["iterator", "__iter__", "__next__"],
        "indicators": lambda code, name: "__iter__" in code and "__next__" in code
    },
    "context_manager": {
        "keywords": ["context", "__enter__", "__exit__"],
        "indicators": lambda code, name: "__enter__" in code and "__exit__" in code
    },
}


class PythonParser(BaseParser):
    """Parse Python source code using Tree-sitter."""
    
    def __init__(self):
        self.parser = _parser
    
    @property
    def language(self) -> str:
        return "python"
    
    @property
    def file_extensions(self) -> list[str]:
        return [".py", ".pyw"]
    
    def parse_file(self, file_path: Path) -> dict:
        """
        Parse a Python file and extract all symbols, imports, and patterns.
        
        Args:
            file_path: Path to the Python file
        
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
        Parse Python source code string.
        
        Args:
            source: Python source code
            file_name: Optional file name for context
            extract_calls: If True, extract function call graph (optional, disabled by default)
        
        Returns:
            Dict with symbols, imports, patterns, calls (if enabled), and metadata
        """
        tree = self.parser.parse(bytes(source, "utf-8"))
        root = tree.root_node
        
        symbols: list[Symbol] = []
        imports: list[Import] = []
        
        # Extract imports
        imports.extend(self._extract_imports(root, source))
        
        # Extract top-level symbols
        for child in root.children:
            if child.type == "function_definition":
                symbol = self._extract_function(child, source, None)
                if symbol:
                    symbols.append(symbol)
            elif child.type == "class_definition":
                class_symbol, methods = self._extract_class(child, source)
                if class_symbol:
                    symbols.append(class_symbol)
                    symbols.extend(methods)
            elif child.type == "decorated_definition":
                # Handle decorated functions/classes
                definition = self._get_child_by_type(child, ["function_definition", "class_definition"])
                if definition:
                    decorators = self._extract_decorators(child, source)
                    if definition.type == "function_definition":
                        symbol = self._extract_function(definition, source, None, decorators)
                        if symbol:
                            symbols.append(symbol)
                    elif definition.type == "class_definition":
                        class_symbol, methods = self._extract_class(definition, source, decorators)
                        if class_symbol:
                            symbols.append(class_symbol)
                            symbols.extend(methods)
        
        # Detect patterns (with call graph awareness if enabled)
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
            if child.type == "import_statement":
                # import module / import module as alias
                for name_node in child.children:
                    if name_node.type == "dotted_name":
                        module = self._node_text(name_node, source)
                        imports.append(Import(
                            module=module,
                            alias=None,
                            imported_names=[],
                            is_relative=False,
                            line_number=child.start_point[0] + 1,
                            import_type="python"
                        ))
                    elif name_node.type == "aliased_import":
                        name = self._get_child_by_type(name_node, ["dotted_name"])
                        alias = self._get_child_by_type(name_node, ["identifier"], skip=1)
                        if name:
                            imports.append(Import(
                                module=self._node_text(name, source),
                                alias=self._node_text(alias, source) if alias else None,
                                imported_names=[],
                                is_relative=False,
                                line_number=child.start_point[0] + 1,
                                import_type="python"
                            ))
            
            elif child.type == "import_from_statement":
                # from module import names
                is_relative = False
                module = ""
                imported_names = []
                
                for node in child.children:
                    if node.type == "relative_import":
                        is_relative = True
                        dotted = self._get_child_by_type(node, ["dotted_name"])
                        if dotted:
                            module = self._node_text(dotted, source)
                    elif node.type == "dotted_name":
                        module = self._node_text(node, source)
                    elif node.type == "import_prefix":
                        is_relative = True
                    elif node.type in ("identifier", "aliased_import"):
                        if node.type == "identifier":
                            imported_names.append(self._node_text(node, source))
                        else:
                            name = self._get_child_by_type(node, ["identifier"])
                            if name:
                                imported_names.append(self._node_text(name, source))
                    elif node.type == "wildcard_import":
                        imported_names.append("*")
                
                if module or imported_names:
                    imports.append(Import(
                        module=module,
                        alias=None,
                        imported_names=imported_names,
                        is_relative=is_relative,
                        line_number=child.start_point[0] + 1,
                        import_type="python"
                    ))
        
        return imports
    
    def _extract_function(self, node: Node, source: str, parent_name: str | None, 
                          decorators: list[str] | None = None) -> Symbol | None:
        """Extract function/method definition."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Get parameters
        params_node = self._get_child_by_type(node, ["parameters"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        # Get return type
        return_type = None
        for child in node.children:
            if child.type == "type":
                return_type = self._node_text(child, source)
                break
        
        # Get docstring
        body = self._get_child_by_type(node, ["block"])
        docstring = self._extract_docstring(body, source) if body else None
        
        # Build signature
        params_str = self._node_text(params_node, source) if params_node else "()"
        signature = f"def {name}{params_str}"
        if return_type:
            signature += f" -> {return_type}"
        
        symbol_type = "method" if parent_name else "function"
        
        return Symbol(
            name=name,
            type=symbol_type,
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            parameters=parameters,
            return_type=return_type,
            decorators=decorators or []
        )
    
    def _extract_class(self, node: Node, source: str, 
                       decorators: list[str] | None = None) -> tuple[Symbol | None, list[Symbol]]:
        """Extract class definition and its methods."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None, []
        
        name = self._node_text(name_node, source)
        
        # Get base classes
        bases = []
        arg_list = self._get_child_by_type(node, ["argument_list"])
        if arg_list:
            for child in arg_list.children:
                if child.type == "identifier":
                    bases.append(self._node_text(child, source))
        
        # Build signature
        signature = f"class {name}"
        if bases:
            signature += f"({', '.join(bases)})"
        
        # Get docstring
        body = self._get_child_by_type(node, ["block"])
        docstring = self._extract_docstring(body, source) if body else None
        
        class_symbol = Symbol(
            name=name,
            type="class",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=None,
            parameters=[{"base": b} for b in bases],
            decorators=decorators or []
        )
        
        # Extract methods
        methods = []
        if body:
            for child in body.children:
                if child.type == "function_definition":
                    method = self._extract_function(child, source, name)
                    if method:
                        methods.append(method)
                elif child.type == "decorated_definition":
                    func_def = self._get_child_by_type(child, ["function_definition"])
                    if func_def:
                        method_decorators = self._extract_decorators(child, source)
                        method = self._extract_function(func_def, source, name, method_decorators)
                        if method:
                            methods.append(method)
        
        return class_symbol, methods
    
    def _extract_parameters(self, params_node: Node, source: str) -> list[dict]:
        """Extract function parameters with type hints."""
        parameters = []
        
        for child in params_node.children:
            if child.type in ("identifier", "typed_parameter", "default_parameter", 
                              "typed_default_parameter", "list_splat_pattern", "dictionary_splat_pattern"):
                param = {"name": "", "type": None, "default": None}
                
                if child.type == "identifier":
                    param["name"] = self._node_text(child, source)
                elif child.type == "typed_parameter":
                    name = self._get_child_by_type(child, ["identifier"])
                    type_node = self._get_child_by_type(child, ["type"])
                    param["name"] = self._node_text(name, source) if name else ""
                    param["type"] = self._node_text(type_node, source) if type_node else None
                elif child.type in ("default_parameter", "typed_default_parameter"):
                    name = self._get_child_by_type(child, ["identifier"])
                    param["name"] = self._node_text(name, source) if name else ""
                    # Get default value
                    for sub in child.children:
                        if sub.type not in ("identifier", "type", ":", "="):
                            param["default"] = self._node_text(sub, source)
                    if child.type == "typed_default_parameter":
                        type_node = self._get_child_by_type(child, ["type"])
                        param["type"] = self._node_text(type_node, source) if type_node else None
                elif child.type == "list_splat_pattern":
                    name = self._get_child_by_type(child, ["identifier"])
                    param["name"] = f"*{self._node_text(name, source)}" if name else "*args"
                elif child.type == "dictionary_splat_pattern":
                    name = self._get_child_by_type(child, ["identifier"])
                    param["name"] = f"**{self._node_text(name, source)}" if name else "**kwargs"
                
                if param["name"]:
                    parameters.append(param)
        
        return parameters
    
    def _extract_decorators(self, node: Node, source: str) -> list[str]:
        """Extract decorator names from decorated definition."""
        decorators = []
        for child in node.children:
            if child.type == "decorator":
                dec_text = self._node_text(child, source)
                decorators.append(dec_text.strip())
        return decorators
    
    def _extract_docstring(self, body: Node, source: str) -> str | None:
        """Extract docstring from function/class body."""
        if not body or not body.children:
            return None
        
        for child in body.children:
            if child.type == "expression_statement":
                string_node = self._get_child_by_type(child, ["string"])
                if string_node:
                    docstring = self._node_text(string_node, source)
                    # Clean up docstring
                    docstring = docstring.strip("\"'")
                    if docstring.startswith('""'):
                        docstring = docstring[2:]
                    if docstring.endswith('""'):
                        docstring = docstring[:-2]
                    return docstring.strip()
                break  # Only first statement can be docstring
            elif child.type not in ("comment", "newline"):
                break
        
        return None
    
    def _detect_patterns(
        self, 
        symbols: list[Symbol], 
        source: str, 
        calls: list[FunctionCall] | None = None
    ) -> list[Pattern]:
        """
        Detect algorithmic patterns in code.
        
        Args:
            symbols: List of parsed symbols
            source: Source code string
            calls: Optional list of function calls for enhanced detection
        
        Returns:
            List of detected patterns
        """
        patterns = []
        source.lower()
        
        # Build call graph lookup for recursion detection
        call_graph: dict[str, set[str]] = {}
        if calls:
            for call in calls:
                if call.caller_name not in call_graph:
                    call_graph[call.caller_name] = set()
                call_graph[call.caller_name].add(call.callee_name)
        
        for symbol in symbols:
            if symbol.type not in ("function", "method"):
                continue
            
            # Determine fully qualified symbol name
            if symbol.parent_name:
                symbol_full_name = f"{symbol.parent_name}.{symbol.name}"
            else:
                symbol_full_name = symbol.name
            
            # Get function source code
            lines = source.split("\n")
            func_source = "\n".join(lines[symbol.start_line - 1:symbol.end_line])
            func_source_lower = func_source.lower()
            
            # Check algorithm patterns
            for pattern_name, pattern_info in ALGORITHM_PATTERNS.items():
                confidence = 0.0
                evidence_parts = []
                
                # Check keywords in name or docstring
                for kw in pattern_info["keywords"]:
                    if kw in symbol.name.lower():
                        confidence += 0.5
                        evidence_parts.append(f"keyword '{kw}' in function name")
                    if symbol.docstring and kw in symbol.docstring.lower():
                        confidence += 0.3
                        evidence_parts.append(f"keyword '{kw}' in docstring")
                
                # Special handling for recursion using call graph
                if pattern_name == "recursion" and call_graph:
                    recursion_info = self._detect_recursion(
                        symbol_full_name, call_graph, max_depth=3
                    )
                    if recursion_info["is_recursive"]:
                        confidence += 0.8
                        if recursion_info["is_direct"]:
                            evidence_parts.append("direct recursion detected via call graph")
                        else:
                            cycle_path = " -> ".join(recursion_info["cycle_path"])
                            evidence_parts.append(f"indirect recursion: {cycle_path}")
                elif pattern_name == "recursion":
                    # Fallback to old string-based detection if no call graph
                    if symbol.name in func_source and f"def {symbol.name}" in func_source:
                        # Count occurrences - if name appears more than in def, it might be recursive
                        name_count = func_source.count(symbol.name)
                        if name_count > 1:
                            confidence += 0.3
                            evidence_parts.append("potential recursion (name appears in body)")
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
                    if kw in symbol.name.lower() or kw in func_source_lower:
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
        """
        Detect if a symbol is recursive using the call graph.
        
        Args:
            symbol_name: Fully qualified name of the function/method
            call_graph: Dict mapping caller names to sets of callee names
            max_depth: Maximum depth to search for indirect recursion
        
        Returns:
            Dict with is_recursive, is_direct, and cycle_path
        """
        result = {"is_recursive": False, "is_direct": False, "cycle_path": []}
        
        if symbol_name not in call_graph:
            return result
        
        callees = call_graph.get(symbol_name, set())
        
        # Check direct recursion
        if symbol_name in callees:
            return {
                "is_recursive": True,
                "is_direct": True,
                "cycle_path": [symbol_name, symbol_name]
            }
        
        # Check indirect recursion using BFS
        visited: set[str] = {symbol_name}
        queue: list[tuple[str, list[str]]] = [(symbol_name, [symbol_name])]
        
        depth = 0
        while queue and depth < max_depth:
            next_queue: list[tuple[str, list[str]]] = []
            for current, path in queue:
                for callee in call_graph.get(current, set()):
                    if callee == symbol_name:
                        return {
                            "is_recursive": True,
                            "is_direct": False,
                            "cycle_path": path + [callee]
                        }
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
        """
        Extract all function calls from the given symbols.
        
        Args:
            symbols: List of parsed symbols (functions, methods, classes)
            source: Original source code
            imports: List of parsed imports for external call detection
        
        Returns:
            List of FunctionCall objects
        """
        calls: list[FunctionCall] = []
        lines = source.split("\n")
        
        # Build import lookup for external detection
        imported_names = self._build_import_lookup(imports)
        
        # Build class-to-methods mapping for self.method normalization
        class_methods: dict[str, set[str]] = {}
        for symbol in symbols:
            if symbol.type == "method" and symbol.parent_name:
                if symbol.parent_name not in class_methods:
                    class_methods[symbol.parent_name] = set()
                class_methods[symbol.parent_name].add(symbol.name)
        
        for symbol in symbols:
            if symbol.type not in ("function", "method"):
                continue
            
            # Get the function's source code portion
            func_source = "\n".join(lines[symbol.start_line - 1:symbol.end_line])
            
            # Parse the function source to get its AST
            func_tree = self.parser.parse(bytes(func_source, "utf-8"))
            
            # Determine the fully qualified caller name
            if symbol.parent_name:
                caller_name = f"{symbol.parent_name}.{symbol.name}"
            else:
                caller_name = symbol.name
            
            # Extract calls from this function's body
            func_calls = self._traverse_for_calls(
                func_tree.root_node,
                func_source,
                caller_name,
                symbol.parent_name,
                class_methods,
                imported_names,
                symbol.start_line  # offset for line numbers
            )
            calls.extend(func_calls)
        
        return calls
    
    def _build_import_lookup(self, imports: list[Import]) -> dict[str, str]:
        """
        Build a lookup dict from imported names to their modules.
        
        Returns:
            Dict mapping name -> module (e.g., {"Path": "pathlib", "json": "json"})
        """
        lookup: dict[str, str] = {}
        
        for imp in imports:
            if imp.imported_names:
                # from module import name1, name2
                for name in imp.imported_names:
                    if name != "*":
                        lookup[name] = imp.module
            else:
                # import module / import module as alias
                module_name = imp.alias if imp.alias else imp.module.split(".")[-1]
                lookup[module_name] = imp.module
        
        return lookup
    
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
        """
        Recursively traverse AST nodes to find function calls.
        
        Args:
            node: Current AST node
            source: Source code string
            caller_name: Fully qualified name of the calling function
            parent_class: Class name if caller is a method
            class_methods: Mapping of class names to their method names
            imported_names: Mapping of imported names to modules
            line_offset: Line number offset for accurate reporting
        
        Returns:
            List of FunctionCall objects found in this node and descendants
        """
        calls: list[FunctionCall] = []
        
        if node.type == "call":
            call = self._parse_call_node(
                node, source, caller_name, parent_class,
                class_methods, imported_names, line_offset
            )
            if call:
                calls.append(call)
        
        # Recurse into children
        for child in node.children:
            calls.extend(self._traverse_for_calls(
                child, source, caller_name, parent_class,
                class_methods, imported_names, line_offset
            ))
        
        return calls
    
    def _parse_call_node(
        self,
        node: Node,
        source: str,
        caller_name: str,
        parent_class: str | None,
        class_methods: dict[str, set[str]],
        imported_names: dict[str, str],
        line_offset: int
    ) -> FunctionCall | None:
        """
        Parse a call node and extract call information.
        
        Args:
            node: The 'call' AST node
            source: Source code string
            caller_name: Fully qualified name of the calling function
            parent_class: Class name if caller is a method
            class_methods: Mapping of class names to their method names
            imported_names: Mapping of imported names to modules
            line_offset: Line number offset
        
        Returns:
            FunctionCall object or None if unable to parse
        """
        if not node.children:
            return None
        
        function_part = node.children[0]
        line_number = line_offset + node.start_point[0]
        
        # Extract arguments
        arguments: list[str] = []
        args_node = self._get_child_by_type(node, ["argument_list"])
        if args_node:
            for arg in args_node.children:
                if arg.type not in ("(", ")", ","):
                    arguments.append(self._node_text(arg, source))
        
        callee_name: str = ""
        call_type: str = "function"
        is_external: bool = False
        module: str | None = None
        
        if function_part.type == "identifier":
            # Direct function call: foo()
            callee_name = self._node_text(function_part, source)
            
            # Check if it's an imported name
            if callee_name in imported_names:
                is_external = True
                module = imported_names[callee_name]
            
            # Check if it's a builtin
            if callee_name in PYTHON_BUILTINS:
                call_type = "builtin"
        
        elif function_part.type == "attribute":
            # Method call: obj.method() or self.method() or module.func()
            call_type = "method"
            
            # Get the object and attribute parts
            if len(function_part.children) >= 3:
                obj_part = function_part.children[0]
                attr_part = function_part.children[2]  # Skip the '.'
                
                obj_text = self._node_text(obj_part, source)
                method_name = self._node_text(attr_part, source)
                
                if obj_text == "self" and parent_class:
                    # self.method() -> ClassName.method
                    callee_name = f"{parent_class}.{method_name}"
                    # Check if it's a known method of this class
                    if parent_class in class_methods and method_name in class_methods[parent_class]:
                        is_external = False
                    else:
                        # Could be inherited or dynamic
                        is_external = False
                elif obj_text == "cls" and parent_class:
                    # cls.method() -> ClassName.method
                    callee_name = f"{parent_class}.{method_name}"
                elif obj_text in imported_names:
                    # module.func() or imported_class.method()
                    callee_name = f"{obj_text}.{method_name}"
                    is_external = True
                    module = imported_names[obj_text]
                else:
                    # obj.method() - could be local variable or unknown
                    callee_name = f"{obj_text}.{method_name}"
        
        elif function_part.type == "subscript":
            # Callable subscript: some_dict["key"]()
            callee_name = self._node_text(function_part, source)
            call_type = "function"
        
        else:
            # Other cases (lambda calls, etc.)
            callee_name = self._node_text(function_part, source)
        
        if not callee_name:
            return None
        
        return FunctionCall(
            caller_name=caller_name,
            callee_name=callee_name,
            call_type=call_type,
            line_number=line_number,
            is_external=is_external,
            module=module,
            arguments=arguments
        )


# Python builtin functions for call type detection
PYTHON_BUILTINS = {
    "abs", "aiter", "all", "any", "anext", "ascii", "bin", "bool", "breakpoint",
    "bytearray", "bytes", "callable", "chr", "classmethod", "compile", "complex",
    "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter",
    "float", "format", "frozenset", "getattr", "globals", "hasattr", "hash",
    "help", "hex", "id", "input", "int", "isinstance", "issubclass", "iter",
    "len", "list", "locals", "map", "max", "memoryview", "min", "next", "object",
    "oct", "open", "ord", "pow", "print", "property", "range", "repr", "reversed",
    "round", "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum",
    "super", "tuple", "type", "vars", "zip", "__import__"
}
