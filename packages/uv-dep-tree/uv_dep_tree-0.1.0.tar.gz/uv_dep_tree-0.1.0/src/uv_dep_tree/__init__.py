#!/usr/bin/env python3
"""
uv-dep-tree: UV Lock Nested Dependency Visualizer

Creates a nested tree visualization of Python dependencies from a uv.lock file,
with weighted deduplication metrics at each node.

Each node shows:
  - self_size: Package's own wheel size
  - total_size: self + all descendants (no dedup)
  - dedup_size: self + descendants, weighted by 1/occurrence_count

The root's dedup_size equals the actual deduplicated total.

Usage:
    python main.py [path/to/uv.lock]           # Generate static HTML file
    python main.py --serve [path/to/uv.lock]   # Start live server
    python main.py --serve --port 8080         # Custom port (default: 8000)
    
Outputs an interactive HTML file: uv-deps.html
"""

import argparse
import sys
import tomllib
import threading
import time
from dataclasses import dataclass, field
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import json
from typing import Any
import webbrowser


@dataclass
class Package:
    name: str
    version: str
    size: int = 0
    dependencies: list[str] = field(default_factory=list)
    is_workspace_member: bool = False


def parse_uv_lock(lock_path: Path) -> tuple[dict[str, Package], list[str]]:
    """Parse uv.lock file and return package info with sizes."""
    
    with open(lock_path, "rb") as f:
        data = tomllib.load(f)
    
    packages: dict[str, Package] = {}
    workspace_members = data.get("manifest", {}).get("members", [])
    
    for pkg_data in data.get("package", []):
        name = pkg_data["name"]
        version = pkg_data.get("version", "0.0.0")
        deps = [d["name"] for d in pkg_data.get("dependencies", [])]
        
        # Get wheel size - prefer platform-specific
        size = 0
        wheels = pkg_data.get("wheels", [])
        
        if wheels:
            best_wheel = None
            best_priority = -1
            
            for wheel in wheels:
                url = wheel.get("url", "")
                priority = 0
                if "linux" in url and "x86_64" in url:
                    priority = 10
                elif "manylinux" in url and "x86_64" in url:
                    priority = 9
                elif "macosx" in url and ("arm64" in url or "universal" in url):
                    priority = 8
                elif "macosx" in url and "x86_64" in url:
                    priority = 7
                elif "none-any" in url or "py3-none-any" in url:
                    priority = 5
                elif "win" in url:
                    priority = 1
                else:
                    priority = 3
                
                if priority > best_priority:
                    best_priority = priority
                    best_wheel = wheel
            
            if best_wheel:
                size = best_wheel.get("size", 0)
        
        if size == 0 and "sdist" in pkg_data:
            size = pkg_data["sdist"].get("size", 0)
        
        packages[name] = Package(
            name=name,
            version=version,
            size=size,
            dependencies=deps,
            is_workspace_member=name in workspace_members,
        )
    
    return packages, workspace_members


@dataclass
class TreeNode:
    """A node in the dependency tree."""
    name: str
    version: str
    self_size: int
    children: list["TreeNode"] = field(default_factory=list)
    depth: int = 0
    # These get calculated later
    total_size: int = 0  # self + all descendants (no dedup)
    dedup_size: float = 0.0  # weighted by occurrence count
    occurrence_count: int = 1  # how many times this package appears in full tree


def build_dependency_tree(
    root_name: str,
    packages: dict[str, Package],
    visited_path: set[str] | None = None,
    depth: int = 0,
    max_depth: int = 20
) -> TreeNode | None:
    """
    Build a dependency tree starting from root_name.
    Uses visited_path to detect cycles within a single path.
    """
    if visited_path is None:
        visited_path = set()
    
    if root_name not in packages:
        return None
    
    if root_name in visited_path:
        return None  # Cycle detected
    
    if depth > max_depth:
        return None
    
    pkg = packages[root_name]
    node = TreeNode(
        name=root_name,
        version=pkg.version,
        self_size=pkg.size,
        depth=depth,
    )
    
    visited_path.add(root_name)
    for dep_name in sorted(pkg.dependencies):
        child = build_dependency_tree(
            dep_name, 
            packages, 
            visited_path.copy(),  # Copy to allow the same dep in different branches
            depth + 1,
            max_depth
        )
        if child:
            node.children.append(child)
    
    return node


def count_occurrences(node: TreeNode, counts: dict[str, int]) -> None:
    """Count how many times each package appears in the tree (recursive)."""
    counts[node.name] = counts.get(node.name, 0) + 1
    for child in node.children:
        count_occurrences(child, counts)


def calculate_sizes(node: TreeNode, occurrence_counts: dict[str, int]) -> None:
    """Calculate total_size and dedup_size for each node (recursive, post-order)."""
    for child in node.children:
        calculate_sizes(child, occurrence_counts)
    
    node.total_size = node.self_size + sum(c.total_size for c in node.children)
    node.occurrence_count = occurrence_counts.get(node.name, 1)
    node.dedup_size = node.self_size / node.occurrence_count + sum(c.dedup_size for c in node.children)


def tree_to_dict(node: TreeNode) -> dict[str, Any]:
    """Convert tree to JSON-serializable dict."""
    return {
        "name": node.name,
        "version": node.version,
        "self_size": node.self_size,
        "total_size": node.total_size,
        "dedup_size": round(node.dedup_size, 2),
        "occurrence_count": node.occurrence_count,
        "depth": node.depth,
        "children": [tree_to_dict(c) for c in node.children]
    }


def format_size(size_bytes: float) -> str:
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(size_bytes) < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def generate_html(
    trees: list[dict],
    packages: dict[str, Package],
    workspace_members: list[str],
    global_occurrence_counts: dict[str, int],
    lock_path: Path,
    output_path: Path | None = None
) -> str:
    """Generate interactive HTML visualization."""
    
    unique_packages = set()
    def collect_packages(node):
        unique_packages.add(node["name"])
        for c in node.get("children", []):
            collect_packages(c)
    for tree in trees:
        collect_packages(tree)
    
    dep_packages = unique_packages - set(workspace_members)
    total_dedup_size = sum(packages[p].size for p in dep_packages if p in packages)
    total_with_dupes = sum(
        packages[name].size * count 
        for name, count in global_occurrence_counts.items() 
        if name in packages and name not in workspace_members
    )
    
    savings = total_with_dupes - total_dedup_size
    savings_pct = (savings / total_with_dupes * 100) if total_with_dupes > 0 else 0
    max_occurrences = max(global_occurrence_counts.values()) if global_occurrence_counts else 1
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>uv.lock Dependency Visualizer</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Verdana, "Open Sans", Arial, sans-serif; background: #111; color: #ccd; line-height: 1.5; }}
        h1 {{ font-size: 20px; font-weight: 600; color: #5af; margin-bottom: 4px; }}
        .header {{ padding: 20px 24px; background: linear-gradient(180deg, #122 0%, #111 100%); border-bottom: 1px solid #334; position: sticky; top: 0; z-index: 100; }}
        .subtitle {{ font-size: 12px; color: #899; }}
        .stats {{ display: flex; gap: 24px; margin-top: 16px; flex-wrap: wrap; }}
        .stat {{ background: #223; border: 1px solid #334; border-radius: 6px; padding: 12px 16px; min-width: 140px; }}
        .stat-label {{ font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; color: #899; margin-bottom: 4px; }}
        .stat .stat-value {{ font-size: 18px; font-weight: 600; color: #fff; }}
        .stat .stat-value.green {{ color: #3b5; }}
        .stat .stat-value.blue {{ color: #5af; }}
        .stat .stat-value.orange {{ color: #da2; }}
        .legend, .tree-stats {{ display: flex; gap: 16px; font-size: 11px; color: #899; flex-wrap: wrap; }}
        .legend {{ margin-top: 16px; }}
        .tree-stats {{ flex: 1; justify-content: center; }}
        .legend-item, .node-left {{ display: flex; align-items: center; gap: 6px; }}
        .node-left {{ gap: 8px; flex-shrink: 0; }}
        .legend-bar {{ width: 40px; height: 8px; border-radius: 2px; }}
        .sort-controls {{ display: flex; align-items: center; gap: 8px; margin-left: auto; }}
        .sort-btn {{ background: #223; border: 1px solid #334; color: #899; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-family: inherit; cursor: pointer; }}
        .sort-btn:hover {{ background: #334; color: #ccd; }}
        .sort-btn.active {{ background: #284; border-color: #284; color: #fff; }}
        .trees-container {{ padding: 24px; display: flex; flex-direction: column; gap: 24px; }}
        .tree-section {{ background: #122; border: 1px solid #334; border-radius: 8px; overflow: hidden; }}
        .tree-header {{ padding: 12px 16px; background: #223; border-bottom: 1px solid #334; display: flex; align-items: center; cursor: pointer; gap: 16px; }}
        .tree-header:hover {{ background: #334; }}
        .tree-title {{ font-weight: 600; color: #5af; }}
        .tree-col-headers, .node-stats {{ display: grid; grid-template-columns: repeat(6, 70px); gap: 4px; flex-shrink: 0; }}
        .tree-col-headers span {{ grid-column: span 2; text-align: center; font-size: 11px; color: #678; }}
        .tree-content.collapsed, .children {{ display: none; }}
        .children.visible {{ display: block; }}
        .node {{
            --bar-start: 0; --bar-self-end: 0; --bar-end: 0; --indent: 0;
            padding: 4px 16px 4px calc(16px + var(--indent) * 20px);
            display: flex; align-items: center; gap: 8px; cursor: pointer;
            border-left: 2px solid transparent;
            background: linear-gradient(to right, transparent 0%, transparent var(--bar-start), rgba(85,170,255,0.3) var(--bar-start), rgba(85,170,255,0.3) var(--bar-self-end), rgba(51,187,85,0.25) var(--bar-self-end), rgba(51,187,85,0.25) var(--bar-end), transparent var(--bar-end), transparent 100%);
        }}
        .node:hover {{
            background: linear-gradient(to right, transparent 0%, transparent var(--bar-start), rgba(85,170,255,0.45) var(--bar-start), rgba(85,170,255,0.45) var(--bar-self-end), rgba(51,187,85,0.4) var(--bar-self-end), rgba(51,187,85,0.4) var(--bar-end), transparent var(--bar-end), transparent 100%), #123;
            border-left-color: #5af;
        }}
        .node.expanded > .toggle {{ transform: rotate(90deg); }}
        .toggle {{ width: 16px; height: 16px; display: flex; align-items: center; justify-content: center; color: #899; transition: transform 0.15s ease; flex-shrink: 0; }}
        .toggle.hidden {{ visibility: hidden; }}
        .node-name {{ font-weight: 500; }}
        .node-version {{ color: #899; font-size: 11px; }}
        .occurrence-badge {{ font-size: 9px; padding: 1px 5px; border-radius: 10px; font-weight: 600; }}
        .node-stats {{ margin-left: auto; align-items: center; font-variant-numeric: tabular-nums; font-size: 11px; }}
        .node-stats .size {{ text-align: right; color: #678; }}
        .node-stats .size.amort {{ color: #3b5; }}
        .node-stats .size.virt {{ color: #a7f; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>uv.lock Dependency Visualizer</h1>
        <div class="subtitle">{lock_path}</div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-label">Unique Packages</div>
                <div class="stat-value">{len(dep_packages)}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Deduplicated Size</div>
                <div class="stat-value blue">{format_size(total_dedup_size)}</div>
            </div>
            <div class="stat">
                <div class="stat-label">If Duplicated</div>
                <div class="stat-value orange">{format_size(total_with_dupes)}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Dedup Savings</div>
                <div class="stat-value green">{format_size(savings)} ({savings_pct:.1f}%)</div>
            </div>
        </div>
        
        <div class="legend">
            <div class="legend-item">
                <div class="legend-bar" style="background: rgba(56, 139, 253, 0.35);"></div>
                <span>Wheel (self)</span>
            </div>
            <div class="legend-item">
                <div class="legend-bar" style="background: rgba(63, 185, 80, 0.3);"></div>
                <span>Dependencies</span>
            </div>
            <div class="legend-item">
                <span style="background: #3b53; color: #3b5; padding: 2px 6px; border-radius: 10px;">×N</span>
                <span>Occurrences (÷N for amortized)</span>
            </div>
            <div class="legend-item">
                <span style="color: #3b5;">Green</span>
                <span style="color: #456;">/</span>
                <span style="color: #a7f;">Purple</span>
                <span>= Amortized / Virtual</span>
            </div>
            <div class="sort-controls">
                <span class="sort-label">Sort by:</span>
                <button class="sort-btn active" data-sort="size">Size ↓</button>
                <button class="sort-btn" data-sort="name">Name A-Z</button>
            </div>
        </div>
    </div>
    
    <div class="trees-container" id="trees"></div>
    
    <script>
        const trees = {json.dumps(trees)};
        const maxOccurrences = {max_occurrences};
        let currentSort = 'size'; // 'size' or 'name'
        
        function calcTreeMax(node, max = 0) {{
            max = Math.max(max, node.dedup_size);
            (node.children || []).forEach(c => {{ max = calcTreeMax(c, max); }});
            return max;
        }}
        
        const treeMaxes = trees.map(tree => ({{ dedupSize: calcTreeMax(tree) }}));
        
        function sortChildren(children) {{
            if (!children) return [];
            const sorted = [...children];
            if (currentSort === 'size') {{
                sorted.sort((a, b) => b.dedup_size - a.dedup_size);
            }} else {{
                sorted.sort((a, b) => a.name.localeCompare(b.name));
            }}
            return sorted;
        }}
        
        function formatBytes(bytes) {{
            const units = ['B', 'KB', 'MB', 'GB'];
            let i = 0;
            while (bytes >= 1024 && i < units.length - 1) {{
                bytes /= 1024;
                i++;
            }}
            return bytes.toFixed(1) + ' ' + units[i];
        }}
        
        function getOccurrenceColor(count) {{
            if (count >= 5) return '#3b5';
            if (count >= 3) return '#5d6';
            if (count >= 2) return '#da2';
            return '#f54';
        }}
        
        function renderNode(node, treeIdx, barStart = 0) {{
            const hasChildren = node.children && node.children.length > 0;
            const maxes = treeMaxes[treeIdx];
            
            const amortizedSelf = node.self_size / node.occurrence_count;
            const selfWidth = (amortizedSelf / maxes.dedupSize) * 100;
            const barSelfEnd = barStart + selfWidth;
            const barEnd = barStart + (node.dedup_size / maxes.dedupSize) * 100;
            const occColor = getOccurrenceColor(node.occurrence_count);
            
            let html = `
                <div class="node" style="--indent: ${{node.depth}}; --bar-start: ${{barStart}}%; --bar-self-end: ${{barSelfEnd}}%; --bar-end: ${{barEnd}}%">
                    <span class="toggle ${{hasChildren ? '' : 'hidden'}}">▶</span>
                    <div class="node-left">
                        <span class="node-name">${{node.name}}</span>
                        <span class="node-version">v${{node.version}}</span>
                        ${{node.occurrence_count > 1 ? `<span class="occurrence-badge" style="background: ${{occColor}}22; color: ${{occColor}}">×${{node.occurrence_count}}</span>` : ''}}
                    </div>
                    <div class="node-stats">
                        <span class="size virt">${{formatBytes(node.self_size)}}</span>
                        <span class="size amort">${{formatBytes(amortizedSelf)}}</span>
                        <span class="size virt">${{formatBytes(node.total_size - node.self_size)}}</span>
                        <span class="size amort">${{formatBytes(node.dedup_size - amortizedSelf)}}</span>
                        <span class="size virt">${{formatBytes(node.total_size)}}</span>
                        <span class="size amort">${{formatBytes(node.dedup_size)}}</span>
                    </div>
                </div>
            `;
            
            if (hasChildren) {{
                html += '<div class="children">';
                let childStart = barSelfEnd;  // Children start where parent's blue portion ends
                sortChildren(node.children).forEach(child => {{
                    const childTotalWidth = (child.dedup_size / maxes.dedupSize) * 100;
                    html += renderNode(child, treeIdx, childStart);
                    childStart += childTotalWidth;
                }});
                html += '</div>';
            }}
            
            return html;
        }}
        
        
        function renderTree(tree, treeIdx) {{
            const totalDeps = countNodes(tree) - 1;
            const maxes = treeMaxes[treeIdx];
            let childrenHtml = '';
            let childStart = 0;
            sortChildren(tree.children).forEach(child => {{
                const childWidth = (child.dedup_size / maxes.dedupSize) * 100;
                childrenHtml += renderNode(child, treeIdx, childStart);
                childStart += childWidth;
            }});
            
            const html = `
                <div class="tree-section">
                    <div class="tree-header">
                        <span class="tree-title">${{tree.name}} v${{tree.version}}</span>
                        <div class="tree-stats">
                            <span>${{totalDeps}} deps</span>
                            <span>Virtual: ${{formatBytes(tree.total_size)}}</span>
                            <span style="color: #3b5">Dedup: ${{formatBytes(tree.dedup_size)}}</span>
                        </div>
                        <div class="tree-col-headers">
                            <span>Wheel</span>
                            <span>Deps</span>
                            <span>Tree</span>
                        </div>
                    </div>
                    <div class="tree-content">
                        ${{childrenHtml}}
                    </div>
                </div>
            `;
            return html;
        }}
        
        function countNodes(node) {{
            let count = 1;
            (node.children || []).forEach(c => count += countNodes(c));
            return count;
        }}
        
        const container = document.getElementById('trees');
        function renderAllTrees() {{
            container.innerHTML = trees.map((tree, idx) => renderTree(tree, idx)).join('');
        }}
        renderAllTrees();
        
        document.querySelectorAll('.sort-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                const sortMode = btn.dataset.sort;
                if (sortMode === currentSort) return;
                
                currentSort = sortMode;
                document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                renderAllTrees();
            }});
        }});
        
        container.addEventListener('click', (e) => {{
            const node = e.target.closest('.node');
            if (node) {{
                const children = node.nextElementSibling;
                if (children && children.classList.contains('children')) {{
                    children.classList.toggle('visible');
                    node.classList.toggle('expanded');
                }}
            }}
            
            const header = e.target.closest('.tree-header');
            if (header) {{
                const content = header.nextElementSibling;
                if (content) {{
                    content.classList.toggle('collapsed');
                }}
            }}
        }});
        
        // Long-poll for file changes and auto-reload
        (function poll() {{
            fetch('/poll').then(r => r.text()).then(status => {{
                if (status === 'changed') location.reload();
                else poll();
            }}).catch(() => setTimeout(poll, 2000));
        }})();
    </script>
</body>
</html>
'''
    
    if output_path:
        with open(output_path, "w") as f:
            f.write(html)
        
        print(f"Generated: {output_path}")
        print(f"  Workspace members: {len(workspace_members)}")
        print(f"  Unique dependencies: {len(dep_packages)}")
        print(f"  Deduplicated size: {format_size(total_dedup_size)}")
        print(f"  If duplicated: {format_size(total_with_dupes)}")
        print(f"  Savings: {format_size(savings)} ({savings_pct:.1f}%)")
    
    return html


def build_visualization(lock_path: Path) -> str:
    """Build the visualization HTML from a uv.lock file."""
    packages, workspace_members = parse_uv_lock(lock_path)
    
    trees: list[TreeNode] = []
    for member in workspace_members:
        if member in packages:
            tree = build_dependency_tree(member, packages)
            if tree:
                trees.append(tree)
    
    global_occurrence_counts: dict[str, int] = {}
    for tree in trees:
        count_occurrences(tree, global_occurrence_counts)
    
    for tree in trees:
        calculate_sizes(tree, global_occurrence_counts)
    
    tree_dicts = [tree_to_dict(tree) for tree in trees]
    return generate_html(tree_dicts, packages, workspace_members, global_occurrence_counts, lock_path)


class FileWatcher:
    """Watch a file for changes using polling."""
    def __init__(self, path: Path, poll_interval: float = 1.0):
        self.path = path
        self.poll_interval = poll_interval
        self.last_mtime = path.stat().st_mtime if path.exists() else 0
        self.change_event = threading.Event()
        self.running = True
        self.thread = threading.Thread(target=self._watch, daemon=True)
        self.thread.start()
    
    def _watch(self):
        while self.running:
            time.sleep(self.poll_interval)
            try:
                mtime = self.path.stat().st_mtime
                if mtime != self.last_mtime:
                    self.last_mtime = mtime
                    print(f"  Change detected: {self.path}")
                    self.change_event.set()
            except OSError:
                pass
    
    def wait_for_change(self, timeout: float = 30.0) -> bool:
        """Block until file changes or timeout. Returns True if changed."""
        self.change_event.clear()
        return self.change_event.wait(timeout)
    
    def stop(self):
        self.running = False


def create_request_handler(lock_path: Path, watcher: FileWatcher):
    """Create a request handler class that serves the visualization."""
    
    class DepTreeHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/" or self.path == "/index.html":
                try:
                    html = build_visualization(lock_path)
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                    self.end_headers()
                    self.wfile.write(html.encode("utf-8"))
                except Exception as e:
                    self.send_response(500)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write(f"Error generating visualization: {e}".encode("utf-8"))
            elif self.path == "/poll":
                changed = watcher.wait_for_change(timeout=30.0)
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                self.wfile.write(b"changed" if changed else b"timeout")
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Not found")
        
        def log_message(self, format, *args):
            print(f"  {args[0]}")
    
    return DepTreeHandler


def run_server(lock_path: Path, port: int = 8000, open_browser: bool = True):
    """Run a live server that watches uv.lock and auto-refreshes on changes."""
    watcher = FileWatcher(lock_path)
    handler = create_request_handler(lock_path, watcher)
    server = HTTPServer(("localhost", port), handler)
    
    url = f"http://localhost:{port}"
    print(f"Live server: {url}")
    print(f"Watching: {lock_path}")
    print(f"  Auto-refreshes on change. Ctrl+C to stop.\n")
    
    if open_browser:
        webbrowser.open(url)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        watcher.stop()
        server.shutdown()


def main():
    parser = argparse.ArgumentParser(
        description="UV Lock Nested Dependency Visualizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                      # Generate HTML from ./uv.lock
  python main.py ../project/uv.lock   # Generate HTML from specific file
  python main.py --serve              # Start live server on port 8000
  python main.py --serve --port 3000  # Start live server on port 3000
  python main.py --serve --no-open    # Start server without opening browser
        """
    )
    parser.add_argument(
        "lock_file",
        nargs="?",
        default=None,
        help="Path to uv.lock file (default: searches upward from current directory)"
    )
    parser.add_argument(
        "--serve", "-s",
        action="store_true",
        help="Start a live server instead of generating a static file"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8000,
        help="Port for live server (default: 8000)"
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Don't automatically open browser when starting server"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file path (default: uv-deps.html in same directory as lock file)"
    )
    
    args = parser.parse_args()
    
    if args.lock_file:
        lock_path = Path(args.lock_file)
        if not lock_path.exists():
            print(f"Error: {lock_path} not found")
            sys.exit(1)
    else:
        # Search upward for uv.lock, like uv does
        lock_path = None
        search_dir = Path.cwd()
        while search_dir != search_dir.parent:
            candidate = search_dir / "uv.lock"
            if candidate.exists():
                lock_path = candidate
                break
            search_dir = search_dir.parent
        
        if lock_path is None:
            print("Error: No uv.lock found in current directory or any parent directory")
            sys.exit(1)
    
    if args.serve:
        run_server(lock_path, args.port, open_browser=not args.no_open)
    else:
        print(f"Parsing {lock_path}...")
        packages, workspace_members = parse_uv_lock(lock_path)
        print(f"Found {len(packages)} packages, {len(workspace_members)} workspace members")
        
        print("Building dependency trees...")
        trees: list[TreeNode] = []
        for member in workspace_members:
            if member in packages:
                tree = build_dependency_tree(member, packages)
                if tree:
                    trees.append(tree)
        
        print("Counting occurrences...")
        global_occurrence_counts: dict[str, int] = {}
        for tree in trees:
            count_occurrences(tree, global_occurrence_counts)
        
        print("Calculating weighted sizes...")
        for tree in trees:
            calculate_sizes(tree, global_occurrence_counts)
        
        tree_dicts = [tree_to_dict(tree) for tree in trees]
        
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = lock_path.parent / "uv-deps.html"
        
        generate_html(tree_dicts, packages, workspace_members, global_occurrence_counts, lock_path, output_path)


if __name__ == "__main__":
    main()
