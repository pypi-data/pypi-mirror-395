"""Report generation tools for analyzed repositories."""

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Literal

from mcp_git_analyzer.db import Database
from mcp_git_analyzer.tools.analysis_tools import AnalysisTools
from mcp_git_analyzer.tools.search_tools import SearchTools


ReportType = Literal[
    "summary", "detailed", "dependencies", "architecture",
    "module_deps", "circular_deps", "architecture_layers", "porting_analysis",
    "api_summary"
]
OutputFormat = Literal["json", "markdown", "html"]


# Architecture layer classification patterns
LAYER_PATTERNS: dict[str, list[str]] = {
    "Presentation": ["server", "api", "views", "routes", "handlers", "controllers"],
    "Business": ["tools", "services", "use_cases", "domain", "logic"],
    "Data": ["db", "database", "repository", "storage", "models", "schema"],
    "Parsing": ["parsers", "lexer", "tokenizer", "ast"],
    "Utils": ["utils", "helpers", "common", "shared", "lib"],
    "Config": ["config", "settings", "constants"],
    "Tests": ["tests", "test_", "spec", "fixtures"],
}


class ReportTools:
    """Generate analysis reports from repository data."""
    
    def __init__(
        self, 
        db: Database, 
        analysis_tools: AnalysisTools, 
        search_tools: SearchTools
    ):
        self.db = db
        self.analysis = analysis_tools
        self.search = search_tools
    
    def generate_report(
        self,
        repo_id: int,
        report_type: ReportType = "summary",
        output_format: OutputFormat = "markdown",
        save_path: str | None = None
    ) -> dict:
        """
        Generate an analysis report for a repository.
        
        Args:
            repo_id: Repository ID
            report_type: Type of report to generate
                - "summary": High-level overview with key statistics
                - "detailed": Full analysis with all symbols and patterns
                - "dependencies": Focus on imports and external dependencies
                - "architecture": Class hierarchy and call graph visualization
            output_format: Output format ("json", "markdown", "html")
            save_path: Optional file path to save the report
        
        Returns:
            Dict with status, report content, and save location if applicable
        """
        # Get repository summary as base data
        summary = self.analysis.get_repo_summary(repo_id)
        if summary.get("status") != "success":
            return summary
        
        # Generate report data based on type
        if report_type == "summary":
            report_data = self._generate_summary_report(repo_id, summary)
        elif report_type == "detailed":
            report_data = self._generate_detailed_report(repo_id, summary)
        elif report_type == "dependencies":
            report_data = self._generate_dependency_report(repo_id, summary)
        elif report_type == "architecture":
            report_data = self._generate_architecture_report(repo_id, summary)
        elif report_type == "module_deps":
            report_data = self._generate_module_dependency_report(repo_id, summary)
        elif report_type == "circular_deps":
            report_data = self._generate_circular_dependency_report(repo_id, summary)
        elif report_type == "architecture_layers":
            report_data = self._generate_architecture_layers_report(repo_id, summary)
        elif report_type == "porting_analysis":
            report_data = self._generate_porting_analysis_report(repo_id, summary)
        elif report_type == "api_summary":
            report_data = self._generate_api_summary_report(repo_id, summary)
        else:
            return {"status": "error", "message": f"Unknown report type: {report_type}"}
        
        # Format report
        if output_format == "json":
            report_content = self._format_as_json(report_data)
        elif output_format == "markdown":
            report_content = self._format_as_markdown(report_data, report_type)
        elif output_format == "html":
            report_content = self._format_as_html(report_data, report_type)
        else:
            return {"status": "error", "message": f"Unknown output format: {output_format}"}
        
        result = {
            "status": "success",
            "report_type": report_type,
            "output_format": output_format,
            "report": report_content,
            "saved_to": None
        }
        
        # Save to file if path provided
        if save_path:
            try:
                save_result = self._save_report(report_content, save_path, output_format)
                result["saved_to"] = save_result
            except Exception as e:
                result["save_error"] = str(e)
        
        return result
    
    def _generate_summary_report(self, repo_id: int, summary: dict) -> dict:
        """Generate high-level summary report data."""
        repo = summary.get("repository", {})
        
        return {
            "title": f"Repository Analysis Summary: {repo.get('name', 'Unknown')}",
            "generated_at": datetime.now().isoformat(),
            "repository": {
                "id": repo.get("id"),
                "name": repo.get("name"),
                "url": repo.get("url"),
                "last_analyzed": repo.get("last_analyzed")
            },
            "overview": {
                "languages": summary.get("languages", []),
                "total_files": sum(lang.get("file_count", 0) for lang in summary.get("languages", [])),
                "total_lines": sum(lang.get("total_lines", 0) for lang in summary.get("languages", []))
            },
            "symbols": {
                "counts": summary.get("symbol_counts", {}),
                "total": sum(summary.get("symbol_counts", {}).values())
            },
            "patterns": {
                "top_patterns": summary.get("top_patterns", [])[:5]
            },
            "key_classes": summary.get("key_classes", [])[:5]
        }
    
    def _generate_detailed_report(self, repo_id: int, summary: dict) -> dict:
        """Generate detailed report with all symbols and patterns."""
        repo = summary.get("repository", {})
        
        # Get all symbols
        all_symbols = self.search.list_symbols(repo_id, "all", limit=1000)
        symbols_list = all_symbols.get("symbols", [])
        
        # Get all patterns
        all_patterns = self.search.find_patterns("all", repo_id=repo_id)
        patterns_list = all_patterns.get("patterns", [])
        
        # Get all imports
        all_imports = self.search.find_imports(repo_id=repo_id, limit=500)
        imports_list = all_imports.get("imports", [])
        
        # Get call graph
        call_graph = self.analysis.get_call_graph(repo_id, output_format="json")
        
        return {
            "title": f"Detailed Repository Analysis: {repo.get('name', 'Unknown')}",
            "generated_at": datetime.now().isoformat(),
            "repository": {
                "id": repo.get("id"),
                "name": repo.get("name"),
                "url": repo.get("url"),
                "last_analyzed": repo.get("last_analyzed")
            },
            "overview": {
                "languages": summary.get("languages", []),
                "total_files": sum(lang.get("file_count", 0) for lang in summary.get("languages", [])),
                "total_lines": sum(lang.get("total_lines", 0) for lang in summary.get("languages", []))
            },
            "symbols": {
                "counts": summary.get("symbol_counts", {}),
                "total": sum(summary.get("symbol_counts", {}).values()),
                "all_symbols": symbols_list
            },
            "patterns": {
                "summary": summary.get("top_patterns", []),
                "all_patterns": patterns_list
            },
            "imports": {
                "summary": summary.get("top_imports", []),
                "all_imports": imports_list
            },
            "call_graph": {
                "nodes": call_graph.get("nodes", []),
                "edges": call_graph.get("edges", []),
                "statistics": call_graph.get("statistics", {})
            },
            "key_classes": summary.get("key_classes", [])
        }
    
    def _generate_dependency_report(self, repo_id: int, summary: dict) -> dict:
        """Generate dependency-focused report."""
        repo = summary.get("repository", {})
        
        # Get all imports
        all_imports = self.search.find_imports(repo_id=repo_id, limit=500)
        imports_list = all_imports.get("imports", [])
        
        # Analyze external dependencies
        external_deps: dict[str, dict] = {}
        internal_deps: dict[str, dict] = {}
        
        for imp in imports_list:
            module = imp.get("module", "")
            is_relative = imp.get("is_relative", False)
            
            if is_relative:
                if module not in internal_deps:
                    internal_deps[module] = {"module": module, "count": 0, "files": []}
                internal_deps[module]["count"] += 1
                if imp.get("file_path") not in internal_deps[module]["files"]:
                    internal_deps[module]["files"].append(imp.get("file_path"))
            else:
                # Classify as standard library or third-party
                base_module = module.split(".")[0] if module else ""
                if base_module not in external_deps:
                    external_deps[base_module] = {
                        "module": base_module,
                        "count": 0,
                        "files": [],
                        "submodules": set()
                    }
                external_deps[base_module]["count"] += 1
                if module != base_module:
                    external_deps[base_module]["submodules"].add(module)
                if imp.get("file_path") not in external_deps[base_module]["files"]:
                    external_deps[base_module]["files"].append(imp.get("file_path"))
        
        # Convert sets to lists for JSON serialization
        for dep in external_deps.values():
            dep["submodules"] = list(dep["submodules"])
        
        # Sort by usage count
        sorted_external = sorted(
            external_deps.values(), 
            key=lambda x: x["count"], 
            reverse=True
        )
        sorted_internal = sorted(
            internal_deps.values(), 
            key=lambda x: x["count"], 
            reverse=True
        )
        
        return {
            "title": f"Dependency Analysis: {repo.get('name', 'Unknown')}",
            "generated_at": datetime.now().isoformat(),
            "repository": {
                "id": repo.get("id"),
                "name": repo.get("name"),
                "url": repo.get("url")
            },
            "summary": {
                "total_imports": len(imports_list),
                "external_modules": len(external_deps),
                "internal_modules": len(internal_deps)
            },
            "external_dependencies": sorted_external,
            "internal_dependencies": sorted_internal,
            "top_dependencies": summary.get("top_imports", [])[:10]
        }
    
    def _generate_architecture_report(self, repo_id: int, summary: dict) -> dict:
        """Generate architecture-focused report with call graph."""
        repo = summary.get("repository", {})
        
        # Get all classes with their methods
        classes_result = self.search.list_symbols(repo_id, "class", limit=500)
        classes = classes_result.get("symbols", [])
        
        # Build class hierarchy
        class_hierarchy: list[dict] = []
        for cls in classes:
            # Get methods for this class
            methods = self.db.execute(
                """SELECT s.name, s.signature, s.docstring, s.start_line, s.end_line, s.metadata
                   FROM symbols s
                   WHERE s.parent_id = ?
                   ORDER BY s.start_line""",
                (cls.get("id"),)
            )
            
            class_info = {
                "name": cls.get("name"),
                "signature": cls.get("signature"),
                "docstring": cls.get("docstring"),
                "file": cls.get("file_path"),
                "line_range": cls.get("line_range"),
                "methods": [
                    {
                        "name": m["name"],
                        "signature": m["signature"],
                        "docstring": m.get("docstring"),
                        "line_range": [m["start_line"], m["end_line"]]
                    }
                    for m in methods
                ],
                "method_count": len(methods)
            }
            class_hierarchy.append(class_info)
        
        # Sort by method count
        class_hierarchy.sort(key=lambda x: x["method_count"], reverse=True)
        
        # Get call graph in both formats
        call_graph_json = self.analysis.get_call_graph(repo_id, output_format="json")
        call_graph_mermaid = self.analysis.get_call_graph(repo_id, output_format="mermaid")
        
        # Get file structure with symbol distribution
        files_result = self.db.execute(
            """SELECT f.path, f.language, f.line_count,
                      COUNT(s.id) as symbol_count,
                      SUM(CASE WHEN s.type = 'function' THEN 1 ELSE 0 END) as function_count,
                      SUM(CASE WHEN s.type = 'class' THEN 1 ELSE 0 END) as class_count,
                      SUM(CASE WHEN s.type = 'method' THEN 1 ELSE 0 END) as method_count
               FROM files f
               LEFT JOIN symbols s ON s.file_id = f.id
               WHERE f.repo_id = ?
               GROUP BY f.id
               ORDER BY symbol_count DESC""",
            (repo_id,)
        )
        
        file_distribution = [
            {
                "path": row["path"],
                "language": row["language"],
                "line_count": row["line_count"],
                "symbol_count": row["symbol_count"] or 0,
                "function_count": row["function_count"] or 0,
                "class_count": row["class_count"] or 0,
                "method_count": row["method_count"] or 0
            }
            for row in files_result
        ]
        
        return {
            "title": f"Architecture Analysis: {repo.get('name', 'Unknown')}",
            "generated_at": datetime.now().isoformat(),
            "repository": {
                "id": repo.get("id"),
                "name": repo.get("name"),
                "url": repo.get("url")
            },
            "overview": {
                "languages": summary.get("languages", []),
                "total_classes": len(class_hierarchy),
                "total_files": len(file_distribution)
            },
            "class_hierarchy": class_hierarchy,
            "file_distribution": file_distribution,
            "call_graph": {
                "json": {
                    "nodes": call_graph_json.get("nodes", []),
                    "edges": call_graph_json.get("edges", []),
                    "statistics": call_graph_json.get("statistics", {})
                },
                "mermaid": call_graph_mermaid.get("diagram", "")
            }
        }
    
    # =========================================================================
    # Module Dependency Graph Generation
    # =========================================================================
    
    def _sanitize_node_id(self, name: str) -> str:
        """Sanitize a name for use as Mermaid node ID."""
        # Replace special characters with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        # Ensure it starts with a letter
        if sanitized and sanitized[0].isdigit():
            sanitized = 'n_' + sanitized
        return sanitized or 'unknown'
    
    def _get_module_name(self, file_path: str) -> str:
        """Extract module name from file path."""
        # Remove extension and convert path to module notation
        path = Path(file_path)
        parts = list(path.parts)
        
        # Remove file extension from last part
        if parts:
            parts[-1] = path.stem
        
        # Join with dots for module notation
        return '.'.join(parts)
    
    def _get_package_name(self, file_path: str) -> str:
        """Extract package (directory) name from file path."""
        path = Path(file_path)
        parent = path.parent
        return str(parent) if str(parent) != '.' else 'root'
    
    def _build_module_graph(
        self, 
        repo_id: int, 
        include_external: bool = False
    ) -> tuple[dict[str, dict], list[dict]]:
        """
        Build module dependency graph from imports table.
        
        Returns:
            Tuple of (nodes dict, edges list)
        """
        # Get all files and imports for the repository
        files_result = self.db.execute(
            "SELECT id, path FROM files WHERE repo_id = ?",
            (repo_id,)
        )
        file_map = {row["id"]: row["path"] for row in files_result}
        
        imports_result = self.db.execute(
            """SELECT i.file_id, i.module, i.is_relative, i.imported_names
               FROM imports i
               JOIN files f ON i.file_id = f.id
               WHERE f.repo_id = ?""",
            (repo_id,)
        )
        
        nodes: dict[str, dict] = {}
        edges: list[dict] = []
        edge_set: set[tuple[str, str]] = set()
        
        # Add all files as nodes
        for file_id, file_path in file_map.items():
            module_name = self._get_module_name(file_path)
            package = self._get_package_name(file_path)
            nodes[module_name] = {
                "name": module_name,
                "package": package,
                "file_path": file_path,
                "type": "internal"
            }
        
        # Build edges from imports
        for imp in imports_result:
            source_path = file_map.get(imp["file_id"], "")
            source_module = self._get_module_name(source_path)
            target_module = imp["module"]
            is_relative = imp["is_relative"]
            
            # For relative imports, resolve the target module
            if is_relative and source_path:
                source_package = self._get_package_name(source_path)
                if target_module:
                    target_module = f"{source_package}.{target_module}".replace('/', '.')
                else:
                    target_module = source_package.replace('/', '.')
            
            # Check if target is internal
            is_internal = any(
                target_module == self._get_module_name(fp) or
                self._get_module_name(fp).startswith(target_module + '.')
                for fp in file_map.values()
            )
            
            if not is_internal and not include_external:
                continue
            
            # Add external module as node if needed
            if not is_internal and include_external:
                base_module = target_module.split('.')[0]
                if base_module not in nodes:
                    nodes[base_module] = {
                        "name": base_module,
                        "package": "external",
                        "file_path": None,
                        "type": "external"
                    }
                target_module = base_module
            
            # Create edge if not duplicate
            edge_key = (source_module, target_module)
            if edge_key not in edge_set and source_module != target_module:
                edge_set.add(edge_key)
                edges.append({
                    "from": source_module,
                    "to": target_module,
                    "type": "internal" if is_internal else "external"
                })
        
        return nodes, edges
    
    def _generate_module_deps_mermaid(
        self, 
        nodes: dict[str, dict], 
        edges: list[dict],
        highlight_cycles: list[list[str]] | None = None
    ) -> str:
        """Generate Mermaid diagram for module dependencies."""
        lines = ["flowchart TD"]
        
        # Group nodes by package
        packages: dict[str, list[str]] = defaultdict(list)
        for name, info in nodes.items():
            packages[info["package"]].append(name)
        
        # Create subgraphs for packages
        for package, module_names in sorted(packages.items()):
            if package == "external":
                lines.append("    subgraph External[\"📦 External Dependencies\"]")
            elif package == "root":
                lines.append("    subgraph Root[\"📁 Root\"]")
            else:
                safe_package = self._sanitize_node_id(package)
                display_name = package.replace('\\', '/')
                lines.append(f"    subgraph {safe_package}[\"{display_name}\"]")
            
            for module_name in sorted(module_names):
                node_id = self._sanitize_node_id(module_name)
                display_name = module_name.split('.')[-1]  # Show only file name
                if nodes[module_name]["type"] == "external":
                    lines.append(f"        {node_id}{{\"{display_name}\"}}")
                else:
                    lines.append(f"        {node_id}[\"{display_name}\"]")
            
            lines.append("    end")
        
        lines.append("")
        
        # Collect cycle edges for highlighting
        cycle_edges: set[tuple[str, str]] = set()
        if highlight_cycles:
            for cycle in highlight_cycles:
                for i in range(len(cycle)):
                    cycle_edges.add((cycle[i], cycle[(i + 1) % len(cycle)]))
        
        # Add edges
        edge_indices: list[int] = []
        for idx, edge in enumerate(edges):
            from_id = self._sanitize_node_id(edge["from"])
            to_id = self._sanitize_node_id(edge["to"])
            
            if edge["type"] == "external":
                lines.append(f"    {from_id} -.-> {to_id}")
            else:
                lines.append(f"    {from_id} --> {to_id}")
            
            # Track cycle edges for styling
            if (edge["from"], edge["to"]) in cycle_edges:
                edge_indices.append(idx)
        
        # Add styling for cycle edges
        if edge_indices:
            lines.append("")
            for idx in edge_indices:
                lines.append(f"    linkStyle {idx} stroke:red,stroke-width:2px")
        
        return "\n".join(lines)
    
    def _generate_module_dependency_report(
        self, 
        repo_id: int, 
        summary: dict,
        include_external: bool = False
    ) -> dict:
        """Generate module dependency graph report."""
        repo = summary.get("repository", {})
        
        nodes, edges = self._build_module_graph(repo_id, include_external)
        mermaid_diagram = self._generate_module_deps_mermaid(nodes, edges)
        
        # Calculate statistics
        internal_edges = [e for e in edges if e["type"] == "internal"]
        external_edges = [e for e in edges if e["type"] == "external"]
        
        # Find most connected modules
        incoming: dict[str, int] = defaultdict(int)
        outgoing: dict[str, int] = defaultdict(int)
        for edge in edges:
            outgoing[edge["from"]] += 1
            incoming[edge["to"]] += 1
        
        most_depended = sorted(incoming.items(), key=lambda x: x[1], reverse=True)[:5]
        most_dependent = sorted(outgoing.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "title": f"Module Dependency Graph: {repo.get('name', 'Unknown')}",
            "generated_at": datetime.now().isoformat(),
            "repository": {
                "id": repo.get("id"),
                "name": repo.get("name"),
                "url": repo.get("url")
            },
            "statistics": {
                "total_modules": len([n for n in nodes.values() if n["type"] == "internal"]),
                "external_modules": len([n for n in nodes.values() if n["type"] == "external"]),
                "total_dependencies": len(edges),
                "internal_dependencies": len(internal_edges),
                "external_dependencies": len(external_edges)
            },
            "most_depended_on": [{"module": m, "count": c} for m, c in most_depended],
            "most_dependent": [{"module": m, "count": c} for m, c in most_dependent],
            "nodes": list(nodes.values()),
            "edges": edges,
            "mermaid_diagram": mermaid_diagram
        }
    
    # =========================================================================
    # Circular Dependency Detection
    # =========================================================================
    
    def _detect_cycles(self, edges: list[dict]) -> list[list[str]]:
        """
        Detect circular dependencies using DFS.
        
        Returns:
            List of cycles, where each cycle is a list of module names
        """
        # Build adjacency list
        graph: dict[str, set[str]] = defaultdict(set)
        all_nodes: set[str] = set()
        
        for edge in edges:
            graph[edge["from"]].add(edge["to"])
            all_nodes.add(edge["from"])
            all_nodes.add(edge["to"])
        
        cycles: list[list[str]] = []
        visited: set[str] = set()
        rec_stack: set[str] = set()
        path: list[str] = []
        
        def dfs(node: str) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in graph.get(node, set()):
                if neighbor not in visited:
                    dfs(neighbor)
                elif neighbor in rec_stack:
                    # Found a cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    # Normalize cycle (start from smallest element)
                    min_idx = cycle.index(min(cycle[:-1]))
                    normalized = cycle[min_idx:-1] + cycle[:min_idx] + [cycle[min_idx]]
                    if normalized not in cycles:
                        cycles.append(normalized)
            
            path.pop()
            rec_stack.remove(node)
        
        for node in all_nodes:
            if node not in visited:
                dfs(node)
        
        return cycles
    
    def _generate_circular_dependency_report(
        self, 
        repo_id: int, 
        summary: dict
    ) -> dict:
        """Generate circular dependency detection report."""
        repo = summary.get("repository", {})
        
        nodes, edges = self._build_module_graph(repo_id, include_external=False)
        cycles = self._detect_cycles(edges)
        
        # Generate Mermaid diagram with highlighted cycles
        mermaid_diagram = self._generate_module_deps_mermaid(
            nodes, edges, highlight_cycles=cycles
        )
        
        # Analyze cycle severity
        cycle_info = []
        for cycle in cycles:
            cycle_info.append({
                "modules": cycle[:-1],  # Remove duplicate end node
                "length": len(cycle) - 1,
                "description": " → ".join(cycle)
            })
        
        # Sort by cycle length (longer cycles are more problematic)
        cycle_info.sort(key=lambda x: x["length"], reverse=True)
        
        return {
            "title": f"Circular Dependency Analysis: {repo.get('name', 'Unknown')}",
            "generated_at": datetime.now().isoformat(),
            "repository": {
                "id": repo.get("id"),
                "name": repo.get("name"),
                "url": repo.get("url")
            },
            "summary": {
                "has_circular_dependencies": len(cycles) > 0,
                "total_cycles": len(cycles),
                "affected_modules": len(set(
                    m for cycle in cycles for m in cycle[:-1]
                ))
            },
            "cycles": cycle_info,
            "mermaid_diagram": mermaid_diagram
        }
    
    # =========================================================================
    # Architecture Layer Diagram
    # =========================================================================
    
    def _classify_layer(self, file_path: str) -> str:
        """Classify a file into an architecture layer."""
        path_lower = file_path.lower()
        path_parts = Path(file_path).parts
        
        for layer, patterns in LAYER_PATTERNS.items():
            for pattern in patterns:
                # Check if pattern matches any part of the path
                if pattern in path_lower:
                    return layer
                # Check individual path components
                for part in path_parts:
                    if pattern in part.lower():
                        return layer
        
        return "Other"
    
    def _build_layer_graph(
        self, 
        repo_id: int
    ) -> tuple[dict[str, list[dict]], list[dict]]:
        """
        Build architecture layer graph.
        
        Returns:
            Tuple of (layers dict mapping layer name to modules, inter-layer edges)
        """
        nodes, edges = self._build_module_graph(repo_id, include_external=False)
        
        # Classify each module into a layer
        layers: dict[str, list[dict]] = defaultdict(list)
        module_to_layer: dict[str, str] = {}
        
        for module_name, info in nodes.items():
            if info["type"] == "internal" and info["file_path"]:
                layer = self._classify_layer(info["file_path"])
                layers[layer].append({
                    "name": module_name,
                    "file_path": info["file_path"]
                })
                module_to_layer[module_name] = layer
        
        # Build inter-layer edges
        layer_edges: list[dict] = []
        layer_edge_set: set[tuple[str, str]] = set()
        
        for edge in edges:
            from_layer = module_to_layer.get(edge["from"])
            to_layer = module_to_layer.get(edge["to"])
            
            if from_layer and to_layer and from_layer != to_layer:
                edge_key = (from_layer, to_layer)
                if edge_key not in layer_edge_set:
                    layer_edge_set.add(edge_key)
                    layer_edges.append({
                        "from_layer": from_layer,
                        "to_layer": to_layer,
                        "from_module": edge["from"],
                        "to_module": edge["to"]
                    })
        
        return layers, layer_edges
    
    def _generate_layer_mermaid(
        self, 
        layers: dict[str, list[dict]], 
        layer_edges: list[dict]
    ) -> str:
        """Generate Mermaid diagram for architecture layers."""
        lines = ["flowchart TB"]
        
        # Define layer order (top to bottom)
        layer_order = [
            "Presentation", "Business", "Parsing", 
            "Data", "Utils", "Config", "Tests", "Other"
        ]
        
        # Layer icons
        layer_icons = {
            "Presentation": "🌐",
            "Business": "⚙️",
            "Data": "💾",
            "Parsing": "📝",
            "Utils": "🔧",
            "Config": "⚙️",
            "Tests": "🧪",
            "Other": "📁"
        }
        
        # Create subgraphs for each layer
        for layer in layer_order:
            if layer not in layers or not layers[layer]:
                continue
            
            icon = layer_icons.get(layer, "📁")
            layer_id = self._sanitize_node_id(layer)
            lines.append(f"    subgraph {layer_id}[\"{icon} {layer} Layer\"]")
            
            for module in sorted(layers[layer], key=lambda x: x["name"]):
                module_id = self._sanitize_node_id(module["name"])
                display_name = module["name"].split('.')[-1]
                lines.append(f"        {module_id}[\"{display_name}\"]")
            
            lines.append("    end")
        
        lines.append("")
        
        # Add inter-layer edges
        seen_layer_edges: set[tuple[str, str]] = set()
        for edge in layer_edges:
            layer_pair = (edge["from_layer"], edge["to_layer"])
            if layer_pair not in seen_layer_edges:
                seen_layer_edges.add(layer_pair)
                from_id = self._sanitize_node_id(edge["from_layer"])
                to_id = self._sanitize_node_id(edge["to_layer"])
                lines.append(f"    {from_id} --> {to_id}")
        
        # Add module-level edges within diagram
        lines.append("")
        for edge in layer_edges:
            from_id = self._sanitize_node_id(edge["from_module"])
            to_id = self._sanitize_node_id(edge["to_module"])
            lines.append(f"    {from_id} -.-> {to_id}")
        
        return "\n".join(lines)
    
    def _generate_architecture_layers_report(
        self, 
        repo_id: int, 
        summary: dict
    ) -> dict:
        """Generate architecture layers diagram report."""
        repo = summary.get("repository", {})
        
        layers, layer_edges = self._build_layer_graph(repo_id)
        mermaid_diagram = self._generate_layer_mermaid(layers, layer_edges)
        
        # Calculate layer statistics
        layer_stats = []
        for layer, modules in sorted(layers.items()):
            layer_stats.append({
                "layer": layer,
                "module_count": len(modules),
                "modules": [m["name"] for m in modules]
            })
        
        # Analyze layer violations (lower layers depending on higher layers)
        layer_order = {
            "Presentation": 1, "Business": 2, "Parsing": 3,
            "Data": 4, "Utils": 5, "Config": 6, "Tests": 7, "Other": 8
        }
        
        violations = []
        for edge in layer_edges:
            from_order = layer_order.get(edge["from_layer"], 99)
            to_order = layer_order.get(edge["to_layer"], 99)
            # A violation is when a lower layer depends on a higher layer
            if from_order > to_order:
                violations.append({
                    "from_layer": edge["from_layer"],
                    "to_layer": edge["to_layer"],
                    "from_module": edge["from_module"],
                    "to_module": edge["to_module"],
                    "description": f"{edge['from_layer']} → {edge['to_layer']}"
                })
        
        return {
            "title": f"Architecture Layer Diagram: {repo.get('name', 'Unknown')}",
            "generated_at": datetime.now().isoformat(),
            "repository": {
                "id": repo.get("id"),
                "name": repo.get("name"),
                "url": repo.get("url")
            },
            "summary": {
                "total_layers": len(layers),
                "total_modules": sum(len(m) for m in layers.values()),
                "layer_dependencies": len(layer_edges),
                "layer_violations": len(violations)
            },
            "layers": layer_stats,
            "layer_dependencies": layer_edges,
            "layer_violations": violations,
            "mermaid_diagram": mermaid_diagram
        }
    
    def _generate_porting_analysis_report(
        self, 
        repo_id: int, 
        summary: dict
    ) -> dict:
        """
        Generate a porting/migration analysis report.
        
        This report is specifically designed to help AI assistants create
        accurate porting plans by providing:
        - File-by-file function listings with exact signatures
        - Exact counts (not estimates)
        - Algorithm category distribution
        - Pattern summary
        
        Response Integration:
            Use the output of this report VERBATIM in your response.
            - files_analysis[].symbols[] → List each function name and signature
            - statistics.* → Use exact numbers
            - algorithm_categories → Show distribution
        """
        repo = summary.get("repository", {})
        
        # Get all files with their symbols
        files_data = self.db.execute(
            """SELECT f.id, f.path, f.language, f.line_count
               FROM files f
               WHERE f.repo_id = ?
               ORDER BY f.path""",
            (repo_id,)
        )
        
        files_analysis = []
        total_functions = 0
        total_classes = 0
        total_methods = 0
        
        for file_row in files_data:
            file_id = file_row["id"]
            file_path = file_row["path"]
            
            # Get symbols for this file
            symbols = self.db.execute(
                """SELECT name, type, signature, docstring, start_line, end_line
                   FROM symbols
                   WHERE file_id = ?
                   ORDER BY start_line""",
                (file_id,)
            )
            
            file_symbols = []
            func_count = 0
            class_count = 0
            method_count = 0
            
            for sym in symbols:
                sym_type = sym["type"]
                if sym_type == "function":
                    func_count += 1
                    total_functions += 1
                elif sym_type == "class":
                    class_count += 1
                    total_classes += 1
                elif sym_type == "method":
                    method_count += 1
                    total_methods += 1
                
                file_symbols.append({
                    "name": sym["name"],
                    "type": sym_type,
                    "signature": sym["signature"],
                    "docstring": sym["docstring"][:200] if sym["docstring"] else None,
                    "lines": f"L{sym['start_line']}-{sym['end_line']}"
                })
            
            if file_symbols:  # Only include files with symbols
                files_analysis.append({
                    "path": file_path,
                    "language": file_row["language"],
                    "line_count": file_row["line_count"],
                    "symbol_counts": {
                        "functions": func_count,
                        "classes": class_count,
                        "methods": method_count,
                        "total": len(file_symbols)
                    },
                    "symbols": file_symbols
                })
        
        # Get algorithm categories if available
        algo_categories = self.db.execute(
            """SELECT static_category, COUNT(*) as count
               FROM core_algorithms
               WHERE repo_id = ?
               GROUP BY static_category
               ORDER BY count DESC""",
            (repo_id,)
        )
        algorithm_categories = {row["static_category"]: row["count"] for row in algo_categories}
        total_algorithms = sum(algorithm_categories.values())
        
        # Get top patterns
        patterns = self.db.execute(
            """SELECT pattern_type, pattern_name, COUNT(*) as count
               FROM patterns p
               JOIN files f ON p.file_id = f.id
               WHERE f.repo_id = ?
               GROUP BY pattern_type, pattern_name
               ORDER BY count DESC
               LIMIT 10""",
            (repo_id,)
        )
        top_patterns = [
            {"type": p["pattern_type"], "name": p["pattern_name"], "count": p["count"]}
            for p in patterns
        ]
        
        # Generate summary text (for easy inclusion in responses)
        summary_lines = [
            f"총 {len(files_analysis)}개 파일에서:",
            f"- {total_functions}개의 함수",
            f"- {total_classes}개의 클래스", 
            f"- {total_methods}개의 메서드",
        ]
        if total_algorithms > 0:
            summary_lines.append(f"- {total_algorithms}개의 알고리즘 (카테고리: {', '.join(f'{k}={v}' for k, v in algorithm_categories.items())})")
        
        return {
            "title": f"Porting Analysis Report: {repo.get('name', 'Unknown')}",
            "generated_at": datetime.now().isoformat(),
            "repository": {
                "id": repo.get("id"),
                "name": repo.get("name"),
                "url": repo.get("url")
            },
            "statistics": {
                "total_files_with_symbols": len(files_analysis),
                "total_functions": total_functions,
                "total_classes": total_classes,
                "total_methods": total_methods,
                "total_symbols": total_functions + total_classes + total_methods,
                "total_algorithms": total_algorithms
            },
            "algorithm_categories": algorithm_categories,
            "top_patterns": top_patterns,
            "files_analysis": files_analysis,
            "summary_text": "\n".join(summary_lines)
        }
    
    def _generate_api_summary_report(
        self,
        repo_id: int,
        summary: dict
    ) -> dict:
        """
        Generate a focused API summary report for library porting.
        
        This report is optimized for AI responses that need to list the
        original library's functions/types. It provides:
        - File-by-file function listing (headers prioritized)
        - Exact function signatures
        - grounded_values for validation
        - Pre-formatted markdown for direct inclusion
        
        Response Integration:
            The formatted_markdown field can be directly copied into your response.
            All values in grounded_values MUST be used exactly as provided.
        """
        repo = summary.get("repository", {})
        
        # Get public API using analysis tools
        api_result = self.analysis.get_public_api(repo_id)
        
        if api_result.get("status") != "success":
            return {
                "title": f"API Summary Report: {repo.get('name', 'Unknown')}",
                "error": api_result.get("message", "Failed to get public API"),
                "generated_at": datetime.now().isoformat()
            }
        
        # Extract data
        public_api = api_result.get("public_api", {})
        functions = public_api.get("functions", [])
        types = public_api.get("types", [])
        constants = public_api.get("constants", [])
        header_files = api_result.get("header_files", {})
        source_files = api_result.get("source_files", {})
        grounded_values = api_result.get("grounded_values", {})
        formatted_summary = api_result.get("formatted_summary", "")
        
        # Get test file analysis
        test_files = self._get_test_file_summary(repo_id)
        
        # Build comprehensive report
        return {
            "title": f"API Summary Report: {repo.get('name', 'Unknown')}",
            "generated_at": datetime.now().isoformat(),
            "repository": {
                "id": repo.get("id"),
                "name": repo.get("name"),
                "url": repo.get("url")
            },
            "grounded_values": grounded_values,
            "statistics": {
                "total_functions": len(functions),
                "total_types": len(types),
                "total_constants": len(constants),
                "header_files": len(header_files),
                "source_files": len(source_files),
                "test_files": test_files.get("count", 0)
            },
            "header_files": {
                path: {
                    "function_count": len(data.get("functions", [])),
                    "type_count": len(data.get("types", [])),
                    "functions": [
                        {"name": f["name"], "signature": f.get("signature", f["name"])}
                        for f in data.get("functions", [])
                    ],
                    "types": [
                        {"name": t["name"], "kind": t.get("kind", "type"), "field_count": len(t.get("fields", []))}
                        for t in data.get("types", [])
                    ]
                }
                for path, data in header_files.items()
            },
            "source_files": {
                path: {
                    "function_count": len(data.get("functions", [])),
                    "functions": [
                        {"name": f["name"], "signature": f.get("signature", f["name"])}
                        for f in data.get("functions", [])
                    ]
                }
                for path, data in source_files.items()
            },
            "test_analysis": test_files,
            "formatted_markdown": formatted_summary,
            "response_template": self._generate_response_template(
                repo.get("name", "Unknown"),
                len(functions),
                len(types),
                header_files
            )
        }
    
    def _get_test_file_summary(self, repo_id: int) -> dict:
        """Get summary of test files for test strategy planning."""
        test_files = self.db.execute(
            """SELECT f.path, f.line_count
               FROM files f
               WHERE f.repo_id = ?
               AND (
                   f.path LIKE '%test_%' OR
                   f.path LIKE '%_test.%' OR
                   f.path LIKE '%tests/%' OR
                   f.path LIKE '%test/%' OR
                   f.path LIKE '%.test.%'
               )
               ORDER BY f.path""",
            (repo_id,)
        )
        
        test_file_list = [{"path": f["path"], "lines": f["line_count"]} for f in test_files]
        
        return {
            "count": len(test_file_list),
            "files": test_file_list[:20],  # Limit to 20 files
            "has_more": len(test_file_list) > 20,
            "total_lines": sum(f["lines"] for f in test_file_list)
        }
    
    def _generate_response_template(
        self,
        repo_name: str,
        func_count: int,
        type_count: int,
        header_files: dict
    ) -> str:
        """Generate a response template for AI to fill in."""
        header_list = "\n".join(
            f"- `{Path(path).name}`: {len(data.get('functions', []))}개 함수"
            for path, data in sorted(header_files.items())
        )
        
        return f'''## 원본 라이브러리 분석: {repo_name}

### 통계 (grounded_values에서 추출)
- 공개 함수: **{func_count}개**
- 공개 타입: **{type_count}개**
- 헤더 파일: **{len(header_files)}개**

### 헤더 파일별 함수 목록
{header_list}

[위의 formatted_markdown을 여기에 포함]

---
**Note**: 위 숫자들은 도구 결과에서 직접 추출됨. 추측하지 말 것.
'''
    
    # =========================================================================
    # Output Formatters
    # =========================================================================
    
    def _format_as_json(self, data: dict) -> str:
        """Format report data as JSON string."""
        return json.dumps(data, indent=2, ensure_ascii=False, default=str)
    
    def _format_as_markdown(self, data: dict, report_type: ReportType) -> str:
        """Format report data as Markdown."""
        lines: list[str] = []
        
        # Header
        lines.append(f"# {data.get('title', 'Analysis Report')}")
        lines.append("")
        lines.append(f"*Generated: {data.get('generated_at', 'Unknown')}*")
        lines.append("")
        
        # Repository info
        repo = data.get("repository", {})
        lines.append("## Repository Information")
        lines.append("")
        lines.append(f"- **Name:** {repo.get('name', 'Unknown')}")
        lines.append(f"- **URL:** {repo.get('url', 'N/A')}")
        if repo.get("last_analyzed"):
            lines.append(f"- **Last Analyzed:** {repo.get('last_analyzed')}")
        lines.append("")
        
        # Type-specific sections
        if report_type == "summary":
            lines.extend(self._format_summary_sections(data))
        elif report_type == "detailed":
            lines.extend(self._format_detailed_sections(data))
        elif report_type == "dependencies":
            lines.extend(self._format_dependency_sections(data))
        elif report_type == "architecture":
            lines.extend(self._format_architecture_sections(data))
        elif report_type == "module_deps":
            lines.extend(self._format_module_deps_sections(data))
        elif report_type == "circular_deps":
            lines.extend(self._format_circular_deps_sections(data))
        elif report_type == "architecture_layers":
            lines.extend(self._format_architecture_layers_sections(data))
        elif report_type == "porting_analysis":
            lines.extend(self._format_porting_analysis_sections(data))
        
        return "\n".join(lines)
    
    def _format_summary_sections(self, data: dict) -> list[str]:
        """Format summary report sections as Markdown."""
        lines: list[str] = []
        
        # Overview
        overview = data.get("overview", {})
        lines.append("## Overview")
        lines.append("")
        lines.append(f"- **Total Files:** {overview.get('total_files', 0)}")
        lines.append(f"- **Total Lines:** {overview.get('total_lines', 0):,}")
        lines.append("")
        
        # Languages
        languages = overview.get("languages", [])
        if languages:
            lines.append("### Language Breakdown")
            lines.append("")
            lines.append("| Language | Files | Lines |")
            lines.append("|----------|-------|-------|")
            for lang in languages:
                lines.append(f"| {lang.get('language', 'Unknown')} | {lang.get('file_count', 0)} | {lang.get('total_lines', 0):,} |")
            lines.append("")
        
        # Symbols
        symbols = data.get("symbols", {})
        counts = symbols.get("counts", {})
        if counts:
            lines.append("## Symbol Statistics")
            lines.append("")
            lines.append(f"**Total Symbols:** {symbols.get('total', 0)}")
            lines.append("")
            for stype, count in counts.items():
                lines.append(f"- {stype.capitalize()}: {count}")
            lines.append("")
        
        # Top Patterns
        patterns = data.get("patterns", {}).get("top_patterns", [])
        if patterns:
            lines.append("## Top Detected Patterns")
            lines.append("")
            lines.append("| Type | Pattern | Occurrences |")
            lines.append("|------|---------|-------------|")
            for p in patterns:
                lines.append(f"| {p.get('pattern_type', '')} | {p.get('pattern_name', '')} | {p.get('count', 0)} |")
            lines.append("")
        
        # Key Classes
        key_classes = data.get("key_classes", [])
        if key_classes:
            lines.append("## Key Classes")
            lines.append("")
            for cls in key_classes:
                lines.append(f"### `{cls.get('name', 'Unknown')}`")
                lines.append("")
                lines.append(f"- **File:** `{cls.get('file_path', 'Unknown')}`")
                lines.append(f"- **Methods:** {cls.get('method_count', 0)}")
                if cls.get("docstring"):
                    lines.append(f"- **Description:** {cls.get('docstring')[:200]}...")
                lines.append("")
        
        return lines
    
    def _format_detailed_sections(self, data: dict) -> list[str]:
        """Format detailed report sections as Markdown."""
        lines: list[str] = []
        
        # Include summary sections first
        lines.extend(self._format_summary_sections(data))
        
        # All Patterns
        all_patterns = data.get("patterns", {}).get("all_patterns", [])
        if all_patterns:
            lines.append("## All Detected Patterns")
            lines.append("")
            lines.append("| Type | Pattern | Confidence | Evidence |")
            lines.append("|------|---------|------------|----------|")
            for p in all_patterns[:50]:  # Limit to 50 for readability
                evidence = p.get("evidence", "")[:50]
                lines.append(
                    f"| {p.get('pattern_type', '')} | {p.get('pattern_name', '')} | "
                    f"{p.get('confidence', 0):.2f} | {evidence}... |"
                )
            if len(all_patterns) > 50:
                lines.append(f"\n*... and {len(all_patterns) - 50} more patterns*")
            lines.append("")
        
        # All Symbols (grouped by type)
        all_symbols = data.get("symbols", {}).get("all_symbols", [])
        if all_symbols:
            lines.append("## All Symbols")
            lines.append("")
            
            # Group by type
            by_type: dict[str, list] = {}
            for sym in all_symbols:
                stype = sym.get("type", "unknown")
                if stype not in by_type:
                    by_type[stype] = []
                by_type[stype].append(sym)
            
            for stype, symbols in by_type.items():
                lines.append(f"### {stype.capitalize()}s ({len(symbols)})")
                lines.append("")
                for sym in symbols[:30]:  # Limit per type
                    lines.append(f"- `{sym.get('signature', sym.get('name', 'Unknown'))}` - `{sym.get('file_path', '')}`")
                if len(symbols) > 30:
                    lines.append(f"\n*... and {len(symbols) - 30} more {stype}s*")
                lines.append("")
        
        # Call Graph Statistics
        call_graph = data.get("call_graph", {})
        stats = call_graph.get("statistics", {})
        if stats:
            lines.append("## Call Graph Statistics")
            lines.append("")
            lines.append(f"- **Total Nodes:** {stats.get('total_nodes', 0)}")
            lines.append(f"- **Total Edges:** {stats.get('total_edges', 0)}")
            lines.append(f"- **External Calls:** {stats.get('external_calls', 0)}")
            lines.append(f"- **Resolved Calls:** {stats.get('resolved_calls', 0)}")
            lines.append("")
        
        return lines
    
    def _format_dependency_sections(self, data: dict) -> list[str]:
        """Format dependency report sections as Markdown."""
        lines: list[str] = []
        
        # Summary
        summary = data.get("summary", {})
        lines.append("## Dependency Summary")
        lines.append("")
        lines.append(f"- **Total Imports:** {summary.get('total_imports', 0)}")
        lines.append(f"- **External Modules:** {summary.get('external_modules', 0)}")
        lines.append(f"- **Internal Modules:** {summary.get('internal_modules', 0)}")
        lines.append("")
        
        # External Dependencies
        external = data.get("external_dependencies", [])
        if external:
            lines.append("## External Dependencies")
            lines.append("")
            lines.append("| Module | Usage Count | Used In Files | Submodules |")
            lines.append("|--------|-------------|---------------|------------|")
            for dep in external[:20]:
                files_count = len(dep.get("files", []))
                submodules = ", ".join(dep.get("submodules", [])[:3])
                if len(dep.get("submodules", [])) > 3:
                    submodules += "..."
                lines.append(
                    f"| {dep.get('module', '')} | {dep.get('count', 0)} | "
                    f"{files_count} | {submodules or '-'} |"
                )
            if len(external) > 20:
                lines.append(f"\n*... and {len(external) - 20} more modules*")
            lines.append("")
        
        # Internal Dependencies
        internal = data.get("internal_dependencies", [])
        if internal:
            lines.append("## Internal Dependencies")
            lines.append("")
            lines.append("| Module | Usage Count | Used In Files |")
            lines.append("|--------|-------------|---------------|")
            for dep in internal[:20]:
                files_count = len(dep.get("files", []))
                lines.append(
                    f"| {dep.get('module', '') or '(relative)'} | "
                    f"{dep.get('count', 0)} | {files_count} |"
                )
            if len(internal) > 20:
                lines.append(f"\n*... and {len(internal) - 20} more modules*")
            lines.append("")
        
        return lines
    
    def _format_architecture_sections(self, data: dict) -> list[str]:
        """Format architecture report sections as Markdown."""
        lines: list[str] = []
        
        # Overview
        overview = data.get("overview", {})
        lines.append("## Architecture Overview")
        lines.append("")
        lines.append(f"- **Total Classes:** {overview.get('total_classes', 0)}")
        lines.append(f"- **Total Files:** {overview.get('total_files', 0)}")
        lines.append("")
        
        # Languages
        languages = overview.get("languages", [])
        if languages:
            lines.append("### Language Distribution")
            lines.append("")
            for lang in languages:
                lines.append(
                    f"- **{lang.get('language', 'Unknown')}:** "
                    f"{lang.get('file_count', 0)} files, {lang.get('total_lines', 0):,} lines"
                )
            lines.append("")
        
        # Class Hierarchy
        class_hierarchy = data.get("class_hierarchy", [])
        if class_hierarchy:
            lines.append("## Class Hierarchy")
            lines.append("")
            for cls in class_hierarchy[:10]:
                lines.append(f"### `{cls.get('name', 'Unknown')}`")
                lines.append("")
                lines.append(f"- **File:** `{cls.get('file', 'Unknown')}`")
                lines.append(f"- **Lines:** {cls.get('line_range', [0, 0])[0]}-{cls.get('line_range', [0, 0])[1]}")
                lines.append(f"- **Methods:** {cls.get('method_count', 0)}")
                if cls.get("docstring"):
                    lines.append(f"- **Description:** {cls.get('docstring')[:150]}...")
                lines.append("")
                
                methods = cls.get("methods", [])
                if methods:
                    lines.append("**Methods:**")
                    lines.append("")
                    for method in methods[:10]:
                        lines.append(f"  - `{method.get('name', 'Unknown')}` (lines {method.get('line_range', [0, 0])[0]}-{method.get('line_range', [0, 0])[1]})")
                    if len(methods) > 10:
                        lines.append(f"  - *... and {len(methods) - 10} more methods*")
                    lines.append("")
            
            if len(class_hierarchy) > 10:
                lines.append(f"*... and {len(class_hierarchy) - 10} more classes*")
                lines.append("")
        
        # File Distribution
        file_distribution = data.get("file_distribution", [])
        if file_distribution:
            lines.append("## File Distribution")
            lines.append("")
            lines.append("| File | Lines | Functions | Classes | Methods |")
            lines.append("|------|-------|-----------|---------|---------|")
            for f in file_distribution[:20]:
                lines.append(
                    f"| `{f.get('path', '')}` | {f.get('line_count', 0)} | "
                    f"{f.get('function_count', 0)} | {f.get('class_count', 0)} | "
                    f"{f.get('method_count', 0)} |"
                )
            if len(file_distribution) > 20:
                lines.append(f"\n*... and {len(file_distribution) - 20} more files*")
            lines.append("")
        
        # Call Graph (Mermaid)
        mermaid = data.get("call_graph", {}).get("mermaid", "")
        if mermaid:
            lines.append("## Call Graph")
            lines.append("")
            lines.append("```mermaid")
            lines.append(mermaid)
            lines.append("```")
            lines.append("")
        
        return lines
    
    def _format_module_deps_sections(self, data: dict) -> list[str]:
        """Format module dependency report sections as Markdown."""
        lines: list[str] = []
        
        # Statistics
        stats = data.get("statistics", {})
        lines.append("## Dependency Statistics")
        lines.append("")
        lines.append(f"- **Total Modules:** {stats.get('total_modules', 0)}")
        lines.append(f"- **External Modules:** {stats.get('external_modules', 0)}")
        lines.append(f"- **Total Dependencies:** {stats.get('total_dependencies', 0)}")
        lines.append(f"- **Internal Dependencies:** {stats.get('internal_dependencies', 0)}")
        lines.append(f"- **External Dependencies:** {stats.get('external_dependencies', 0)}")
        lines.append("")
        
        # Most depended on modules
        most_depended = data.get("most_depended_on", [])
        if most_depended:
            lines.append("## Most Depended On Modules")
            lines.append("")
            lines.append("| Module | Incoming Dependencies |")
            lines.append("|--------|----------------------|")
            for mod in most_depended:
                lines.append(f"| `{mod.get('module', '')}` | {mod.get('count', 0)} |")
            lines.append("")
        
        # Most dependent modules
        most_dependent = data.get("most_dependent", [])
        if most_dependent:
            lines.append("## Most Dependent Modules")
            lines.append("")
            lines.append("| Module | Outgoing Dependencies |")
            lines.append("|--------|----------------------|")
            for mod in most_dependent:
                lines.append(f"| `{mod.get('module', '')}` | {mod.get('count', 0)} |")
            lines.append("")
        
        # Mermaid diagram
        mermaid = data.get("mermaid_diagram", "")
        if mermaid:
            lines.append("## Module Dependency Graph")
            lines.append("")
            lines.append("```mermaid")
            lines.append(mermaid)
            lines.append("```")
            lines.append("")
        
        return lines
    
    def _format_circular_deps_sections(self, data: dict) -> list[str]:
        """Format circular dependency report sections as Markdown."""
        lines: list[str] = []
        
        # Summary
        summary = data.get("summary", {})
        has_cycles = summary.get("has_circular_dependencies", False)
        
        lines.append("## Circular Dependency Summary")
        lines.append("")
        
        if has_cycles:
            lines.append("⚠️ **Circular dependencies detected!**")
            lines.append("")
            lines.append(f"- **Total Cycles:** {summary.get('total_cycles', 0)}")
            lines.append(f"- **Affected Modules:** {summary.get('affected_modules', 0)}")
        else:
            lines.append("✅ **No circular dependencies detected.**")
        lines.append("")
        
        # Cycles details
        cycles = data.get("cycles", [])
        if cycles:
            lines.append("## Detected Cycles")
            lines.append("")
            for i, cycle in enumerate(cycles, 1):
                lines.append(f"### Cycle {i}")
                lines.append("")
                lines.append(f"- **Length:** {cycle.get('length', 0)} modules")
                lines.append(f"- **Path:** `{cycle.get('description', '')}`")
                lines.append("")
        
        # Mermaid diagram
        mermaid = data.get("mermaid_diagram", "")
        if mermaid:
            lines.append("## Dependency Graph (Cycles Highlighted)")
            lines.append("")
            lines.append("*Cycle edges are shown in red*")
            lines.append("")
            lines.append("```mermaid")
            lines.append(mermaid)
            lines.append("```")
            lines.append("")
        
        return lines
    
    def _format_architecture_layers_sections(self, data: dict) -> list[str]:
        """Format architecture layers report sections as Markdown."""
        lines: list[str] = []
        
        # Summary
        summary = data.get("summary", {})
        lines.append("## Architecture Summary")
        lines.append("")
        lines.append(f"- **Total Layers:** {summary.get('total_layers', 0)}")
        lines.append(f"- **Total Modules:** {summary.get('total_modules', 0)}")
        lines.append(f"- **Layer Dependencies:** {summary.get('layer_dependencies', 0)}")
        
        violations_count = summary.get("layer_violations", 0)
        if violations_count > 0:
            lines.append(f"- ⚠️ **Layer Violations:** {violations_count}")
        else:
            lines.append("- ✅ **Layer Violations:** 0")
        lines.append("")
        
        # Layer breakdown
        layers = data.get("layers", [])
        if layers:
            lines.append("## Layer Breakdown")
            lines.append("")
            lines.append("| Layer | Module Count | Modules |")
            lines.append("|-------|--------------|---------|")
            for layer in layers:
                modules = layer.get("modules", [])
                module_preview = ", ".join(m.split(".")[-1] for m in modules[:3])
                if len(modules) > 3:
                    module_preview += f" (+{len(modules) - 3} more)"
                lines.append(
                    f"| {layer.get('layer', '')} | {layer.get('module_count', 0)} | "
                    f"{module_preview} |"
                )
            lines.append("")
        
        # Layer violations
        violations = data.get("layer_violations", [])
        if violations:
            lines.append("## ⚠️ Layer Violations")
            lines.append("")
            lines.append("*These are dependencies where a lower layer depends on a higher layer:*")
            lines.append("")
            lines.append("| From Layer | To Layer | From Module | To Module |")
            lines.append("|------------|----------|-------------|-----------|")
            for v in violations:
                lines.append(
                    f"| {v.get('from_layer', '')} | {v.get('to_layer', '')} | "
                    f"`{v.get('from_module', '').split('.')[-1]}` | "
                    f"`{v.get('to_module', '').split('.')[-1]}` |"
                )
            lines.append("")
        
        # Mermaid diagram
        mermaid = data.get("mermaid_diagram", "")
        if mermaid:
            lines.append("## Architecture Layer Diagram")
            lines.append("")
            lines.append("```mermaid")
            lines.append(mermaid)
            lines.append("```")
            lines.append("")
        
        return lines
    
    def _format_porting_analysis_sections(self, data: dict) -> list[str]:
        """Format porting analysis report sections as Markdown."""
        lines: list[str] = []
        
        # Statistics Summary
        stats = data.get("statistics", {})
        lines.append("## 통계 요약 (Statistics Summary)")
        lines.append("")
        lines.append("| 항목 | 개수 |")
        lines.append("|------|------|")
        lines.append(f"| 파일 수 | {stats.get('total_files_with_symbols', 0)} |")
        lines.append(f"| 함수 (functions) | {stats.get('total_functions', 0)} |")
        lines.append(f"| 클래스 (classes) | {stats.get('total_classes', 0)} |")
        lines.append(f"| 메서드 (methods) | {stats.get('total_methods', 0)} |")
        lines.append(f"| **총 심볼** | **{stats.get('total_symbols', 0)}** |")
        if stats.get("total_algorithms", 0) > 0:
            lines.append(f"| 알고리즘 | {stats.get('total_algorithms', 0)} |")
        lines.append("")
        
        # Algorithm Categories
        algo_cats = data.get("algorithm_categories", {})
        if algo_cats:
            lines.append("## 알고리즘 카테고리 (Algorithm Categories)")
            lines.append("")
            lines.append("| 카테고리 | 개수 |")
            lines.append("|----------|------|")
            for cat, count in sorted(algo_cats.items(), key=lambda x: -x[1]):
                lines.append(f"| {cat} | {count} |")
            lines.append("")
        
        # Top Patterns
        patterns = data.get("top_patterns", [])
        if patterns:
            lines.append("## 탐지된 패턴 (Detected Patterns)")
            lines.append("")
            lines.append("| 타입 | 패턴명 | 횟수 |")
            lines.append("|------|--------|------|")
            for p in patterns:
                lines.append(f"| {p.get('type', '')} | {p.get('name', '')} | {p.get('count', 0)} |")
            lines.append("")
        
        # File-by-file symbol listing
        files = data.get("files_analysis", [])
        if files:
            lines.append("## 파일별 심볼 목록 (Symbols by File)")
            lines.append("")
            lines.append("*아래 목록을 포팅 계획에 그대로 사용하세요.*")
            lines.append("")
            
            for file_info in files:
                path = file_info.get("path", "unknown")
                lang = file_info.get("language", "")
                counts = file_info.get("symbol_counts", {})
                
                # File header
                count_parts = []
                if counts.get("functions", 0) > 0:
                    count_parts.append(f"{counts['functions']}개 함수")
                if counts.get("classes", 0) > 0:
                    count_parts.append(f"{counts['classes']}개 클래스")
                if counts.get("methods", 0) > 0:
                    count_parts.append(f"{counts['methods']}개 메서드")
                
                lines.append(f"### `{path}` ({', '.join(count_parts) if count_parts else '심볼 없음'})")
                lines.append("")
                
                symbols = file_info.get("symbols", [])
                for sym in symbols:
                    sig = sym.get("signature", sym.get("name", "unknown"))
                    sym_type = sym.get("type", "")
                    loc = sym.get("lines", "")
                    
                    # Format based on type
                    if sym_type == "class":
                        lines.append(f"- 📦 **class** `{sig}` ({loc})")
                    elif sym_type == "function":
                        lines.append(f"- ⚡ `{sig}` ({loc})")
                    elif sym_type == "method":
                        lines.append(f"  - 🔹 `{sig}` ({loc})")
                    else:
                        lines.append(f"- `{sig}` ({loc})")
                
                lines.append("")
        
        # Summary text for copy-paste
        summary_text = data.get("summary_text", "")
        if summary_text:
            lines.append("---")
            lines.append("")
            lines.append("## 요약 텍스트 (Copy-paste ready)")
            lines.append("")
            lines.append("```")
            lines.append(summary_text)
            lines.append("```")
            lines.append("")
        
        return lines
    
    def _format_as_html(self, data: dict, report_type: ReportType) -> str:
        """Format report data as HTML."""
        # Convert Markdown to HTML with basic styling
        md_content = self._format_as_markdown(data, report_type)
        
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            "  <meta charset='UTF-8'>",
            "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
            f"  <title>{data.get('title', 'Analysis Report')}</title>",
            "  <style>",
            "    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; line-height: 1.6; }",
            "    h1 { border-bottom: 2px solid #333; padding-bottom: 10px; }",
            "    h2 { color: #2c3e50; margin-top: 30px; border-bottom: 1px solid #ddd; padding-bottom: 5px; }",
            "    h3 { color: #34495e; }",
            "    table { border-collapse: collapse; width: 100%; margin: 15px 0; }",
            "    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
            "    th { background-color: #f5f5f5; font-weight: 600; }",
            "    tr:nth-child(even) { background-color: #fafafa; }",
            "    code { background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Monaco', 'Consolas', monospace; }",
            "    pre { background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }",
            "    .mermaid { background-color: #fff; padding: 20px; }",
            "    ul { padding-left: 20px; }",
            "    em { color: #666; }",
            "  </style>",
            "  <script src='https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js'></script>",
            "  <script>mermaid.initialize({startOnLoad:true});</script>",
            "</head>",
            "<body>",
        ]
        
        # Convert Markdown to HTML (basic conversion)
        html_content = self._md_to_html(md_content)
        html_parts.append(html_content)
        
        html_parts.extend([
            "</body>",
            "</html>"
        ])
        
        return "\n".join(html_parts)
    
    def _md_to_html(self, md: str) -> str:
        """Convert basic Markdown to HTML."""
        
        lines = md.split("\n")
        html_lines: list[str] = []
        in_table = False
        in_code_block = False
        in_list = False
        
        for line in lines:
            # Code blocks
            if line.startswith("```"):
                if in_code_block:
                    if "mermaid" in html_lines[-1] if html_lines else "":
                        html_lines.append("</div>")
                    else:
                        html_lines.append("</code></pre>")
                    in_code_block = False
                else:
                    lang = line[3:].strip()
                    if lang == "mermaid":
                        html_lines.append("<div class='mermaid'>")
                    else:
                        html_lines.append(f"<pre><code class='language-{lang}'>")
                    in_code_block = True
                continue
            
            if in_code_block:
                html_lines.append(line)
                continue
            
            # Tables
            if line.startswith("|"):
                if not in_table:
                    html_lines.append("<table>")
                    in_table = True
                
                if line.replace("|", "").replace("-", "").strip() == "":
                    continue  # Skip separator line
                
                cells = [c.strip() for c in line.split("|")[1:-1]]
                if not any(html_lines[-1:]) or "<table>" in html_lines[-1]:
                    html_lines.append("<thead><tr>")
                    for cell in cells:
                        html_lines.append(f"<th>{self._inline_md(cell)}</th>")
                    html_lines.append("</tr></thead><tbody>")
                else:
                    html_lines.append("<tr>")
                    for cell in cells:
                        html_lines.append(f"<td>{self._inline_md(cell)}</td>")
                    html_lines.append("</tr>")
                continue
            elif in_table:
                html_lines.append("</tbody></table>")
                in_table = False
            
            # Headers
            if line.startswith("# "):
                html_lines.append(f"<h1>{self._inline_md(line[2:])}</h1>")
            elif line.startswith("## "):
                html_lines.append(f"<h2>{self._inline_md(line[3:])}</h2>")
            elif line.startswith("### "):
                html_lines.append(f"<h3>{self._inline_md(line[4:])}</h3>")
            # Lists
            elif line.startswith("- "):
                if not in_list:
                    html_lines.append("<ul>")
                    in_list = True
                html_lines.append(f"<li>{self._inline_md(line[2:])}</li>")
            elif line.startswith("  - "):
                html_lines.append(f"<li style='margin-left:20px'>{self._inline_md(line[4:])}</li>")
            elif in_list and line.strip() == "":
                html_lines.append("</ul>")
                in_list = False
            # Paragraphs
            elif line.strip():
                html_lines.append(f"<p>{self._inline_md(line)}</p>")
            else:
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
        
        # Close any open tags
        if in_table:
            html_lines.append("</tbody></table>")
        if in_list:
            html_lines.append("</ul>")
        
        return "\n".join(html_lines)
    
    def _inline_md(self, text: str) -> str:
        """Convert inline Markdown to HTML."""
        import re
        
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # Code
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
        
        return text
    
    def _save_report(
        self, 
        content: str, 
        save_path: str, 
        output_format: OutputFormat
    ) -> str:
        """Save report to file."""
        path = Path(save_path)
        
        # Add extension if not present
        ext_map = {"json": ".json", "markdown": ".md", "html": ".html"}
        expected_ext = ext_map.get(output_format, "")
        if not path.suffix:
            path = path.with_suffix(expected_ext)
        
        # Create directory if needed
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        path.write_text(content, encoding="utf-8")
        
        return str(path.resolve())
