"""
TypeScript/React Indexer - extracts code constructs from TS/JS files.
Uses regex-based parsing for simplicity (no external dependencies).
Runs locally for speed.
"""
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class FunctionInfo:
    """Information about a function."""
    name: str
    file_path: str
    line_number: int
    parameters: List[str]
    return_type: Optional[str]
    is_async: bool
    is_exported: bool
    source: str


@dataclass
class ComponentInfo:
    """Information about a React component."""
    name: str
    file_path: str
    line_number: int
    props: List[str]
    is_exported: bool
    source: str


@dataclass
class InterfaceInfo:
    """Information about a TypeScript interface."""
    name: str
    file_path: str
    line_number: int
    properties: List[str]
    is_exported: bool
    source: str


@dataclass
class HookInfo:
    """Information about a React hook."""
    name: str
    file_path: str
    line_number: int
    source: str


class TypeScriptIndexer:
    """Indexes TypeScript/JavaScript source files."""
    
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.functions: List[FunctionInfo] = []
        self.components: List[ComponentInfo] = []
        self.interfaces: List[InterfaceInfo] = []
        self.hooks: List[HookInfo] = []
    
    def index(self, exclude_dirs: List[str] = None) -> Dict[str, Any]:
        """Index all TypeScript/JavaScript files."""
        exclude_dirs = exclude_dirs or ['node_modules', 'dist', 'build', '.next', '.git']
        
        extensions = ['.ts', '.tsx', '.js', '.jsx']
        
        for ext in extensions:
            for file_path in self.root_dir.rglob(f"*{ext}"):
                if any(excl in file_path.parts for excl in exclude_dirs):
                    continue
                
                try:
                    self._index_file(file_path)
                except Exception:
                    continue
        
        return self.to_dict()
    
    def _index_file(self, file_path: Path):
        """Index a single file."""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()
        
        rel_path = str(file_path.relative_to(self.root_dir))
        lines = source.split("\n")
        
        # Extract functions
        self._extract_functions(source, rel_path, lines)
        
        # Extract React components
        self._extract_components(source, rel_path, lines)
        
        # Extract interfaces (TypeScript)
        if file_path.suffix in ['.ts', '.tsx']:
            self._extract_interfaces(source, rel_path, lines)
        
        # Extract hooks
        self._extract_hooks(source, rel_path, lines)
    
    def _extract_functions(self, source: str, file_path: str, lines: List[str]):
        """Extract function declarations."""
        # Match: function name(...) or const name = (...) => or const name = function(...)
        patterns = [
            # Regular function
            r'^(export\s+)?(async\s+)?function\s+(\w+)\s*\(([^)]*)\)\s*(?::\s*(\w+))?',
            # Arrow function
            r'^(export\s+)?(const|let)\s+(\w+)\s*=\s*(async\s+)?\(([^)]*)\)\s*(?::\s*(\w+))?\s*=>',
        ]
        
        for i, line in enumerate(lines):
            for pattern in patterns:
                match = re.match(pattern, line.strip())
                if match:
                    groups = match.groups()
                    
                    if 'function' in pattern:
                        is_exported = groups[0] is not None
                        is_async = groups[1] is not None
                        name = groups[2]
                        params = groups[3]
                        return_type = groups[4]
                    else:
                        is_exported = groups[0] is not None
                        name = groups[2]
                        is_async = groups[3] is not None
                        params = groups[4]
                        return_type = groups[5]
                    
                    # Skip React components (handled separately)
                    if name[0].isupper():
                        continue
                    
                    # Get function source (simplified - just get a few lines)
                    end_line = min(i + 20, len(lines))
                    func_source = "\n".join(lines[i:end_line])
                    
                    self.functions.append(FunctionInfo(
                        name=name,
                        file_path=file_path,
                        line_number=i + 1,
                        parameters=[p.strip() for p in params.split(",") if p.strip()],
                        return_type=return_type,
                        is_async=is_async,
                        is_exported=is_exported,
                        source=func_source,
                    ))
                    break
    
    def _extract_components(self, source: str, file_path: str, lines: List[str]):
        """Extract React components."""
        # Match: function ComponentName or const ComponentName = (props) =>
        # Also matches: const ComponentName: React.FC<Props> = (props) =>
        patterns = [
            # Function component
            r'^(export\s+)?(default\s+)?function\s+([A-Z]\w+)\s*\(([^)]*)\)',
            # Arrow function component (with optional type annotation like React.FC<Props>)
            r'^(export\s+)?(default\s+)?(const|let)\s+([A-Z]\w+)\s*(?::\s*[^=]+)?\s*=\s*\(([^)]*)\)\s*=>',
            # Arrow function with type but no parens: const Comp: FC<P> = props =>
            r'^(export\s+)?(default\s+)?(const|let)\s+([A-Z]\w+)\s*:\s*(?:React\.)?FC\s*<[^>]*>\s*=\s*(\w+)\s*=>',
        ]
        
        for i, line in enumerate(lines):
            for pattern in patterns:
                match = re.match(pattern, line.strip())
                if match:
                    groups = match.groups()
                    
                    if 'function' in pattern:
                        is_exported = groups[0] is not None or groups[1] is not None
                        name = groups[2]
                        props_str = groups[3]
                    else:
                        is_exported = groups[0] is not None or groups[1] is not None
                        name = groups[3]
                        props_str = groups[4] if len(groups) > 4 else ""
                    
                    # Parse props
                    props = []
                    if props_str and props_str.strip():
                        # Simple prop extraction from destructuring
                        prop_match = re.search(r'\{\s*([^}]+)\s*\}', props_str)
                        if prop_match:
                            props = [p.strip().split(':')[0].strip() 
                                   for p in prop_match.group(1).split(',')
                                   if p.strip()]
                    
                    # Get component source
                    end_line = min(i + 30, len(lines))
                    comp_source = "\n".join(lines[i:end_line])
                    
                    self.components.append(ComponentInfo(
                        name=name,
                        file_path=file_path,
                        line_number=i + 1,
                        props=props,
                        is_exported=is_exported,
                        source=comp_source,
                    ))
                    break
    
    def _extract_interfaces(self, source: str, file_path: str, lines: List[str]):
        """Extract TypeScript interfaces."""
        pattern = r'^(export\s+)?interface\s+(\w+)'
        
        for i, line in enumerate(lines):
            match = re.match(pattern, line.strip())
            if match:
                is_exported = match.group(1) is not None
                name = match.group(2)
                
                # Find interface body
                properties = []
                brace_count = 0
                started = False
                interface_lines = []
                
                for j in range(i, min(i + 50, len(lines))):
                    interface_lines.append(lines[j])
                    if '{' in lines[j]:
                        started = True
                        brace_count += lines[j].count('{')
                    if '}' in lines[j]:
                        brace_count -= lines[j].count('}')
                    if started and brace_count == 0:
                        break
                
                # Extract property names
                body = "\n".join(interface_lines)
                prop_pattern = r'(\w+)\s*[?]?\s*:'
                properties = re.findall(prop_pattern, body)
                
                self.interfaces.append(InterfaceInfo(
                    name=name,
                    file_path=file_path,
                    line_number=i + 1,
                    properties=properties,
                    is_exported=is_exported,
                    source="\n".join(interface_lines),
                ))
    
    def _extract_hooks(self, source: str, file_path: str, lines: List[str]):
        """Extract React hooks (custom hooks starting with 'use')."""
        pattern = r'^(export\s+)?(const|function)\s+(use\w+)'
        
        for i, line in enumerate(lines):
            match = re.match(pattern, line.strip())
            if match:
                name = match.group(3)
                
                # Get hook source
                end_line = min(i + 30, len(lines))
                hook_source = "\n".join(lines[i:end_line])
                
                self.hooks.append(HookInfo(
                    name=name,
                    file_path=file_path,
                    line_number=i + 1,
                    source=hook_source,
                ))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert index to dictionary."""
        return {
            "functions": [asdict(f) for f in self.functions],
            "components": [asdict(c) for c in self.components],
            "interfaces": [asdict(i) for i in self.interfaces],
            "hooks": [asdict(h) for h in self.hooks],
        }
    
    def save(self, output_path: Path):
        """Save index to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)


def index_typescript_project(root_dir: Path, output_path: Path = None) -> Dict[str, Any]:
    """
    Index a TypeScript/JavaScript project.
    
    Args:
        root_dir: Project root directory
        output_path: Optional path to save index JSON
    
    Returns:
        Index dictionary
    """
    indexer = TypeScriptIndexer(root_dir)
    index = indexer.index()
    
    if output_path:
        indexer.save(output_path)
    
    return index
