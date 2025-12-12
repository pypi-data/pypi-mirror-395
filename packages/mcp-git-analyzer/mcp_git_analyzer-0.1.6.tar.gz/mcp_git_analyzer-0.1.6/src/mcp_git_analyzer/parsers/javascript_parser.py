"""JavaScript code parser using Tree-sitter."""

from pathlib import Path

import tree_sitter_javascript as tsjavascript
from tree_sitter import Language, Parser, Node

from mcp_git_analyzer.parsers.base_parser import (
    BaseParser,
    Symbol,
    Import,
    Pattern,
    FunctionCall,
    ALGORITHM_PATTERNS as BASE_ALGORITHM_PATTERNS,
    DESIGN_PATTERNS as BASE_DESIGN_PATTERNS,
    JS_PATTERNS,
)


# Initialize JavaScript parser
JS_LANGUAGE = Language(tsjavascript.language())
_parser = Parser(JS_LANGUAGE)


# JavaScript-specific pattern indicators
ALGORITHM_PATTERNS = {
    **BASE_ALGORITHM_PATTERNS,
    "dynamic_programming": {
        **BASE_ALGORITHM_PATTERNS["dynamic_programming"],
        "indicators": lambda code, name: "memo" in code.lower() or "cache" in code.lower()
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
        "indicators": lambda code, name: ".sort(" in code
    },
    "graph_traversal": {
        **BASE_ALGORITHM_PATTERNS["graph_traversal"],
        "indicators": lambda code, name: ("queue" in code.lower() or "stack" in code.lower()) and ("visited" in code.lower())
    },
    "greedy": {
        **BASE_ALGORITHM_PATTERNS["greedy"],
        "indicators": lambda code, name: "Math.max(" in code or "Math.min(" in code
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
        "indicators": lambda code, name: "_instance" in code or "getInstance" in code
    },
    "factory": {
        **BASE_DESIGN_PATTERNS["factory"],
        "indicators": lambda code, name: "create" in name.lower() or "make" in name.lower()
    },
    "decorator_pattern": {
        **BASE_DESIGN_PATTERNS["decorator_pattern"],
        "indicators": lambda code, name: "wrapper" in code.lower()
    },
    "module": {
        "keywords": ["module", "exports", "require"],
        "indicators": lambda code, name: "module.exports" in code or "exports." in code
    },
}


# JavaScript builtin functions
JS_BUILTINS = {
    "console", "log", "error", "warn", "info", "debug",
    "parseInt", "parseFloat", "isNaN", "isFinite",
    "encodeURI", "decodeURI", "encodeURIComponent", "decodeURIComponent",
    "eval", "setTimeout", "setInterval", "clearTimeout", "clearInterval",
    "JSON", "Math", "Date", "Array", "Object", "String", "Number", "Boolean",
    "Map", "Set", "WeakMap", "WeakSet", "Symbol", "Promise",
    "fetch", "require", "import",
}


class JavaScriptParser(BaseParser):
    """Parse JavaScript source code using Tree-sitter."""
    
    def __init__(self):
        self.parser = _parser
        self._language = JS_LANGUAGE
    
    @property
    def language(self) -> str:
        return "javascript"
    
    @property
    def file_extensions(self) -> list[str]:
        return [".js", ".jsx", ".mjs", ".cjs"]
    
    def parse_file(self, file_path: Path) -> dict:
        """Parse a JavaScript file and extract all symbols, imports, and patterns."""
        try:
            source = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            return {"error": str(e), "symbols": [], "imports": [], "patterns": []}
        
        return self.parse_source(source, str(file_path))
    
    def parse_source(self, source: str, file_name: str = "<source>", 
                     extract_calls: bool = False) -> dict:
        """Parse JavaScript source code string."""
        tree = self.parser.parse(bytes(source, "utf-8"))
        root = tree.root_node
        
        symbols: list[Symbol] = []
        imports: list[Import] = []
        
        # Extract imports (ESM and CommonJS)
        imports.extend(self._extract_imports(root, source))
        
        # Extract top-level symbols
        self._extract_symbols_recursive(root, source, None, symbols)
        
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
    
    def _extract_symbols_recursive(
        self, 
        node: Node, 
        source: str, 
        parent_name: str | None,
        symbols: list[Symbol]
    ) -> None:
        """Recursively extract symbols from AST nodes."""
        for child in node.children:
            symbol = None
            child_symbols: list[Symbol] = []
            
            if child.type == "function_declaration":
                symbol = self._extract_function(child, source, parent_name)
            elif child.type == "class_declaration":
                symbol, child_symbols = self._extract_class(child, source)
            elif child.type == "lexical_declaration" or child.type == "variable_declaration":
                # Handle const/let/var declarations
                extracted = self._extract_variable_declaration(child, source, parent_name)
                symbols.extend(extracted)
                continue
            elif child.type == "export_statement":
                # Handle exports
                self._extract_export(child, source, symbols)
                continue
            elif child.type == "expression_statement":
                # Handle expression-based declarations (e.g., module.exports = ...)
                self._extract_expression_declaration(child, source, parent_name, symbols)
                continue
            
            if symbol:
                symbols.append(symbol)
                symbols.extend(child_symbols)
    
    def _extract_imports(self, root: Node, source: str) -> list[Import]:
        """Extract ESM and CommonJS import statements."""
        imports = []
        
        for child in root.children:
            if child.type == "import_statement":
                imports.extend(self._extract_esm_import(child, source))
            elif child.type == "lexical_declaration" or child.type == "variable_declaration":
                # Check for CommonJS require
                imports.extend(self._extract_commonjs_require(child, source))
        
        return imports
    
    def _extract_esm_import(self, node: Node, source: str) -> list[Import]:
        """Extract ESM import statement."""
        imports = []
        module = ""
        imported_names = []
        alias = None
        
        for child in node.children:
            if child.type == "string":
                # Remove quotes from module name
                module = self._node_text(child, source).strip("'\"")
            elif child.type == "import_clause":
                for clause_child in child.children:
                    if clause_child.type == "identifier":
                        # Default import: import foo from 'module'
                        imported_names.append(self._node_text(clause_child, source))
                    elif clause_child.type == "namespace_import":
                        # Namespace import: import * as foo from 'module'
                        alias_node = self._get_child_by_type(clause_child, ["identifier"])
                        if alias_node:
                            alias = self._node_text(alias_node, source)
                            imported_names.append("*")
                    elif clause_child.type == "named_imports":
                        # Named imports: import { a, b as c } from 'module'
                        for spec in clause_child.children:
                            if spec.type == "import_specifier":
                                name_node = self._get_child_by_type(spec, ["identifier"])
                                alias_node = self._get_child_by_type(spec, ["identifier"], skip=1)
                                if name_node:
                                    name = self._node_text(name_node, source)
                                    imported_names.append(name)
        
        if module:
            imports.append(Import(
                module=module,
                alias=alias,
                imported_names=imported_names,
                is_relative=module.startswith("."),
                line_number=node.start_point[0] + 1,
                import_type="esm"
            ))
        
        return imports
    
    def _extract_commonjs_require(self, node: Node, source: str) -> list[Import]:
        """Extract CommonJS require() calls from variable declarations."""
        imports = []
        
        for child in node.children:
            if child.type == "variable_declarator":
                name_node = self._get_child_by_type(child, ["identifier", "object_pattern", "array_pattern"])
                value_node = self._get_child_by_type(child, ["call_expression"])
                
                if value_node:
                    # Check if it's a require call
                    callee = self._get_child_by_type(value_node, ["identifier"])
                    if callee and self._node_text(callee, source) == "require":
                        args = self._get_child_by_type(value_node, ["arguments"])
                        if args:
                            string_arg = self._get_child_by_type(args, ["string"])
                            if string_arg:
                                module = self._node_text(string_arg, source).strip("'\"")
                                imported_names = []
                                alias = None
                                
                                if name_node:
                                    if name_node.type == "identifier":
                                        alias = self._node_text(name_node, source)
                                    elif name_node.type == "object_pattern":
                                        # Destructuring: const { a, b } = require('module')
                                        for prop in name_node.children:
                                            if prop.type == "shorthand_property_identifier_pattern":
                                                imported_names.append(self._node_text(prop, source))
                                            elif prop.type == "pair_pattern":
                                                key = self._get_child_by_type(prop, ["property_identifier"])
                                                if key:
                                                    imported_names.append(self._node_text(key, source))
                                
                                imports.append(Import(
                                    module=module,
                                    alias=alias,
                                    imported_names=imported_names,
                                    is_relative=module.startswith("."),
                                    line_number=node.start_point[0] + 1,
                                    import_type="commonjs"
                                ))
        
        return imports
    
    def _extract_function(
        self, 
        node: Node, 
        source: str, 
        parent_name: str | None,
        decorators: list[str] | None = None
    ) -> Symbol | None:
        """Extract function declaration."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Check if async
        is_async = any(c.type == "async" for c in node.children)
        
        # Check if generator
        is_generator = any(c.type == "*" for c in node.children)
        
        # Get parameters
        params_node = self._get_child_by_type(node, ["formal_parameters"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        # Build signature
        params_str = self._node_text(params_node, source) if params_node else "()"
        prefix = "async " if is_async else ""
        gen_mark = "*" if is_generator else ""
        signature = f"{prefix}function{gen_mark} {name}{params_str}"
        
        # Get JSDoc comment if present
        docstring = self._get_jsdoc(node, source)
        
        # Check if this is a React component (PascalCase + returns JSX)
        symbol_type = "method" if parent_name else "function"
        body = self._get_child_by_type(node, ["statement_block"])
        if self._is_pascal_case(name) and body and self._contains_jsx(body, source):
            symbol_type = "component"
        
        return Symbol(
            name=name,
            type=symbol_type,
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            parameters=parameters,
            decorators=decorators or [],
            is_async=is_async,
            is_generator=is_generator
        )
    
    def _extract_arrow_function(
        self, 
        node: Node, 
        source: str, 
        name: str,
        parent_name: str | None = None
    ) -> Symbol | None:
        """Extract arrow function expression."""
        # Check if async
        is_async = node.parent and node.parent.type == "await_expression"
        
        # Check the actual arrow function node
        arrow_node = node
        if node.type != "arrow_function":
            arrow_node = self._get_child_by_type(node, ["arrow_function"])
            if not arrow_node:
                return None
        
        # Check async in arrow function
        is_async = any(c.type == "async" for c in (node.parent.children if node.parent else []))
        
        # Get parameters
        params_node = self._get_child_by_type(arrow_node, ["formal_parameters", "identifier"])
        if params_node and params_node.type == "identifier":
            params_str = f"({self._node_text(params_node, source)})"
            parameters = [{"name": self._node_text(params_node, source)}]
        elif params_node:
            params_str = self._node_text(params_node, source)
            parameters = self._extract_parameters(params_node, source)
        else:
            params_str = "()"
            parameters = []
        
        prefix = "async " if is_async else ""
        signature = f"{prefix}{name} = {params_str} =>"
        
        # Get JSDoc from parent
        docstring = self._get_jsdoc(node.parent if node.parent else node, source)
        
        # Check if React component
        symbol_type = "method" if parent_name else "function"
        body = self._get_child_by_type(arrow_node, ["statement_block", "jsx_element", "jsx_self_closing_element", "jsx_fragment"])
        if self._is_pascal_case(name) and body and (body.type.startswith("jsx") or self._contains_jsx(body, source)):
            symbol_type = "component"
        
        return Symbol(
            name=name,
            type=symbol_type,
            signature=signature,
            docstring=docstring,
            start_line=arrow_node.start_point[0] + 1,
            end_line=arrow_node.end_point[0] + 1,
            parent_name=parent_name,
            parameters=parameters,
            is_async=is_async
        )
    
    def _extract_class(self, node: Node, source: str) -> tuple[Symbol | None, list[Symbol]]:
        """Extract class declaration and its methods."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None, []
        
        name = self._node_text(name_node, source)
        
        # Get extends clause
        bases = []
        heritage = self._get_child_by_type(node, ["class_heritage"])
        if heritage:
            extends = self._get_child_by_type(heritage, ["identifier", "member_expression"])
            if extends:
                bases.append(self._node_text(extends, source))
        
        # Build signature
        signature = f"class {name}"
        if bases:
            signature += f" extends {', '.join(bases)}"
        
        docstring = self._get_jsdoc(node, source)
        
        class_symbol = Symbol(
            name=name,
            type="class",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parameters=[{"base": b} for b in bases]
        )
        
        # Extract methods
        methods = []
        body = self._get_child_by_type(node, ["class_body"])
        if body:
            for child in body.children:
                if child.type == "method_definition":
                    method = self._extract_method(child, source, name)
                    if method:
                        methods.append(method)
                elif child.type == "field_definition":
                    # Class field (may be arrow function)
                    field = self._extract_class_field(child, source, name)
                    if field:
                        methods.append(field)
        
        return class_symbol, methods
    
    def _extract_method(self, node: Node, source: str, class_name: str) -> Symbol | None:
        """Extract class method."""
        name_node = self._get_child_by_type(node, ["property_identifier", "computed_property_name"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        if name_node.type == "computed_property_name":
            name = f"[{name}]"
        
        # Check modifiers
        is_static = any(c.type == "static" for c in node.children)
        is_async = any(c.type == "async" for c in node.children)
        is_getter = any(c.type == "get" for c in node.children)
        is_setter = any(c.type == "set" for c in node.children)
        is_generator = any(c.type == "*" for c in node.children)
        
        # Get parameters
        params_node = self._get_child_by_type(node, ["formal_parameters"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        params_str = self._node_text(params_node, source) if params_node else "()"
        
        # Build signature
        parts = []
        if is_static:
            parts.append("static")
        if is_async:
            parts.append("async")
        if is_getter:
            parts.append("get")
        if is_setter:
            parts.append("set")
        if is_generator:
            parts.append("*")
        parts.append(f"{name}{params_str}")
        signature = " ".join(parts)
        
        docstring = self._get_jsdoc(node, source)
        
        decorators = []
        # Check for decorators (experimental syntax)
        prev = node.prev_sibling
        while prev and prev.type == "decorator":
            decorators.insert(0, self._node_text(prev, source))
            prev = prev.prev_sibling
        
        return Symbol(
            name=name,
            type="method",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=class_name,
            parameters=parameters,
            decorators=decorators,
            is_async=is_async,
            is_generator=is_generator
        )
    
    def _extract_class_field(self, node: Node, source: str, class_name: str) -> Symbol | None:
        """Extract class field (may be arrow function)."""
        name_node = self._get_child_by_type(node, ["property_identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Check if it's an arrow function
        value_node = None
        for child in node.children:
            if child.type == "arrow_function":
                value_node = child
                break
        
        if value_node:
            return self._extract_arrow_function(value_node, source, name, class_name)
        
        return None
    
    def _extract_variable_declaration(
        self, 
        node: Node, 
        source: str, 
        parent_name: str | None
    ) -> list[Symbol]:
        """Extract function/class from variable declarations."""
        symbols = []
        
        for child in node.children:
            if child.type == "variable_declarator":
                name_node = self._get_child_by_type(child, ["identifier"])
                if not name_node:
                    continue
                
                name = self._node_text(name_node, source)
                
                # Check the value
                for value_child in child.children:
                    if value_child.type == "arrow_function":
                        symbol = self._extract_arrow_function(value_child, source, name, parent_name)
                        if symbol:
                            symbols.append(symbol)
                    elif value_child.type == "function_expression":
                        symbol = self._extract_function_expression(value_child, source, name, parent_name)
                        if symbol:
                            symbols.append(symbol)
                    elif value_child.type == "class_expression":
                        symbol, methods = self._extract_class_expression(value_child, source, name)
                        if symbol:
                            symbols.append(symbol)
                            symbols.extend(methods)
        
        return symbols
    
    def _extract_function_expression(
        self, 
        node: Node, 
        source: str, 
        name: str,
        parent_name: str | None = None
    ) -> Symbol | None:
        """Extract function expression."""
        is_async = any(c.type == "async" for c in (node.parent.children if node.parent else []))
        is_generator = any(c.type == "*" for c in node.children)
        
        params_node = self._get_child_by_type(node, ["formal_parameters"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        params_str = self._node_text(params_node, source) if params_node else "()"
        
        prefix = "async " if is_async else ""
        gen_mark = "*" if is_generator else ""
        signature = f"{prefix}function{gen_mark} {name}{params_str}"
        
        docstring = self._get_jsdoc(node.parent if node.parent else node, source)
        
        symbol_type = "method" if parent_name else "function"
        body = self._get_child_by_type(node, ["statement_block"])
        if self._is_pascal_case(name) and body and self._contains_jsx(body, source):
            symbol_type = "component"
        
        return Symbol(
            name=name,
            type=symbol_type,
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            parameters=parameters,
            is_async=is_async,
            is_generator=is_generator
        )
    
    def _extract_class_expression(
        self, 
        node: Node, 
        source: str, 
        name: str
    ) -> tuple[Symbol | None, list[Symbol]]:
        """Extract class expression."""
        # Similar to class declaration but with provided name
        bases = []
        heritage = self._get_child_by_type(node, ["class_heritage"])
        if heritage:
            extends = self._get_child_by_type(heritage, ["identifier", "member_expression"])
            if extends:
                bases.append(self._node_text(extends, source))
        
        signature = f"class {name}"
        if bases:
            signature += f" extends {', '.join(bases)}"
        
        docstring = self._get_jsdoc(node.parent if node.parent else node, source)
        
        class_symbol = Symbol(
            name=name,
            type="class",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parameters=[{"base": b} for b in bases]
        )
        
        methods = []
        body = self._get_child_by_type(node, ["class_body"])
        if body:
            for child in body.children:
                if child.type == "method_definition":
                    method = self._extract_method(child, source, name)
                    if method:
                        methods.append(method)
        
        return class_symbol, methods
    
    def _extract_export(self, node: Node, source: str, symbols: list[Symbol]) -> None:
        """Extract exported declarations."""
        for child in node.children:
            if child.type == "function_declaration":
                symbol = self._extract_function(child, source, None)
                if symbol:
                    symbol.is_exported = True
                    symbols.append(symbol)
            elif child.type == "class_declaration":
                symbol, methods = self._extract_class(child, source)
                if symbol:
                    symbol.is_exported = True
                    symbols.append(symbol)
                    symbols.extend(methods)
            elif child.type == "lexical_declaration":
                extracted = self._extract_variable_declaration(child, source, None)
                for s in extracted:
                    s.is_exported = True
                symbols.extend(extracted)
    
    def _extract_expression_declaration(
        self, 
        node: Node, 
        source: str, 
        parent_name: str | None,
        symbols: list[Symbol]
    ) -> None:
        """Extract declarations from expression statements (e.g., module.exports = ...)."""
        expr = node.children[0] if node.children else None
        if not expr or expr.type != "assignment_expression":
            return
        
        left = self._get_child_by_type(expr, ["member_expression", "identifier"])
        right = self._get_child_by_type(expr, ["function_expression", "arrow_function", "class_expression", "object"])
        
        if not left or not right:
            return
        
        left_text = self._node_text(left, source)
        
        # Handle module.exports = function/class
        if left_text == "module.exports" or left_text.startswith("exports."):
            if left_text.startswith("exports."):
                name = left_text.split(".", 1)[1]
            else:
                name = "default"
            
            if right.type == "function_expression":
                symbol = self._extract_function_expression(right, source, name, parent_name)
                if symbol:
                    symbol.is_exported = True
                    symbols.append(symbol)
            elif right.type == "arrow_function":
                symbol = self._extract_arrow_function(right, source, name, parent_name)
                if symbol:
                    symbol.is_exported = True
                    symbols.append(symbol)
            elif right.type == "class_expression":
                symbol, methods = self._extract_class_expression(right, source, name)
                if symbol:
                    symbol.is_exported = True
                    symbols.append(symbol)
                    symbols.extend(methods)
    
    def _extract_parameters(self, params_node: Node, source: str) -> list[dict]:
        """Extract function parameters."""
        parameters = []
        
        if not params_node:
            return parameters
        
        for child in params_node.children:
            if child.type in ("identifier", "rest_pattern", "assignment_pattern", "object_pattern", "array_pattern"):
                param = {"name": "", "type": None, "default": None}
                
                if child.type == "identifier":
                    param["name"] = self._node_text(child, source)
                elif child.type == "rest_pattern":
                    inner = self._get_child_by_type(child, ["identifier"])
                    param["name"] = f"...{self._node_text(inner, source)}" if inner else "...args"
                elif child.type == "assignment_pattern":
                    left = child.children[0] if child.children else None
                    right = child.children[2] if len(child.children) > 2 else None
                    if left:
                        param["name"] = self._node_text(left, source)
                    if right:
                        param["default"] = self._node_text(right, source)
                elif child.type in ("object_pattern", "array_pattern"):
                    param["name"] = self._node_text(child, source)
                
                if param["name"]:
                    parameters.append(param)
        
        return parameters
    
    def _get_jsdoc(self, node: Node, source: str) -> str | None:
        """Extract JSDoc comment preceding a node."""
        # Look for comment in preceding siblings
        prev = node.prev_sibling
        while prev:
            if prev.type == "comment":
                text = self._node_text(prev, source)
                if text.startswith("/**"):
                    # Clean JSDoc
                    lines = text.split("\n")
                    cleaned = []
                    for line in lines:
                        line = line.strip()
                        if line.startswith("/**"):
                            line = line[3:]
                        elif line.startswith("*/"):
                            line = line[:-2]
                        elif line.startswith("*"):
                            line = line[1:].strip()
                        if line:
                            cleaned.append(line)
                    return "\n".join(cleaned) if cleaned else None
                break
            elif prev.type not in ("", "\n"):
                break
            prev = prev.prev_sibling
        return None
    
    def _contains_jsx(self, node: Node, source: str) -> bool:
        """Check if a node contains JSX elements."""
        if node.type.startswith("jsx"):
            return True
        for child in node.children:
            if self._contains_jsx(child, source):
                return True
        return False
    
    def _extract_calls_from_symbols(
        self, 
        symbols: list[Symbol], 
        source: str, 
        imports: list[Import]
    ) -> list[FunctionCall]:
        """Extract function calls from symbols."""
        calls: list[FunctionCall] = []
        lines = source.split("\n")
        
        # Build import lookup
        imported_names = self._build_import_lookup(imports)
        
        # Build class-to-methods mapping
        class_methods: dict[str, set[str]] = {}
        for symbol in symbols:
            if symbol.type == "method" and symbol.parent_name:
                if symbol.parent_name not in class_methods:
                    class_methods[symbol.parent_name] = set()
                class_methods[symbol.parent_name].add(symbol.name)
        
        for symbol in symbols:
            if symbol.type not in ("function", "method", "component"):
                continue
            
            func_source = "\n".join(lines[symbol.start_line - 1:symbol.end_line])
            func_tree = self.parser.parse(bytes(func_source, "utf-8"))
            
            caller_name = f"{symbol.parent_name}.{symbol.name}" if symbol.parent_name else symbol.name
            
            func_calls = self._traverse_for_calls(
                func_tree.root_node,
                func_source,
                caller_name,
                symbol.parent_name,
                class_methods,
                imported_names,
                symbol.start_line
            )
            calls.extend(func_calls)
        
        return calls
    
    def _build_import_lookup(self, imports: list[Import]) -> dict[str, str]:
        """Build lookup dict from imported names to modules."""
        lookup: dict[str, str] = {}
        
        for imp in imports:
            if imp.imported_names:
                for name in imp.imported_names:
                    if name != "*":
                        lookup[name] = imp.module
            if imp.alias:
                lookup[imp.alias] = imp.module
        
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
        """Recursively traverse AST to find function calls."""
        calls: list[FunctionCall] = []
        
        if node.type == "call_expression":
            call = self._parse_call_node(
                node, source, caller_name, parent_class,
                class_methods, imported_names, line_offset
            )
            if call:
                calls.append(call)
        elif node.type == "await_expression":
            # Handle await calls
            inner = self._get_child_by_type(node, ["call_expression"])
            if inner:
                call = self._parse_call_node(
                    inner, source, caller_name, parent_class,
                    class_methods, imported_names, line_offset
                )
                if call:
                    call.is_async_call = True
                    calls.append(call)
        elif node.type in ("jsx_element", "jsx_self_closing_element", "jsx_opening_element"):
            # Extract JSX component calls
            jsx_call = self._parse_jsx_call(node, source, caller_name, imported_names, line_offset)
            if jsx_call:
                calls.append(jsx_call)
        
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
        """Parse a call_expression node."""
        if not node.children:
            return None
        
        function_part = node.children[0]
        line_number = line_offset + node.start_point[0]
        
        # Extract arguments
        arguments: list[str] = []
        args_node = self._get_child_by_type(node, ["arguments"])
        if args_node:
            for arg in args_node.children:
                if arg.type not in ("(", ")", ","):
                    arguments.append(self._node_text(arg, source))
        
        callee_name: str = ""
        call_type: str = "function"
        is_external: bool = False
        module: str | None = None
        
        if function_part.type == "identifier":
            callee_name = self._node_text(function_part, source)
            
            if callee_name in imported_names:
                is_external = True
                module = imported_names[callee_name]
            
            if callee_name in JS_BUILTINS:
                call_type = "builtin"
        
        elif function_part.type == "member_expression":
            call_type = "method"
            
            obj_part = function_part.children[0] if function_part.children else None
            prop_part = self._get_child_by_type(function_part, ["property_identifier"])
            
            if obj_part and prop_part:
                obj_text = self._node_text(obj_part, source)
                method_name = self._node_text(prop_part, source)
                
                if obj_text == "this" and parent_class:
                    callee_name = f"{parent_class}.{method_name}"
                elif obj_text in imported_names:
                    callee_name = f"{obj_text}.{method_name}"
                    is_external = True
                    module = imported_names[obj_text]
                else:
                    callee_name = f"{obj_text}.{method_name}"
        
        elif function_part.type == "new_expression":
            # Constructor call
            call_type = "constructor"
            inner = self._get_child_by_type(function_part, ["identifier", "member_expression"])
            if inner:
                callee_name = f"new {self._node_text(inner, source)}"
        
        else:
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
    
    def _parse_jsx_call(
        self,
        node: Node,
        source: str,
        caller_name: str,
        imported_names: dict[str, str],
        line_offset: int
    ) -> FunctionCall | None:
        """Parse JSX element as a function call."""
        # Get the component name
        if node.type == "jsx_self_closing_element":
            name_node = self._get_child_by_type(node, ["identifier", "member_expression", "jsx_identifier"])
        elif node.type == "jsx_opening_element":
            name_node = self._get_child_by_type(node, ["identifier", "member_expression", "jsx_identifier"])
        else:
            # For jsx_element, look at opening element
            opening = self._get_child_by_type(node, ["jsx_opening_element"])
            if opening:
                return self._parse_jsx_call(opening, source, caller_name, imported_names, line_offset)
            return None
        
        if not name_node:
            return None
        
        component_name = self._node_text(name_node, source)
        
        # Skip HTML elements (lowercase)
        if component_name and component_name[0].islower():
            return None
        
        is_external = component_name in imported_names
        module = imported_names.get(component_name)
        
        return FunctionCall(
            caller_name=caller_name,
            callee_name=component_name,
            call_type="component",
            line_number=line_offset + node.start_point[0],
            is_external=is_external,
            module=module,
            arguments=[]
        )
    
    def _detect_patterns(
        self, 
        symbols: list[Symbol], 
        source: str, 
        calls: list[FunctionCall] | None = None
    ) -> list[Pattern]:
        """Detect patterns in JavaScript code."""
        patterns = []
        
        # Build call graph
        call_graph: dict[str, set[str]] = {}
        if calls:
            for call in calls:
                if call.caller_name not in call_graph:
                    call_graph[call.caller_name] = set()
                call_graph[call.caller_name].add(call.callee_name)
        
        lines = source.split("\n")
        
        for symbol in symbols:
            if symbol.type not in ("function", "method", "component"):
                continue
            
            symbol_full_name = f"{symbol.parent_name}.{symbol.name}" if symbol.parent_name else symbol.name
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
                        evidence_parts.append(f"keyword '{kw}' in JSDoc")
                
                if pattern_name == "recursion" and call_graph:
                    recursion_info = self._detect_recursion(symbol_full_name, call_graph)
                    if recursion_info["is_recursive"]:
                        confidence += 0.8
                        if recursion_info["is_direct"]:
                            evidence_parts.append("direct recursion detected")
                        else:
                            evidence_parts.append("indirect recursion detected")
                elif pattern_info.get("indicators") and pattern_info["indicators"](func_source, symbol.name):
                    confidence += 0.4
                    evidence_parts.append("code structure matches pattern")
                
                if confidence >= 0.5:
                    patterns.append(Pattern(
                        pattern_type="algorithm",
                        pattern_name=pattern_name,
                        confidence=min(confidence, 1.0),
                        evidence=f"{symbol.name}: {'; '.join(evidence_parts)}"
                    ))
            
            # Check JS-specific patterns
            for pattern_name, pattern_info in JS_PATTERNS.items():
                confidence = 0.0
                evidence_parts = []
                
                for kw in pattern_info["keywords"]:
                    if kw in func_source:
                        confidence += 0.4
                        evidence_parts.append(f"keyword '{kw}' found")
                
                if pattern_info.get("indicators") and pattern_info["indicators"](func_source, symbol.name):
                    confidence += 0.5
                    evidence_parts.append("code structure matches pattern")
                
                if confidence >= 0.5:
                    patterns.append(Pattern(
                        pattern_type="async_pattern" if pattern_name in ("promise_chain", "async_await", "callback") else "idiom",
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
                
                if pattern_info.get("indicators") and pattern_info["indicators"](func_source, symbol.name):
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
        """Detect recursion using call graph."""
        result = {"is_recursive": False, "is_direct": False, "cycle_path": []}
        
        if symbol_name not in call_graph:
            return result
        
        callees = call_graph.get(symbol_name, set())
        
        # Direct recursion
        if symbol_name in callees:
            return {"is_recursive": True, "is_direct": True, "cycle_path": [symbol_name, symbol_name]}
        
        # Indirect recursion (BFS)
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
