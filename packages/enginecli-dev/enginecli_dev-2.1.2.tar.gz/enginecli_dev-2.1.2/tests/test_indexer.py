"""
Tests for the Python and TypeScript indexers.
"""
import pytest
import tempfile
from pathlib import Path

from engine.indexer.python import PythonIndexer, index_python_project
from engine.indexer.typescript import TypeScriptIndexer, index_typescript_project


class TestPythonIndexer:
    """Tests for Python AST indexer."""
    
    def test_index_simple_function(self):
        """Test indexing a simple function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a simple Python file
            py_file = Path(tmpdir) / "simple.py"
            py_file.write_text('''
def hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"
''')
            
            indexer = PythonIndexer(Path(tmpdir))
            index = indexer.index()
            
            assert len(index['functions']) == 1
            func = index['functions'][0]
            assert func['name'] == 'hello'
            assert func['parameters'] == ['name']
            assert func['return_type'] == 'str'
            assert func['docstring'] == 'Say hello to someone.'
    
    def test_index_class(self):
        """Test indexing a class."""
        with tempfile.TemporaryDirectory() as tmpdir:
            py_file = Path(tmpdir) / "models.py"
            py_file.write_text('''
class User:
    """A user model."""
    
    def __init__(self, name: str):
        self.name = name
    
    def greet(self) -> str:
        return f"Hi, I'm {self.name}"
''')
            
            indexer = PythonIndexer(Path(tmpdir))
            index = indexer.index()
            
            assert len(index['classes']) == 1
            cls = index['classes'][0]
            assert cls['name'] == 'User'
            assert cls['docstring'] == 'A user model.'
            assert '__init__' in cls['methods']
            assert 'greet' in cls['methods']
    
    def test_index_fastapi_endpoint(self):
        """Test indexing FastAPI endpoints."""
        with tempfile.TemporaryDirectory() as tmpdir:
            py_file = Path(tmpdir) / "routes.py"
            py_file.write_text('''
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def list_users():
    return []

@router.post("/users")
def create_user(name: str):
    return {"name": name}

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {"deleted": user_id}
''')
            
            indexer = PythonIndexer(Path(tmpdir))
            index = indexer.index()
            
            assert len(index['endpoints']) == 3
            
            methods = {e['method'] for e in index['endpoints']}
            assert methods == {'GET', 'POST', 'DELETE'}
            
            paths = {e['path'] for e in index['endpoints']}
            assert '/users' in paths
            assert '/users/{user_id}' in paths
    
    def test_index_async_function(self):
        """Test indexing async functions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            py_file = Path(tmpdir) / "async_funcs.py"
            py_file.write_text('''
async def fetch_data(url: str) -> dict:
    """Fetch data from URL."""
    pass
''')
            
            indexer = PythonIndexer(Path(tmpdir))
            index = indexer.index()
            
            assert len(index['functions']) == 1
            func = index['functions'][0]
            assert func['name'] == 'fetch_data'
            assert func['is_async'] is True
    
    def test_index_excludes_venv(self):
        """Test that venv directories are excluded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file in venv
            venv_dir = Path(tmpdir) / "venv" / "lib"
            venv_dir.mkdir(parents=True)
            (venv_dir / "some_lib.py").write_text('def lib_func(): pass')
            
            # Create a file outside venv
            (Path(tmpdir) / "main.py").write_text('def main_func(): pass')
            
            indexer = PythonIndexer(Path(tmpdir))
            index = indexer.index()
            
            # Should only find main_func
            assert len(index['functions']) == 1
            assert index['functions'][0]['name'] == 'main_func'
    
    def test_index_imports(self):
        """Test indexing imports."""
        with tempfile.TemporaryDirectory() as tmpdir:
            py_file = Path(tmpdir) / "imports.py"
            py_file.write_text('''
import os
import json
from pathlib import Path
from typing import List, Dict
''')
            
            indexer = PythonIndexer(Path(tmpdir))
            index = indexer.index()
            
            assert len(index['imports']) >= 3
            modules = {i['module'] for i in index['imports']}
            assert 'os' in modules
            assert 'pathlib' in modules
            assert 'typing' in modules


class TestTypeScriptIndexer:
    """Tests for TypeScript/React indexer."""
    
    def test_index_react_component(self):
        """Test indexing a React component."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tsx_file = Path(tmpdir) / "Button.tsx"
            tsx_file.write_text('''
import React from 'react';

interface ButtonProps {
    label: string;
    onClick: () => void;
}

export const Button: React.FC<ButtonProps> = ({ label, onClick }) => {
    return <button onClick={onClick}>{label}</button>;
};
''')
            
            indexer = TypeScriptIndexer(Path(tmpdir))
            index = indexer.index()
            
            assert len(index['components']) >= 1, \
                f"Expected at least 1 component, got {len(index['components'])}. " \
                f"Components found: {[c['name'] for c in index['components']]}"
            component = next((c for c in index['components'] if c['name'] == 'Button'), None)
            assert component is not None, \
                f"Button component not found. Components: {[c['name'] for c in index['components']]}"
    
    def test_index_interface(self):
        """Test indexing TypeScript interfaces."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ts_file = Path(tmpdir) / "types.ts"
            ts_file.write_text('''
export interface User {
    id: number;
    name: string;
    email: string;
}

export interface Post {
    id: number;
    title: string;
    content: string;
    authorId: number;
}
''')
            
            indexer = TypeScriptIndexer(Path(tmpdir))
            index = indexer.index()
            
            assert len(index['interfaces']) == 2
            names = {i['name'] for i in index['interfaces']}
            assert names == {'User', 'Post'}
    
    def test_index_custom_hook(self):
        """Test indexing custom React hooks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ts_file = Path(tmpdir) / "useAuth.ts"
            ts_file.write_text('''
import { useState, useEffect } from 'react';

export function useAuth() {
    const [user, setUser] = useState(null);
    
    useEffect(() => {
        // Check auth status
    }, []);
    
    return { user, setUser };
}

export const useLocalStorage = (key: string) => {
    const [value, setValue] = useState(() => {
        return localStorage.getItem(key);
    });
    return [value, setValue];
};
''')
            
            indexer = TypeScriptIndexer(Path(tmpdir))
            index = indexer.index()
            
            assert len(index['hooks']) >= 1
            hook_names = {h['name'] for h in index['hooks']}
            assert 'useAuth' in hook_names
    
    def test_index_excludes_node_modules(self):
        """Test that node_modules is excluded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file in node_modules
            nm_dir = Path(tmpdir) / "node_modules" / "some-lib"
            nm_dir.mkdir(parents=True)
            (nm_dir / "index.ts").write_text('export const lib = {};')
            
            # Create a file outside node_modules
            (Path(tmpdir) / "main.ts").write_text('export const main = {};')
            
            indexer = TypeScriptIndexer(Path(tmpdir))
            index = indexer.index()
            
            # Should not include node_modules files
            all_files = set()
            for key in ['functions', 'components', 'interfaces', 'hooks']:
                for item in index.get(key, []):
                    all_files.add(item.get('file_path', ''))
            
            assert not any('node_modules' in f for f in all_files)


class TestIndexHelpers:
    """Test helper functions."""
    
    def test_index_python_project(self):
        """Test the index_python_project helper."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "main.py").write_text('def main(): pass')
            
            index = index_python_project(Path(tmpdir))
            
            assert 'functions' in index
            assert 'classes' in index
            assert 'endpoints' in index
            assert 'imports' in index
    
    def test_index_typescript_project(self):
        """Test the index_typescript_project helper."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "App.tsx").write_text('export const App = () => <div />;')
            
            index = index_typescript_project(Path(tmpdir))
            
            assert 'functions' in index
            assert 'components' in index
            assert 'interfaces' in index
            assert 'hooks' in index
