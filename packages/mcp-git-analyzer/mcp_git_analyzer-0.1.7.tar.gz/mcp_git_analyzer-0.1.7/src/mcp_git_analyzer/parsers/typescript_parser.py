"""TypeScript code parser using Tree-sitter."""


import tree_sitter_typescript as tstypescript
from tree_sitter import Language, Parser, Node

from mcp_git_analyzer.parsers.base_parser import (
    Symbol,
    Pattern,
    FunctionCall,
)
from mcp_git_analyzer.parsers.javascript_parser import JavaScriptParser


# Initialize TypeScript parser (using tsx for both .ts and .tsx)
TS_LANGUAGE = Language(tstypescript.language_tsx())
_parser = Parser(TS_LANGUAGE)


# TypeScript-specific patterns
TS_PATTERNS = {
    "generic_usage": {
        "keywords": ["<T>", "<K,", "<V>", "extends", "keyof", "infer"],
        "indicators": lambda code, name: "<" in name or "extends" in code
    },
    "type_guard": {
        "keywords": ["is ", "asserts ", "typeof", "instanceof"],
        "indicators": lambda code, name: ": " + name.split("(")[0] + " is " in code if "(" in name else False
    },
    "discriminated_union": {
        "keywords": ["kind", "type", "discriminator"],
        "indicators": lambda code, name: "switch" in code and ("kind" in code or ".type" in code)
    },
    "mapped_type": {
        "keywords": ["keyof", "in keyof", "Partial", "Required", "Readonly", "Pick", "Omit"],
        "indicators": lambda code, name: "keyof" in code or any(t in code for t in ["Partial<", "Required<", "Pick<", "Omit<"])
    },
}


class TypeScriptParser(JavaScriptParser):
    """Parse TypeScript source code using Tree-sitter."""
    
    def __init__(self):
        # Override parent's parser with TypeScript parser
        self.parser = _parser
        self._language = TS_LANGUAGE
    
    @property
    def language(self) -> str:
        return "typescript"
    
    @property
    def file_extensions(self) -> list[str]:
        return [".ts", ".tsx", ".mts", ".cts"]
    
    def _extract_symbols_recursive(
        self, 
        node: Node, 
        source: str, 
        parent_name: str | None,
        symbols: list[Symbol]
    ) -> None:
        """Recursively extract symbols including TypeScript-specific constructs."""
        for child in node.children:
            symbol = None
            child_symbols: list[Symbol] = []
            
            if child.type == "function_declaration":
                symbol = self._extract_function(child, source, parent_name)
            elif child.type == "class_declaration":
                symbol, child_symbols = self._extract_class(child, source)
            elif child.type == "interface_declaration":
                symbol = self._extract_interface(child, source)
            elif child.type == "type_alias_declaration":
                symbol = self._extract_type_alias(child, source)
            elif child.type == "enum_declaration":
                symbol = self._extract_enum(child, source)
            elif child.type in ("lexical_declaration", "variable_declaration"):
                extracted = self._extract_variable_declaration(child, source, parent_name)
                symbols.extend(extracted)
                continue
            elif child.type == "export_statement":
                self._extract_export_ts(child, source, symbols)
                continue
            elif child.type == "expression_statement":
                self._extract_expression_declaration(child, source, parent_name, symbols)
                continue
            elif child.type == "ambient_declaration":
                # Handle declare statements
                self._extract_ambient(child, source, symbols)
                continue
            
            if symbol:
                symbols.append(symbol)
                symbols.extend(child_symbols)
    
    def _extract_interface(self, node: Node, source: str) -> Symbol | None:
        """Extract TypeScript interface declaration."""
        name_node = self._get_child_by_type(node, ["type_identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Get generic type parameters
        generic_params = []
        type_params = self._get_child_by_type(node, ["type_parameters"])
        if type_params:
            generic_params = self._extract_generic_params(type_params, source)
        
        # Get extends clause
        extends = []
        extends_clause = self._get_child_by_type(node, ["extends_type_clause"])
        if extends_clause:
            for child in extends_clause.children:
                if child.type in ("type_identifier", "generic_type"):
                    extends.append(self._node_text(child, source))
        
        # Build signature
        signature = f"interface {name}"
        if generic_params:
            signature += f"<{', '.join(generic_params)}>"
        if extends:
            signature += f" extends {', '.join(extends)}"
        
        docstring = self._get_jsdoc(node, source)
        
        return Symbol(
            name=name,
            type="interface",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parameters=[{"extends": e} for e in extends],
            generic_params=generic_params
        )
    
    def _extract_type_alias(self, node: Node, source: str) -> Symbol | None:
        """Extract TypeScript type alias declaration."""
        name_node = self._get_child_by_type(node, ["type_identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Get generic type parameters
        generic_params = []
        type_params = self._get_child_by_type(node, ["type_parameters"])
        if type_params:
            generic_params = self._extract_generic_params(type_params, source)
        
        # Get the type definition
        type_def = None
        for child in node.children:
            if child.type not in ("type", "type_identifier", "type_parameters", "="):
                if child.type.endswith("_type") or child.type in ("union_type", "intersection_type", "object_type", "tuple_type"):
                    type_def = self._node_text(child, source)
                    break
        
        # Build signature
        signature = f"type {name}"
        if generic_params:
            signature += f"<{', '.join(generic_params)}>"
        if type_def:
            # Truncate if too long
            if len(type_def) > 100:
                type_def = type_def[:100] + "..."
            signature += f" = {type_def}"
        
        docstring = self._get_jsdoc(node, source)
        
        return Symbol(
            name=name,
            type="type_alias",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            generic_params=generic_params
        )
    
    def _extract_enum(self, node: Node, source: str) -> Symbol | None:
        """Extract TypeScript enum declaration."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Check if const enum
        is_const = any(c.type == "const" for c in node.children)
        
        # Build signature
        prefix = "const " if is_const else ""
        signature = f"{prefix}enum {name}"
        
        docstring = self._get_jsdoc(node, source)
        
        return Symbol(
            name=name,
            type="class",  # Treat enum as class for compatibility
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1
        )
    
    def _extract_generic_params(self, node: Node, source: str) -> list[str]:
        """Extract generic type parameters."""
        params = []
        for child in node.children:
            if child.type == "type_parameter":
                param_name = self._get_child_by_type(child, ["type_identifier"])
                if param_name:
                    param_text = self._node_text(param_name, source)
                    # Check for constraint
                    constraint = self._get_child_by_type(child, ["constraint"])
                    if constraint:
                        param_text += f" extends {self._node_text(constraint, source).replace('extends ', '')}"
                    # Check for default
                    default = self._get_child_by_type(child, ["default_type"])
                    if default:
                        param_text += f" = {self._node_text(default, source).replace('= ', '')}"
                    params.append(param_text)
        return params
    
    def _extract_function(
        self, 
        node: Node, 
        source: str, 
        parent_name: str | None,
        decorators: list[str] | None = None
    ) -> Symbol | None:
        """Extract function with TypeScript type annotations."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Check if async
        is_async = any(c.type == "async" for c in node.children)
        
        # Check if generator
        is_generator = any(c.type == "*" for c in node.children)
        
        # Get generic type parameters
        generic_params = []
        type_params = self._get_child_by_type(node, ["type_parameters"])
        if type_params:
            generic_params = self._extract_generic_params(type_params, source)
        
        # Get parameters with types
        params_node = self._get_child_by_type(node, ["formal_parameters"])
        parameters = self._extract_ts_parameters(params_node, source) if params_node else []
        
        # Get return type
        return_type = None
        return_type_node = self._get_child_by_type(node, ["type_annotation"])
        if return_type_node:
            return_type = self._node_text(return_type_node, source).lstrip(": ")
        
        # Build signature
        params_str = self._node_text(params_node, source) if params_node else "()"
        prefix = "async " if is_async else ""
        gen_mark = "*" if is_generator else ""
        signature = f"{prefix}function{gen_mark} {name}"
        if generic_params:
            signature += f"<{', '.join(generic_params)}>"
        signature += params_str
        if return_type:
            signature += f": {return_type}"
        
        docstring = self._get_jsdoc(node, source)
        
        # Check if React component
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
            return_type=return_type,
            decorators=decorators or [],
            is_async=is_async,
            is_generator=is_generator,
            generic_params=generic_params
        )
    
    def _extract_ts_parameters(self, params_node: Node, source: str) -> list[dict]:
        """Extract function parameters with TypeScript type annotations."""
        parameters = []
        
        if not params_node:
            return parameters
        
        for child in params_node.children:
            if child.type in ("required_parameter", "optional_parameter", "rest_pattern"):
                param = {"name": "", "type": None, "default": None, "optional": False}
                
                if child.type == "optional_parameter":
                    param["optional"] = True
                
                # Get parameter name
                name_node = self._get_child_by_type(child, ["identifier", "object_pattern", "array_pattern"])
                if name_node:
                    param["name"] = self._node_text(name_node, source)
                
                # Get type annotation
                type_node = self._get_child_by_type(child, ["type_annotation"])
                if type_node:
                    param["type"] = self._node_text(type_node, source).lstrip(": ")
                
                # Get default value
                for sub in child.children:
                    if sub.type == "=":
                        # Next sibling is the default value
                        idx = list(child.children).index(sub)
                        if idx + 1 < len(child.children):
                            param["default"] = self._node_text(child.children[idx + 1], source)
                        break
                
                if param["name"]:
                    parameters.append(param)
            elif child.type == "rest_pattern":
                inner = self._get_child_by_type(child, ["identifier"])
                if inner:
                    param = {
                        "name": f"...{self._node_text(inner, source)}",
                        "type": None,
                        "default": None
                    }
                    # Get type annotation
                    type_node = self._get_child_by_type(child, ["type_annotation"])
                    if type_node:
                        param["type"] = self._node_text(type_node, source).lstrip(": ")
                    parameters.append(param)
        
        return parameters
    
    def _extract_method(self, node: Node, source: str, class_name: str) -> Symbol | None:
        """Extract class method with TypeScript features."""
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
        
        # TypeScript-specific modifiers
        accessibility = None
        for mod in ["public", "private", "protected"]:
            if any(c.type == mod for c in node.children):
                accessibility = mod
                break
        
        is_abstract = any(c.type == "abstract" for c in node.children)
        is_override = any(c.type == "override" for c in node.children)
        is_readonly = any(c.type == "readonly" for c in node.children)
        
        # Get generic type parameters
        generic_params = []
        type_params = self._get_child_by_type(node, ["type_parameters"])
        if type_params:
            generic_params = self._extract_generic_params(type_params, source)
        
        # Get parameters
        params_node = self._get_child_by_type(node, ["formal_parameters"])
        parameters = self._extract_ts_parameters(params_node, source) if params_node else []
        params_str = self._node_text(params_node, source) if params_node else "()"
        
        # Get return type
        return_type = None
        return_type_node = self._get_child_by_type(node, ["type_annotation"])
        if return_type_node:
            return_type = self._node_text(return_type_node, source).lstrip(": ")
        
        # Build signature
        parts = []
        if accessibility:
            parts.append(accessibility)
        if is_static:
            parts.append("static")
        if is_abstract:
            parts.append("abstract")
        if is_override:
            parts.append("override")
        if is_readonly:
            parts.append("readonly")
        if is_async:
            parts.append("async")
        if is_getter:
            parts.append("get")
        if is_setter:
            parts.append("set")
        if is_generator:
            parts.append("*")
        
        method_sig = name
        if generic_params:
            method_sig += f"<{', '.join(generic_params)}>"
        method_sig += params_str
        if return_type:
            method_sig += f": {return_type}"
        parts.append(method_sig)
        
        signature = " ".join(parts)
        
        docstring = self._get_jsdoc(node, source)
        
        # Get decorators
        decorators = []
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
            return_type=return_type,
            decorators=decorators,
            is_async=is_async,
            is_generator=is_generator,
            generic_params=generic_params
        )
    
    def _extract_class(self, node: Node, source: str) -> tuple[Symbol | None, list[Symbol]]:
        """Extract class with TypeScript features."""
        name_node = self._get_child_by_type(node, ["type_identifier", "identifier"])
        if not name_node:
            return None, []
        
        name = self._node_text(name_node, source)
        
        # Get generic type parameters
        generic_params = []
        type_params = self._get_child_by_type(node, ["type_parameters"])
        if type_params:
            generic_params = self._extract_generic_params(type_params, source)
        
        # Get extends clause
        bases = []
        heritage = self._get_child_by_type(node, ["class_heritage"])
        if heritage:
            extends_clause = self._get_child_by_type(heritage, ["extends_clause"])
            if extends_clause:
                for child in extends_clause.children:
                    if child.type in ("identifier", "generic_type", "member_expression"):
                        bases.append(self._node_text(child, source))
        
        # Get implements clause
        implements = []
        if heritage:
            implements_clause = self._get_child_by_type(heritage, ["implements_clause"])
            if implements_clause:
                for child in implements_clause.children:
                    if child.type in ("type_identifier", "generic_type"):
                        implements.append(self._node_text(child, source))
        
        # Check modifiers
        is_abstract = any(c.type == "abstract" for c in node.children)
        
        # Build signature
        prefix = "abstract " if is_abstract else ""
        signature = f"{prefix}class {name}"
        if generic_params:
            signature += f"<{', '.join(generic_params)}>"
        if bases:
            signature += f" extends {', '.join(bases)}"
        if implements:
            signature += f" implements {', '.join(implements)}"
        
        docstring = self._get_jsdoc(node, source)
        
        class_symbol = Symbol(
            name=name,
            type="class",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parameters=[{"base": b} for b in bases] + [{"implements": i} for i in implements],
            generic_params=generic_params
        )
        
        # Extract methods and properties
        methods = []
        body = self._get_child_by_type(node, ["class_body"])
        if body:
            for child in body.children:
                if child.type == "method_definition":
                    method = self._extract_method(child, source, name)
                    if method:
                        methods.append(method)
                elif child.type in ("public_field_definition", "field_definition"):
                    field = self._extract_class_field_ts(child, source, name)
                    if field:
                        methods.append(field)
        
        return class_symbol, methods
    
    def _extract_class_field_ts(self, node: Node, source: str, class_name: str) -> Symbol | None:
        """Extract TypeScript class field (property)."""
        name_node = self._get_child_by_type(node, ["property_identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Check if it's an arrow function
        for child in node.children:
            if child.type == "arrow_function":
                return self._extract_arrow_function(child, source, name, class_name)
        
        # It's a regular property, not a method - skip for now
        # Could be extended to track class properties if needed
        return None
    
    def _extract_export_ts(self, node: Node, source: str, symbols: list[Symbol]) -> None:
        """Extract exported TypeScript declarations."""
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
            elif child.type == "interface_declaration":
                symbol = self._extract_interface(child, source)
                if symbol:
                    symbol.is_exported = True
                    symbols.append(symbol)
            elif child.type == "type_alias_declaration":
                symbol = self._extract_type_alias(child, source)
                if symbol:
                    symbol.is_exported = True
                    symbols.append(symbol)
            elif child.type == "enum_declaration":
                symbol = self._extract_enum(child, source)
                if symbol:
                    symbol.is_exported = True
                    symbols.append(symbol)
            elif child.type == "lexical_declaration":
                extracted = self._extract_variable_declaration(child, source, None)
                for s in extracted:
                    s.is_exported = True
                symbols.extend(extracted)
    
    def _extract_ambient(self, node: Node, source: str, symbols: list[Symbol]) -> None:
        """Extract ambient (declare) declarations."""
        for child in node.children:
            if child.type == "function_signature":
                symbol = self._extract_function_signature(child, source)
                if symbol:
                    symbols.append(symbol)
            elif child.type == "interface_declaration":
                symbol = self._extract_interface(child, source)
                if symbol:
                    symbols.append(symbol)
            elif child.type == "type_alias_declaration":
                symbol = self._extract_type_alias(child, source)
                if symbol:
                    symbols.append(symbol)
            elif child.type == "class_declaration":
                symbol, methods = self._extract_class(child, source)
                if symbol:
                    symbols.append(symbol)
                    symbols.extend(methods)
    
    def _extract_function_signature(self, node: Node, source: str) -> Symbol | None:
        """Extract function signature (for ambient declarations)."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Get generic type parameters
        generic_params = []
        type_params = self._get_child_by_type(node, ["type_parameters"])
        if type_params:
            generic_params = self._extract_generic_params(type_params, source)
        
        # Get parameters
        params_node = self._get_child_by_type(node, ["formal_parameters"])
        parameters = self._extract_ts_parameters(params_node, source) if params_node else []
        params_str = self._node_text(params_node, source) if params_node else "()"
        
        # Get return type
        return_type = None
        return_type_node = self._get_child_by_type(node, ["type_annotation"])
        if return_type_node:
            return_type = self._node_text(return_type_node, source).lstrip(": ")
        
        signature = f"declare function {name}"
        if generic_params:
            signature += f"<{', '.join(generic_params)}>"
        signature += params_str
        if return_type:
            signature += f": {return_type}"
        
        docstring = self._get_jsdoc(node, source)
        
        return Symbol(
            name=name,
            type="function",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parameters=parameters,
            return_type=return_type,
            generic_params=generic_params
        )
    
    def _detect_patterns(
        self, 
        symbols: list[Symbol], 
        source: str, 
        calls: list[FunctionCall] | None = None
    ) -> list[Pattern]:
        """Detect patterns including TypeScript-specific ones."""
        # Get base patterns from JavaScript parser
        patterns = super()._detect_patterns(symbols, source, calls)
        
        lines = source.split("\n")
        
        # Add TypeScript-specific pattern detection
        for symbol in symbols:
            if symbol.type not in ("function", "method", "component", "interface", "type_alias"):
                continue
            
            func_source = "\n".join(lines[symbol.start_line - 1:symbol.end_line])
            
            for pattern_name, pattern_info in TS_PATTERNS.items():
                confidence = 0.0
                evidence_parts = []
                
                for kw in pattern_info["keywords"]:
                    if kw in func_source:
                        confidence += 0.3
                        evidence_parts.append(f"keyword '{kw}' found")
                
                # Check generic usage on symbol itself
                if pattern_name == "generic_usage" and symbol.generic_params:
                    confidence += 0.5
                    evidence_parts.append(f"generic parameters: {', '.join(symbol.generic_params)}")
                
                if pattern_info.get("indicators"):
                    try:
                        if pattern_info["indicators"](func_source, symbol.name):
                            confidence += 0.4
                            evidence_parts.append("code structure matches pattern")
                    except Exception:
                        pass
                
                if confidence >= 0.5:
                    patterns.append(Pattern(
                        pattern_type="type_pattern",
                        pattern_name=pattern_name,
                        confidence=min(confidence, 1.0),
                        evidence=f"{symbol.name}: {'; '.join(evidence_parts)}"
                    ))
        
        return patterns
