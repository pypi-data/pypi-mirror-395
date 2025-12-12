"""
Tests for incremental indexer.
"""
import json
import tempfile
import time
from pathlib import Path

import pytest

from engine.indexer.incremental import (
    IncrementalIndexer,
    FileMetadata,
    IndexState,
    incremental_index,
)


class TestFileMetadata:
    """Tests for FileMetadata."""
    
    def test_create_metadata(self, tmp_path):
        """Test creating file metadata."""
        # Create test file
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")
        
        indexer = IncrementalIndexer(tmp_path, "python")
        metadata = indexer._get_file_metadata(test_file)
        
        assert metadata.path == "test.py"
        assert metadata.mtime > 0
        assert metadata.size > 0
        assert len(metadata.content_hash) == 64  # SHA256 hex


class TestIndexState:
    """Tests for IndexState."""
    
    def test_to_dict(self):
        """Test converting state to dict."""
        state = IndexState(
            language="python",
            last_indexed="2024-01-15T10:00:00",
            files={"test.py": {"mtime": 123, "size": 100, "content_hash": "abc"}},
        )
        
        d = state.to_dict()
        
        assert d["language"] == "python"
        assert d["last_indexed"] == "2024-01-15T10:00:00"
        assert "test.py" in d["files"]
    
    def test_from_dict(self):
        """Test creating state from dict."""
        data = {
            "version": "1.0",
            "language": "typescript",
            "last_indexed": "2024-01-15T10:00:00",
            "files": {"app.ts": {"mtime": 456}},
        }
        
        state = IndexState.from_dict(data)
        
        assert state.language == "typescript"
        assert "app.ts" in state.files


class TestIncrementalIndexer:
    """Tests for IncrementalIndexer."""
    
    @pytest.fixture
    def sample_project(self, tmp_path):
        """Create a sample Python project."""
        # Create some Python files
        (tmp_path / "main.py").write_text('''
def main():
    """Main function."""
    print("Hello")

if __name__ == "__main__":
    main()
''')
        
        (tmp_path / "utils.py").write_text('''
def helper(x: int) -> int:
    """Helper function."""
    return x * 2

class Config:
    """Configuration class."""
    debug = True
''')
        
        # Create subdirectory
        api_dir = tmp_path / "api"
        api_dir.mkdir()
        (api_dir / "routes.py").write_text('''
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def list_users():
    return []
''')
        
        return tmp_path
    
    def test_scan_files(self, sample_project):
        """Test scanning files."""
        indexer = IncrementalIndexer(sample_project, "python")
        files = indexer._scan_files()
        
        assert "main.py" in files
        assert "utils.py" in files
        assert "api/routes.py" in files
    
    def test_scan_excludes_dirs(self, sample_project):
        """Test that excluded dirs are skipped."""
        # Create venv directory
        venv_dir = sample_project / "venv"
        venv_dir.mkdir()
        (venv_dir / "ignored.py").write_text("# ignored")
        
        indexer = IncrementalIndexer(sample_project, "python")
        files = indexer._scan_files()
        
        assert "venv/ignored.py" not in files
    
    def test_initial_index(self, sample_project):
        """Test initial indexing (no previous state)."""
        indexer = IncrementalIndexer(sample_project, "python")
        index_data, stats = indexer.index()
        
        # Should have indexed all files
        assert stats["added"] == 3  # main.py, utils.py, api/routes.py
        assert stats["modified"] == 0
        assert stats["deleted"] == 0
        
        # Check index content
        assert len(index_data["functions"]) >= 3  # main, helper, list_users
        assert len(index_data["classes"]) >= 1  # Config
        assert len(index_data["endpoints"]) >= 1  # GET /users
    
    def test_no_changes(self, sample_project):
        """Test re-indexing with no changes."""
        indexer = IncrementalIndexer(sample_project, "python")
        
        # First index
        indexer.index()
        
        # Second index - should detect no changes
        index_data, stats = indexer.index()
        
        assert stats["added"] == 0
        assert stats["modified"] == 0
        assert stats["deleted"] == 0
        assert stats["unchanged"] == 3
    
    def test_detect_modified_file(self, sample_project):
        """Test detecting modified files."""
        indexer = IncrementalIndexer(sample_project, "python")
        
        # First index
        indexer.index()
        
        # Modify a file
        time.sleep(0.1)  # Ensure mtime changes
        (sample_project / "utils.py").write_text('''
def helper(x: int) -> int:
    """Modified helper."""
    return x * 3  # Changed!

def new_function():
    pass
''')
        
        # Re-index
        index_data, stats = indexer.index()
        
        assert stats["modified"] == 1
        assert stats["unchanged"] == 2
        
        # New function should be in index
        func_names = [f["name"] for f in index_data["functions"]]
        assert "new_function" in func_names
    
    def test_detect_added_file(self, sample_project):
        """Test detecting added files."""
        indexer = IncrementalIndexer(sample_project, "python")
        
        # First index
        indexer.index()
        
        # Add new file
        (sample_project / "new_module.py").write_text('''
def brand_new():
    """A brand new function."""
    pass
''')
        
        # Re-index
        index_data, stats = indexer.index()
        
        assert stats["added"] == 1
        assert stats["modified"] == 0
        assert stats["unchanged"] == 3
        
        # New function should be in index
        func_names = [f["name"] for f in index_data["functions"]]
        assert "brand_new" in func_names
    
    def test_detect_deleted_file(self, sample_project):
        """Test detecting deleted files."""
        indexer = IncrementalIndexer(sample_project, "python")
        
        # First index
        index_data1, _ = indexer.index()
        
        # Verify helper is in index
        func_names1 = [f["name"] for f in index_data1["functions"]]
        assert "helper" in func_names1
        
        # Delete file
        (sample_project / "utils.py").unlink()
        
        # Re-index
        index_data2, stats = indexer.index()
        
        assert stats["deleted"] == 1
        assert stats["unchanged"] == 2
        
        # Helper should be removed from index
        func_names2 = [f["name"] for f in index_data2["functions"]]
        assert "helper" not in func_names2
    
    def test_force_reindex(self, sample_project):
        """Test force re-indexing."""
        indexer = IncrementalIndexer(sample_project, "python")
        
        # First index
        indexer.index()
        
        # Force re-index (should re-index everything)
        index_data, stats = indexer.index(force=True)
        
        assert stats["added"] == 3
        assert stats["modified"] == 0
        assert stats["deleted"] == 0
        assert stats["unchanged"] == 0
    
    def test_state_persistence(self, sample_project):
        """Test that state is saved and loaded correctly."""
        indexer = IncrementalIndexer(sample_project, "python")
        indexer.index()
        
        # Check state file exists
        state_file = sample_project / ".engine" / "index_state.json"
        assert state_file.exists()
        
        # Load state with new indexer instance
        indexer2 = IncrementalIndexer(sample_project, "python")
        state = indexer2._load_state()
        
        assert state is not None
        assert state.language == "python"
        assert len(state.files) == 3


class TestConvenienceFunction:
    """Tests for incremental_index convenience function."""
    
    def test_incremental_index(self, tmp_path):
        """Test the convenience function."""
        (tmp_path / "app.py").write_text("def hello(): pass")
        
        index_data, stats = incremental_index(tmp_path, "python")
        
        assert stats["total"] == 1
        assert len(index_data["functions"]) == 1


class TestTypescriptIncremental:
    """Tests for TypeScript incremental indexing."""
    
    @pytest.fixture
    def ts_project(self, tmp_path):
        """Create a sample TypeScript project."""
        (tmp_path / "app.tsx").write_text('''
import React from 'react';

interface User {
    id: number;
    name: string;
}

export const UserCard: React.FC<{user: User}> = ({user}) => {
    return <div>{user.name}</div>;
};
''')
        
        (tmp_path / "hooks.ts").write_text('''
import { useState, useEffect } from 'react';

export const useAuth = () => {
    const [user, setUser] = useState(null);
    return { user };
};
''')
        
        return tmp_path
    
    def test_typescript_incremental(self, ts_project):
        """Test TypeScript incremental indexing."""
        indexer = IncrementalIndexer(ts_project, "typescript")
        index_data, stats = indexer.index()
        
        assert stats["added"] == 2
        assert len(index_data["components"]) >= 1  # UserCard
        assert len(index_data["interfaces"]) >= 1  # User
        assert len(index_data["hooks"]) >= 1  # useAuth
    
    def test_typescript_modification(self, ts_project):
        """Test detecting TypeScript modifications."""
        indexer = IncrementalIndexer(ts_project, "typescript")
        indexer.index()
        
        # Modify file
        time.sleep(0.1)
        (ts_project / "app.tsx").write_text('''
import React from 'react';

interface User {
    id: number;
    name: string;
    email: string;  // Added field
}

export const UserCard: React.FC<{user: User}> = ({user}) => {
    return <div>{user.name} - {user.email}</div>;
};

// New component
export const UserList: React.FC = () => {
    return <div>Users</div>;
};
''')
        
        # Re-index
        index_data, stats = indexer.index()
        
        assert stats["modified"] == 1
        assert stats["unchanged"] == 1
        
        # Should have both components
        component_names = [c["name"] for c in index_data["components"]]
        assert "UserCard" in component_names
        assert "UserList" in component_names
