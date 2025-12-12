"""Rust code parser using Tree-sitter."""

from pathlib import Path

import tree_sitter_rust as tsrust
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


# Initialize Rust parser
RUST_LANGUAGE = Language(tsrust.language())
_parser = Parser(RUST_LANGUAGE)


# Rust-specific pattern indicators (extending base patterns)
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
        "indicators": lambda code, name: ".sort(" in code or ".sort_by(" in code or ".sort_unstable(" in code
    },
    "graph_traversal": {
        **BASE_ALGORITHM_PATTERNS["graph_traversal"],
        "indicators": lambda code, name: "visited" in code.lower() and ("VecDeque" in code or "Vec" in code)
    },
    "greedy": {
        **BASE_ALGORITHM_PATTERNS["greedy"],
        "indicators": lambda code, name: ".max(" in code or ".min(" in code or "std::cmp::max" in code
    },
    "backtracking": {
        **BASE_ALGORITHM_PATTERNS["backtracking"],
        "indicators": lambda code, name: "backtrack" in code.lower() or ("pop()" in code and "push(" in code)
    },
    "iterator_pattern": {
        "keywords": ["iter", "map", "filter", "fold", "collect"],
        "indicators": lambda code, name: ".iter()" in code or ".into_iter()" in code
    },
}

DESIGN_PATTERNS = {
    **BASE_DESIGN_PATTERNS,
    "singleton": {
        **BASE_DESIGN_PATTERNS["singleton"],
        "indicators": lambda code, name: "lazy_static!" in code or "OnceCell" in code or "OnceLock" in code
    },
    "factory": {
        **BASE_DESIGN_PATTERNS["factory"],
        "indicators": lambda code, name: name == "new" or name.startswith("new_") or name.startswith("create_")
    },
    "builder": {
        "keywords": ["builder", "Builder", "build"],
        "indicators": lambda code, name: "Builder" in name or (".build()" in code and "self" in code)
    },
    "decorator_pattern": {
        **BASE_DESIGN_PATTERNS["decorator_pattern"],
        "indicators": lambda code, name: "#[" in code  # Rust uses attributes
    },
    "newtype": {
        "keywords": ["newtype", "wrapper"],
        "indicators": lambda code, name: "struct " in code and "(" in code and ");" in code
    },
    "typestate": {
        "keywords": ["state", "typestate"],
        "indicators": lambda code, name: "PhantomData" in code
    },
    "result_pattern": {
        "keywords": ["Result", "Ok", "Err", "?"],
        "indicators": lambda code, name: "Result<" in code or "Ok(" in code or "Err(" in code
    },
    "option_pattern": {
        "keywords": ["Option", "Some", "None"],
        "indicators": lambda code, name: "Option<" in code or "Some(" in code or "None" in code
    },
    "trait_object": {
        "keywords": ["dyn", "trait", "impl"],
        "indicators": lambda code, name: "dyn " in code or "impl " in code
    },
    "async_pattern": {
        "keywords": ["async", "await", "Future"],
        "indicators": lambda code, name: "async fn" in code or ".await" in code
    },
    "lifetime_pattern": {
        "keywords": ["lifetime", "'a", "'static"],
        "indicators": lambda code, name: "'" in code and "<" in code
    },
}


class RustParser(BaseParser):
    """Parse Rust source code using Tree-sitter."""
    
    def __init__(self):
        self.parser = _parser
    
    @property
    def language(self) -> str:
        return "rust"
    
    @property
    def file_extensions(self) -> list[str]:
        return [".rs"]
    
    def parse_file(self, file_path: Path) -> dict:
        """
        Parse a Rust file and extract all symbols, imports, and patterns.
        
        Args:
            file_path: Path to the Rust file
        
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
        Parse Rust source code string.
        
        Args:
            source: Rust source code
            file_name: Optional file name for context
            extract_calls: If True, extract function call graph
        
        Returns:
            Dict with symbols, imports, patterns, calls (if enabled), and metadata
        """
        tree = self.parser.parse(bytes(source, "utf-8"))
        root = tree.root_node
        
        symbols: list[Symbol] = []
        imports: list[Import] = []
        
        # Extract imports (use statements)
        imports.extend(self._extract_imports(root, source))
        
        # Extract declarations
        self._extract_declarations(root, source, symbols, None)
        
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
        """Extract all use statements."""
        imports = []
        
        for child in root.children:
            if child.type == "use_declaration":
                imports.extend(self._parse_use_declaration(child, source))
        
        return imports
    
    def _parse_use_declaration(self, node: Node, source: str) -> list[Import]:
        """Parse a use declaration node."""
        imports = []
        
        # Find the use tree (scoped_identifier, use_wildcard, use_list, etc.)
        for child in node.children:
            if child.type in ("scoped_identifier", "identifier", "use_as_clause",
                              "scoped_use_list", "use_wildcard", "use_list"):
                imports.extend(self._parse_use_tree(child, source, "", node.start_point[0] + 1))
        
        return imports
    
    def _parse_use_tree(self, node: Node, source: str, prefix: str, line_number: int) -> list[Import]:
        """Recursively parse use tree."""
        imports = []
        
        if node.type == "identifier":
            name = self._node_text(node, source)
            path = f"{prefix}::{name}" if prefix else name
            imports.append(Import(
                module=path,
                alias=None,
                imported_names=[name],
                is_relative=False,
                line_number=line_number,
                import_type="rust"
            ))
        elif node.type == "scoped_identifier":
            path = self._node_text(node, source)
            parts = path.rsplit("::", 1)
            name = parts[-1] if parts else path
            imports.append(Import(
                module=path,
                alias=None,
                imported_names=[name],
                is_relative=False,
                line_number=line_number,
                import_type="rust"
            ))
        elif node.type == "use_as_clause":
            path_node = self._get_child_by_type(node, ["scoped_identifier", "identifier"])
            alias_node = self._get_child_by_type(node, ["identifier"], skip=1)
            if path_node:
                path = self._node_text(path_node, source)
                alias = self._node_text(alias_node, source) if alias_node else None
                parts = path.rsplit("::", 1)
                name = parts[-1] if parts else path
                imports.append(Import(
                    module=path,
                    alias=alias,
                    imported_names=[name],
                    is_relative=False,
                    line_number=line_number,
                    import_type="rust"
                ))
        elif node.type == "use_wildcard":
            path = self._node_text(node, source).rstrip("::*")
            imports.append(Import(
                module=path,
                alias=None,
                imported_names=["*"],
                is_relative=False,
                line_number=line_number,
                import_type="rust"
            ))
        elif node.type == "scoped_use_list":
            # Get the path prefix
            path_node = self._get_child_by_type(node, ["scoped_identifier", "identifier", "crate", "self"])
            use_list = self._get_child_by_type(node, ["use_list"])
            
            path_prefix = ""
            if path_node:
                path_prefix = self._node_text(path_node, source)
            
            if use_list:
                for child in use_list.children:
                    if child.type not in ("{", "}", ","):
                        imports.extend(self._parse_use_tree(child, source, path_prefix, line_number))
        elif node.type == "use_list":
            for child in node.children:
                if child.type not in ("{", "}", ","):
                    imports.extend(self._parse_use_tree(child, source, prefix, line_number))
        
        return imports
    
    def _extract_declarations(self, node: Node, source: str, symbols: list[Symbol], parent_name: str | None):
        """Extract all declarations from a node."""
        for child in node.children:
            if child.type == "function_item":
                symbol = self._extract_function(child, source, parent_name)
                if symbol:
                    symbols.append(symbol)
            elif child.type == "struct_item":
                symbol = self._extract_struct(child, source)
                if symbol:
                    symbols.append(symbol)
            elif child.type == "enum_item":
                symbol = self._extract_enum(child, source)
                if symbol:
                    symbols.append(symbol)
            elif child.type == "trait_item":
                symbol = self._extract_trait(child, source)
                if symbol:
                    symbols.append(symbol)
            elif child.type == "impl_item":
                self._extract_impl(child, source, symbols)
            elif child.type == "type_item":
                symbol = self._extract_type_alias(child, source)
                if symbol:
                    symbols.append(symbol)
            elif child.type == "mod_item":
                # Extract module declarations
                mod_name = None
                name_node = self._get_child_by_type(child, ["identifier"])
                if name_node:
                    mod_name = self._node_text(name_node, source)
                
                # Check for inline module body
                body = self._get_child_by_type(child, ["declaration_list"])
                if body and mod_name:
                    self._extract_declarations(body, source, symbols, mod_name)
    
    def _extract_function(self, node: Node, source: str, parent_name: str | None) -> Symbol | None:
        """Extract function definition."""
        name_node = self._get_child_by_type(node, ["identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        
        # Get visibility
        visibility = self._extract_visibility(node, source)
        
        # Get generic parameters
        type_params = self._extract_type_params(node, source)
        
        # Get parameters
        params_node = self._get_child_by_type(node, ["parameters"])
        parameters = self._extract_parameters(params_node, source) if params_node else []
        
        # Get return type
        return_type = None
        for child in node.children:
            if child.type == "type_identifier" or child.type.endswith("_type"):
                # Check if this is after ->
                prev_sibling = child.prev_sibling
                if prev_sibling and self._node_text(prev_sibling, source) == "->":
                    return_type = self._node_text(child, source)
                    break
        
        # Check for async
        is_async = "async" in self._node_text(node, source).split("{")[0]
        
        # Build signature
        sig_parts = []
        if visibility:
            sig_parts.append(visibility)
        if is_async:
            sig_parts.append("async")
        sig_parts.append("fn")
        sig_parts.append(name)
        
        if type_params:
            sig_parts.append(f"<{', '.join(type_params)}>")
        
        params_str = self._node_text(params_node, source) if params_node else "()"
        signature = " ".join(sig_parts) + params_str
        if return_type:
            signature += f" -> {return_type}"
        
        # Get doc comment
        docstring = self._extract_doc_comment(node, source)
        
        # Get attributes
        decorators = self._extract_attributes(node, source)
        
        return Symbol(
            name=name,
            type="function" if not parent_name else "method",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            parent_name=parent_name,
            parameters=parameters,
            return_type=return_type,
            decorators=decorators,
            generic_params=type_params,
            is_async=is_async,
            is_exported=visibility == "pub"
        )
    
    def _extract_struct(self, node: Node, source: str) -> Symbol | None:
        """Extract struct definition with field details."""
        name_node = self._get_child_by_type(node, ["type_identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        visibility = self._extract_visibility(node, source)
        type_params = self._extract_type_params(node, source)
        
        sig_parts = []
        if visibility:
            sig_parts.append(visibility)
        sig_parts.append("struct")
        sig_parts.append(name)
        if type_params:
            sig_parts.append(f"<{', '.join(type_params)}>")
        
        signature = " ".join(sig_parts)
        docstring = self._extract_doc_comment(node, source)
        decorators = self._extract_attributes(node, source)
        
        # Extract struct fields
        fields = []
        body = self._get_child_by_type(node, ["field_declaration_list"])
        if body:
            for child in body.children:
                if child.type == "field_declaration":
                    field_info = self._extract_struct_field(child, source)
                    if field_info:
                        fields.append(field_info)
        
        return Symbol(
            name=name,
            type="class",  # Map struct to class for consistency
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            decorators=decorators,
            generic_params=type_params,
            is_exported=visibility == "pub",
            fields=fields
        )
    
    def _extract_struct_field(self, node: Node, source: str) -> dict | None:
        """Extract a single struct field with name, type, and visibility."""
        # Get field visibility (pub or private)
        visibility = self._extract_visibility(node, source)
        
        # Get field name
        name_node = self._get_child_by_type(node, ["field_identifier"])
        if not name_node:
            return None
        
        field_name = self._node_text(name_node, source)
        
        # Get field type
        type_node = self._get_child_by_type(node, [
            "type_identifier", "primitive_type", "generic_type", 
            "reference_type", "array_type", "tuple_type", "function_type"
        ])
        
        if type_node:
            field_type = self._node_text(type_node, source)
        else:
            # Fallback: try to extract from the full text after ':'
            text = self._node_text(node, source)
            if ":" in text:
                # Extract type after the colon
                type_part = text.split(":", 1)[1].strip()
                # Remove trailing comma if present
                field_type = type_part.rstrip(",").strip()
            else:
                field_type = "unknown"
        
        return {
            "name": field_name,
            "type": field_type,
            "visibility": visibility if visibility else "private"
        }
    
    def _extract_enum(self, node: Node, source: str) -> Symbol | None:
        """Extract enum definition."""
        name_node = self._get_child_by_type(node, ["type_identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        visibility = self._extract_visibility(node, source)
        type_params = self._extract_type_params(node, source)
        
        sig_parts = []
        if visibility:
            sig_parts.append(visibility)
        sig_parts.append("enum")
        sig_parts.append(name)
        if type_params:
            sig_parts.append(f"<{', '.join(type_params)}>")
        
        signature = " ".join(sig_parts)
        docstring = self._extract_doc_comment(node, source)
        decorators = self._extract_attributes(node, source)
        
        return Symbol(
            name=name,
            type="class",  # Map enum to class for consistency
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            decorators=decorators,
            generic_params=type_params,
            is_exported=visibility == "pub"
        )
    
    def _extract_trait(self, node: Node, source: str) -> Symbol | None:
        """Extract trait definition."""
        name_node = self._get_child_by_type(node, ["type_identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        visibility = self._extract_visibility(node, source)
        type_params = self._extract_type_params(node, source)
        
        sig_parts = []
        if visibility:
            sig_parts.append(visibility)
        sig_parts.append("trait")
        sig_parts.append(name)
        if type_params:
            sig_parts.append(f"<{', '.join(type_params)}>")
        
        signature = " ".join(sig_parts)
        docstring = self._extract_doc_comment(node, source)
        decorators = self._extract_attributes(node, source)
        
        return Symbol(
            name=name,
            type="interface",  # Map trait to interface
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            decorators=decorators,
            generic_params=type_params,
            is_exported=visibility == "pub"
        )
    
    def _extract_impl(self, node: Node, source: str, symbols: list[Symbol]):
        """Extract impl block and its methods."""
        # Get the type being implemented
        type_node = None
        trait_name = None
        
        for child in node.children:
            if child.type == "type_identifier":
                if trait_name is None:
                    # First type_identifier could be trait or self type
                    # Check if there's "for" keyword after
                    next_sibling = child.next_sibling
                    while next_sibling:
                        if self._node_text(next_sibling, source) == "for":
                            trait_name = self._node_text(child, source)
                            break
                        if next_sibling.type == "type_identifier":
                            type_node = next_sibling
                            break
                        next_sibling = next_sibling.next_sibling
                    
                    if type_node is None:
                        type_node = child
                else:
                    type_node = child
                    break
            elif child.type == "generic_type":
                type_node = child
                break
        
        if not type_node:
            return
        
        parent_name = self._node_text(type_node, source)
        # Clean generic parameters from parent name
        if "<" in parent_name:
            parent_name = parent_name.split("<")[0]
        
        # Extract methods from impl body
        body = self._get_child_by_type(node, ["declaration_list"])
        if body:
            for child in body.children:
                if child.type == "function_item":
                    method = self._extract_function(child, source, parent_name)
                    if method:
                        symbols.append(method)
    
    def _extract_type_alias(self, node: Node, source: str) -> Symbol | None:
        """Extract type alias definition."""
        name_node = self._get_child_by_type(node, ["type_identifier"])
        if not name_node:
            return None
        
        name = self._node_text(name_node, source)
        visibility = self._extract_visibility(node, source)
        type_params = self._extract_type_params(node, source)
        
        sig_parts = []
        if visibility:
            sig_parts.append(visibility)
        sig_parts.append("type")
        sig_parts.append(name)
        if type_params:
            sig_parts.append(f"<{', '.join(type_params)}>")
        
        # Get the aliased type
        aliased_type = ""
        for child in node.children:
            if child.type.endswith("_type") or child.type == "type_identifier":
                # Skip the first type_identifier (the name)
                if self._node_text(child, source) != name:
                    aliased_type = self._node_text(child, source)
                    break
        
        if aliased_type:
            sig_parts.append(f"= {aliased_type}")
        
        signature = " ".join(sig_parts)
        docstring = self._extract_doc_comment(node, source)
        
        return Symbol(
            name=name,
            type="type_alias",
            signature=signature,
            docstring=docstring,
            start_line=node.start_point[0] + 1,
            end_line=node.end_point[0] + 1,
            generic_params=type_params,
            is_exported=visibility == "pub"
        )
    
    def _extract_visibility(self, node: Node, source: str) -> str | None:
        """Extract visibility modifier."""
        vis_node = self._get_child_by_type(node, ["visibility_modifier"])
        if vis_node:
            return self._node_text(vis_node, source).strip()
        return None
    
    def _extract_type_params(self, node: Node, source: str) -> list[str]:
        """Extract generic type parameters."""
        params = []
        type_params_node = self._get_child_by_type(node, ["type_parameters"])
        if type_params_node:
            for child in type_params_node.children:
                if child.type in ("type_identifier", "constrained_type_parameter", "lifetime"):
                    params.append(self._node_text(child, source))
        return params
    
    def _extract_parameters(self, params_node: Node, source: str) -> list[dict]:
        """Extract function parameters."""
        parameters = []
        
        for child in params_node.children:
            if child.type == "parameter":
                param = {"name": "", "type": None}
                
                # Get pattern (name)
                pattern_node = self._get_child_by_type(child, ["identifier", "self"])
                if pattern_node:
                    param["name"] = self._node_text(pattern_node, source)
                
                # Get type
                for type_child in child.children:
                    if type_child.type.endswith("_type") or type_child.type == "type_identifier":
                        param["type"] = self._node_text(type_child, source)
                        break
                
                if param["name"]:
                    parameters.append(param)
            elif child.type == "self_parameter":
                param_text = self._node_text(child, source)
                parameters.append({"name": param_text, "type": "Self"})
        
        return parameters
    
    def _extract_attributes(self, node: Node, source: str) -> list[str]:
        """Extract Rust attributes (#[...])."""
        attributes = []
        
        # Look for attribute items before the node
        prev = node.prev_sibling
        while prev:
            if prev.type == "attribute_item":
                attributes.insert(0, self._node_text(prev, source).strip())
            elif prev.type not in ("line_comment", "block_comment"):
                break
            prev = prev.prev_sibling
        
        return attributes
    
    def _extract_doc_comment(self, node: Node, source: str) -> str | None:
        """Extract Rust doc comments (/// or //!)."""
        lines = source[:node.start_byte].split('\n')
        
        doc_lines = []
        for line in reversed(lines):
            stripped = line.strip()
            if stripped.startswith("///") or stripped.startswith("//!"):
                doc_lines.insert(0, stripped[3:].strip())
            elif stripped.startswith("#["):
                # Skip attributes
                continue
            elif stripped:
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
            
            symbol_full_name = f"{symbol.parent_name}::{symbol.name}" if symbol.parent_name else symbol.name
            
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
            
            # Check design patterns (including Rust-specific)
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
        
        # Build imported modules mapping
        imported_modules: dict[str, str] = {}
        for imp in imports:
            for name in imp.imported_names:
                if name != "*":
                    imported_modules[name] = imp.module
        
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
                imported_modules,
                symbol.start_line
            ))
        
        return calls
    
    def _traverse_for_calls(
        self,
        node: Node,
        source: str,
        caller_name: str,
        imported_modules: dict[str, str],
        line_offset: int
    ) -> list[FunctionCall]:
        """Traverse AST to find function calls."""
        calls: list[FunctionCall] = []
        
        if node.type == "call_expression":
            call = self._parse_call_expression(
                node, source, caller_name, imported_modules, line_offset
            )
            if call:
                calls.append(call)
        
        for child in node.children:
            calls.extend(self._traverse_for_calls(
                child, source, caller_name, imported_modules, line_offset
            ))
        
        return calls
    
    def _parse_call_expression(
        self,
        node: Node,
        source: str,
        caller_name: str,
        imported_modules: dict[str, str],
        line_offset: int
    ) -> FunctionCall | None:
        """Parse a call expression node."""
        if not node.children:
            return None
        
        function_part = node.children[0]
        line_number = line_offset + node.start_point[0]
        
        # Get arguments
        arguments: list[str] = []
        args_node = self._get_child_by_type(node, ["arguments"])
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
            callee_name = self._node_text(function_part, source)
            if callee_name in imported_modules:
                is_external = True
                module = imported_modules[callee_name]
        elif function_part.type == "scoped_identifier":
            callee_name = self._node_text(function_part, source)
            # Check if the first part is an imported module
            parts = callee_name.split("::")
            if parts and parts[0] in imported_modules:
                is_external = True
                module = imported_modules[parts[0]]
        elif function_part.type == "field_expression":
            # Method call: obj.method()
            call_type = "method"
            callee_name = self._node_text(function_part, source)
        elif function_part.type == "generic_function":
            # Function with turbofish: func::<T>()
            inner_func = self._get_child_by_type(function_part, ["identifier", "scoped_identifier", "field_expression"])
            if inner_func:
                callee_name = self._node_text(inner_func, source)
        else:
            callee_name = self._node_text(function_part, source)
        
        # Check for .await (async call)
        parent = node.parent
        if parent and parent.type == "await_expression":
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
