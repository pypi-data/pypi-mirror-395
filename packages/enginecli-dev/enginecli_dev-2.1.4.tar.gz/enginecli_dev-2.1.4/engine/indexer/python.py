"""
Python AST Indexer - extracts code constructs from Python files.
Runs locally for speed - no network calls needed.
"""
import ast
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
    docstring: Optional[str]
    parameters: List[str]
    return_type: Optional[str]
    decorators: List[str]
    is_async: bool
    source: str


@dataclass
class ClassInfo:
    """Information about a class."""
    name: str
    file_path: str
    line_number: int
    docstring: Optional[str]
    bases: List[str]
    methods: List[str]
    decorators: List[str]
    source: str


@dataclass
class APIEndpoint:
    """Information about an API endpoint (Flask/FastAPI)."""
    method: str
    path: str
    function_name: str
    file_path: str
    line_number: int
    source: str


@dataclass
class ImportInfo:
    """Information about an import."""
    module: str
    names: List[str]
    file_path: str
    line_number: int


class PythonIndexer:
    """Indexes Python source files."""
    
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.functions: List[FunctionInfo] = []
        self.classes: List[ClassInfo] = []
        self.endpoints: List[APIEndpoint] = []
        self.imports: List[ImportInfo] = []
    
    def index(self, exclude_dirs: List[str] = None) -> Dict[str, Any]:
        """
        Index all Python files in the directory.
        
        Args:
            exclude_dirs: Directories to exclude (e.g., ['venv', '__pycache__'])
        
        Returns:
            Index dictionary with all extracted constructs
        """
        exclude_dirs = exclude_dirs or ['venv', 'env', '.venv', '__pycache__', 'node_modules', '.git']
        
        for py_file in self.root_dir.rglob("*.py"):
            # Check if in excluded directory
            if any(excl in py_file.parts for excl in exclude_dirs):
                continue
            
            try:
                self._index_file(py_file)
            except Exception as e:
                # Skip files that can't be parsed
                continue
        
        return self.to_dict()
    
    def _index_file(self, file_path: Path):
        """Index a single Python file."""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()
        
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return
        
        rel_path = str(file_path.relative_to(self.root_dir))
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                self._extract_function(node, rel_path, source)
            elif isinstance(node, ast.ClassDef):
                self._extract_class(node, rel_path, source)
            elif isinstance(node, ast.Import):
                self._extract_import(node, rel_path)
            elif isinstance(node, ast.ImportFrom):
                self._extract_import_from(node, rel_path)
    
    def _extract_function(self, node: ast.FunctionDef, file_path: str, source: str):
        """Extract function information."""
        # Get source code
        lines = source.split("\n")
        start = node.lineno - 1
        end = node.end_lineno if hasattr(node, "end_lineno") else start + 1
        func_source = "\n".join(lines[start:end])
        
        # Get parameters
        params = []
        for arg in node.args.args:
            params.append(arg.arg)
        
        # Get return type
        return_type = None
        if node.returns:
            return_type = ast.unparse(node.returns) if hasattr(ast, "unparse") else str(node.returns)
        
        # Get decorators
        decorators = []
        for dec in node.decorator_list:
            if isinstance(dec, ast.Name):
                decorators.append(dec.id)
            elif isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                decorators.append(f"{dec.func.value.id}.{dec.func.attr}" if isinstance(dec.func.value, ast.Name) else dec.func.attr)
            elif isinstance(dec, ast.Attribute):
                decorators.append(dec.attr)
        
        # Check for API endpoints
        for dec in node.decorator_list:
            endpoint = self._extract_endpoint_from_decorator(dec, node.name, file_path, node.lineno, func_source)
            if endpoint:
                self.endpoints.append(endpoint)
        
        func_info = FunctionInfo(
            name=node.name,
            file_path=file_path,
            line_number=node.lineno,
            docstring=ast.get_docstring(node),
            parameters=params,
            return_type=return_type,
            decorators=decorators,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            source=func_source,
        )
        self.functions.append(func_info)
    
    def _extract_endpoint_from_decorator(
        self,
        decorator: ast.expr,
        func_name: str,
        file_path: str,
        line_number: int,
        source: str,
    ) -> Optional[APIEndpoint]:
        """Extract API endpoint from decorator."""
        # Flask style: @app.route("/path")
        # FastAPI style: @app.get("/path"), @router.post("/path")
        
        if not isinstance(decorator, ast.Call):
            return None
        
        if not isinstance(decorator.func, ast.Attribute):
            return None
        
        method = decorator.func.attr.upper()
        if method not in ["GET", "POST", "PUT", "DELETE", "PATCH", "ROUTE"]:
            return None
        
        # Get path from first argument
        if not decorator.args:
            return None
        
        path_arg = decorator.args[0]
        if isinstance(path_arg, ast.Constant):
            path = str(path_arg.value)
        else:
            path = "unknown"
        
        # Route decorator needs method from kwargs
        if method == "ROUTE":
            method = "GET"  # Default
            for kw in decorator.keywords:
                if kw.arg == "methods" and isinstance(kw.value, ast.List):
                    if kw.value.elts:
                        first = kw.value.elts[0]
                        if isinstance(first, ast.Constant):
                            method = str(first.value).upper()
        
        return APIEndpoint(
            method=method,
            path=path,
            function_name=func_name,
            file_path=file_path,
            line_number=line_number,
            source=source,
        )
    
    def _extract_class(self, node: ast.ClassDef, file_path: str, source: str):
        """Extract class information."""
        lines = source.split("\n")
        start = node.lineno - 1
        end = node.end_lineno if hasattr(node, "end_lineno") else start + 10
        class_source = "\n".join(lines[start:end])
        
        # Get base classes
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(base.attr)
        
        # Get method names
        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(item.name)
        
        # Get decorators
        decorators = []
        for dec in node.decorator_list:
            if isinstance(dec, ast.Name):
                decorators.append(dec.id)
        
        class_info = ClassInfo(
            name=node.name,
            file_path=file_path,
            line_number=node.lineno,
            docstring=ast.get_docstring(node),
            bases=bases,
            methods=methods,
            decorators=decorators,
            source=class_source,
        )
        self.classes.append(class_info)
    
    def _extract_import(self, node: ast.Import, file_path: str):
        """Extract import statement."""
        for alias in node.names:
            self.imports.append(ImportInfo(
                module=alias.name,
                names=[alias.asname or alias.name],
                file_path=file_path,
                line_number=node.lineno,
            ))
    
    def _extract_import_from(self, node: ast.ImportFrom, file_path: str):
        """Extract from...import statement."""
        if node.module:
            names = [alias.name for alias in node.names]
            self.imports.append(ImportInfo(
                module=node.module,
                names=names,
                file_path=file_path,
                line_number=node.lineno,
            ))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert index to dictionary."""
        return {
            "functions": [asdict(f) for f in self.functions],
            "classes": [asdict(c) for c in self.classes],
            "endpoints": [asdict(e) for e in self.endpoints],
            "imports": [asdict(i) for i in self.imports],
        }
    
    def save(self, output_path: Path):
        """Save index to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)


def index_python_project(root_dir: Path, output_path: Path = None) -> Dict[str, Any]:
    """
    Index a Python project.
    
    Args:
        root_dir: Project root directory
        output_path: Optional path to save index JSON
    
    Returns:
        Index dictionary
    """
    indexer = PythonIndexer(root_dir)
    index = indexer.index()
    
    if output_path:
        indexer.save(output_path)
    
    return index
