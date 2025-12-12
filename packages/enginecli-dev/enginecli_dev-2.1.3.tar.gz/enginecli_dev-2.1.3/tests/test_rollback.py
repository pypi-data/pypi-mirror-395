"""
Tests for the rollback system.
"""
import pytest
import tempfile
from pathlib import Path

from engine.rollback import (
    RollbackManager,
    Snapshot,
    FileState,
    create_snapshot,
    rollback,
    list_snapshots,
)


class TestFileState:
    """Tests for FileState dataclass."""
    
    def test_create_existing_file(self):
        """Test creating state for existing file."""
        state = FileState(
            path="api/users.py",
            existed=True,
            content="print('hello')",
        )
        
        assert state.path == "api/users.py"
        assert state.existed is True
        assert state.content == "print('hello')"
    
    def test_create_new_file(self):
        """Test creating state for new file."""
        state = FileState(
            path="api/new.py",
            existed=False,
        )
        
        assert state.existed is False
        assert state.content is None


class TestSnapshot:
    """Tests for Snapshot dataclass."""
    
    def test_to_dict(self):
        """Test converting snapshot to dict."""
        snapshot = Snapshot(
            id="20240115_143022",
            timestamp="2024-01-15T14:30:22",
            task="add user authentication",
            files=[
                FileState("api/users.py", True, "old content"),
                FileState("api/auth.py", False),
            ],
        )
        
        data = snapshot.to_dict()
        
        assert data["id"] == "20240115_143022"
        assert data["task"] == "add user authentication"
        assert len(data["files"]) == 2
        assert data["files"][0]["existed"] is True
    
    def test_from_dict(self):
        """Test creating snapshot from dict."""
        data = {
            "id": "20240115_143022",
            "timestamp": "2024-01-15T14:30:22",
            "task": "add user authentication",
            "files": [
                {"path": "api/users.py", "existed": True, "content": "old content"},
            ],
        }
        
        snapshot = Snapshot.from_dict(data)
        
        assert snapshot.id == "20240115_143022"
        assert len(snapshot.files) == 1
        assert snapshot.files[0].path == "api/users.py"


class TestRollbackManager:
    """Tests for RollbackManager."""
    
    @pytest.fixture
    def temp_project(self):
        """Create a temporary project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            
            # Create some files
            (project / "api").mkdir()
            (project / "api" / "users.py").write_text("def get_users():\n    return []")
            (project / "api" / "auth.py").write_text("def login():\n    pass")
            
            yield project
    
    def test_create_snapshot_existing_files(self, temp_project):
        """Test creating snapshot of existing files."""
        manager = RollbackManager(temp_project)
        
        snapshot = manager.create_snapshot(
            file_paths=["api/users.py", "api/auth.py"],
            task="modify auth system",
        )
        
        assert snapshot.id is not None
        assert snapshot.task == "modify auth system"
        assert len(snapshot.files) == 2
        
        # Check file states
        users_state = next(f for f in snapshot.files if f.path == "api/users.py")
        assert users_state.existed is True
        assert "get_users" in users_state.content
        
        # Check snapshot was saved
        snapshots = manager.list_snapshots()
        assert len(snapshots) == 1
    
    def test_create_snapshot_new_files(self, temp_project):
        """Test creating snapshot including new files."""
        manager = RollbackManager(temp_project)
        
        snapshot = manager.create_snapshot(
            file_paths=["api/new_feature.py"],
            task="add new feature",
        )
        
        # New file should be marked as not existing
        new_file_state = snapshot.files[0]
        assert new_file_state.path == "api/new_feature.py"
        assert new_file_state.existed is False
        assert new_file_state.content is None
    
    def test_rollback_modified_files(self, temp_project):
        """Test rolling back modified files."""
        manager = RollbackManager(temp_project)
        
        # Create snapshot
        snapshot = manager.create_snapshot(
            file_paths=["api/users.py"],
            task="modify users",
        )
        
        # Modify the file
        (temp_project / "api" / "users.py").write_text("MODIFIED CONTENT")
        assert "MODIFIED" in (temp_project / "api" / "users.py").read_text()
        
        # Rollback
        result = manager.rollback()
        
        assert result is True
        # File should be restored
        content = (temp_project / "api" / "users.py").read_text()
        assert "get_users" in content
        assert "MODIFIED" not in content
    
    def test_rollback_new_files(self, temp_project):
        """Test rolling back new files (should delete them)."""
        manager = RollbackManager(temp_project)
        
        # Create snapshot for file that doesn't exist
        manager.create_snapshot(
            file_paths=["api/new_feature.py"],
            task="add feature",
        )
        
        # Create the file (simulating generation)
        (temp_project / "api" / "new_feature.py").write_text("NEW FILE")
        assert (temp_project / "api" / "new_feature.py").exists()
        
        # Rollback
        result = manager.rollback()
        
        assert result is True
        # File should be deleted
        assert not (temp_project / "api" / "new_feature.py").exists()
    
    def test_rollback_to_specific_snapshot(self, temp_project):
        """Test rolling back to a specific snapshot."""
        manager = RollbackManager(temp_project)
        
        # Create first snapshot (captures original content)
        snapshot1 = manager.create_snapshot(["api/users.py"], "first change")
        original_content = (temp_project / "api" / "users.py").read_text()
        
        # Modify the file
        (temp_project / "api" / "users.py").write_text("VERSION 1")
        
        # Create second snapshot (captures VERSION 1)
        import time
        time.sleep(0.01)  # Ensure different timestamp (milliseconds)
        snapshot2 = manager.create_snapshot(["api/users.py"], "second change")
        (temp_project / "api" / "users.py").write_text("VERSION 2")
        
        # Rollback to first snapshot
        result = manager.rollback(snapshot1.id)
        
        assert result is True
        content = (temp_project / "api" / "users.py").read_text()
        assert content == original_content  # Should restore original
        assert "get_users" in content
    
    def test_list_snapshots_order(self, temp_project):
        """Test that snapshots are listed newest first."""
        manager = RollbackManager(temp_project)
        
        import time
        
        # Create multiple snapshots with small delays
        snapshot1 = manager.create_snapshot(["api/users.py"], "first")
        time.sleep(0.01)
        snapshot2 = manager.create_snapshot(["api/auth.py"], "second")
        time.sleep(0.01)
        snapshot3 = manager.create_snapshot(["api/users.py"], "third")
        
        snapshots = manager.list_snapshots()
        
        assert len(snapshots) == 3
        assert snapshots[0].id == snapshot3.id  # Newest first
        assert snapshots[2].id == snapshot1.id  # Oldest last
    
    def test_snapshot_limit(self, temp_project):
        """Test that old snapshots are cleaned up."""
        from engine.rollback import MAX_SNAPSHOTS
        
        manager = RollbackManager(temp_project)
        
        import time
        
        # Create more than max snapshots
        for i in range(MAX_SNAPSHOTS + 5):
            manager.create_snapshot(["api/users.py"], f"task {i}")
            time.sleep(0.002)  # Small delay for unique timestamps
        
        snapshots = manager.list_snapshots()
        
        # Should only keep MAX_SNAPSHOTS
        assert len(snapshots) == MAX_SNAPSHOTS
    
    def test_clear_all_snapshots(self, temp_project):
        """Test clearing all snapshots."""
        manager = RollbackManager(temp_project)
        
        import time
        
        # Create some snapshots
        manager.create_snapshot(["api/users.py"], "task 1")
        time.sleep(0.01)
        manager.create_snapshot(["api/auth.py"], "task 2")
        
        assert len(manager.list_snapshots()) == 2
        
        # Clear all
        manager.clear_all_snapshots()
        
        assert len(manager.list_snapshots()) == 0
    
    def test_rollback_no_snapshots(self, temp_project):
        """Test rollback when no snapshots exist."""
        manager = RollbackManager(temp_project)
        
        result = manager.rollback()
        
        assert result is False
    
    def test_get_nonexistent_snapshot(self, temp_project):
        """Test getting a snapshot that doesn't exist."""
        manager = RollbackManager(temp_project)
        
        snapshot = manager.get_snapshot("nonexistent_id")
        
        assert snapshot is None


class TestConvenienceFunctions:
    """Tests for convenience functions."""
    
    def test_create_snapshot_function(self):
        """Test the create_snapshot convenience function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            (project / "test.py").write_text("print('hello')")
            
            snapshot = create_snapshot(["test.py"], "test task", project)
            
            assert snapshot.task == "test task"
            assert len(snapshot.files) == 1
    
    def test_list_snapshots_function(self):
        """Test the list_snapshots convenience function."""
        import time
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            (project / "test.py").write_text("print('hello')")
            
            create_snapshot(["test.py"], "task 1", project)
            time.sleep(0.01)  # Ensure unique timestamps
            create_snapshot(["test.py"], "task 2", project)
            
            snapshots = list_snapshots(project)
            
            assert len(snapshots) == 2
    
    def test_rollback_function(self):
        """Test the rollback convenience function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            (project / "test.py").write_text("original")
            
            create_snapshot(["test.py"], "modify", project)
            (project / "test.py").write_text("modified")
            
            result = rollback(project_dir=project)
            
            assert result is True
            assert (project / "test.py").read_text() == "original"
