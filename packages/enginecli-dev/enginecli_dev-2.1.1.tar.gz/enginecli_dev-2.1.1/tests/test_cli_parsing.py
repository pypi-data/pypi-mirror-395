"""
Tests for the CLI file parsing functions.
"""
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import from CLI module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestFileParsing:
    """Tests for file content parsing."""
    
    def test_extract_new_format(self):
        """Test extracting files from new format."""
        from engine.cli import _extract_file_changes
        
        content = """<<<<< FILE: api/users.py >>>>>
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def list_users():
    return []
<<<<< END FILE >>>>>

<<<<< FILE: models/user.py >>>>>
class User:
    id: int
    name: str
<<<<< END FILE >>>>>"""
        
        changes = _extract_file_changes(content)
        
        assert len(changes) == 2
        assert changes[0][0] == "api/users.py"
        assert "APIRouter" in changes[0][1]
        assert changes[1][0] == "models/user.py"
        assert "class User" in changes[1][1]
    
    def test_extract_legacy_format(self):
        """Test extracting files from legacy format."""
        from engine.cli import _extract_file_changes
        
        content = """FILE: api/users.py
```python
from fastapi import APIRouter

router = APIRouter()
```

FILE: models/user.py
```python
class User:
    pass
```"""
        
        changes = _extract_file_changes(content)
        
        assert len(changes) == 2
        assert changes[0][0] == "api/users.py"
        assert changes[1][0] == "models/user.py"
    
    def test_extract_empty_content(self):
        """Test with no file markers."""
        from engine.cli import _extract_file_changes
        
        content = "Just some regular text"
        
        changes = _extract_file_changes(content)
        
        assert changes == []
    
    def test_apply_new_format(self):
        """Test applying files from new format."""
        from engine.cli import _apply_changes
        
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            os.chdir(tmpdir)
            
            content = """<<<<< FILE: test_file.py >>>>>
print("hello world")
<<<<< END FILE >>>>>"""
            
            # Mock the RollbackManager to avoid side effects
            with patch('engine.rollback.RollbackManager') as mock_manager:
                mock_instance = MagicMock()
                mock_instance.create_snapshot.return_value = MagicMock(id="test_snapshot")
                mock_manager.return_value = mock_instance
                
                _apply_changes(content)
            
            assert Path("test_file.py").exists()
            assert Path("test_file.py").read_text() == 'print("hello world")'
    
    def test_apply_creates_directories(self):
        """Test that apply creates parent directories."""
        from engine.cli import _apply_changes
        
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            os.chdir(tmpdir)
            
            content = """<<<<< FILE: deep/nested/dir/file.py >>>>>
# nested file
<<<<< END FILE >>>>>"""
            
            with patch('engine.rollback.RollbackManager') as mock_manager:
                mock_instance = MagicMock()
                mock_instance.create_snapshot.return_value = MagicMock(id="test_snapshot")
                mock_manager.return_value = mock_instance
                
                _apply_changes(content)
            
            assert Path("deep/nested/dir/file.py").exists()
    
    def test_delete_marker(self):
        """Test delete file marker."""
        from engine.cli import _apply_changes
        
        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            os.chdir(tmpdir)
            
            # Create file first
            Path("to_delete.py").write_text("delete me")
            assert Path("to_delete.py").exists()
            
            content = """<<<<< FILE: to_delete.py >>>>>
__DELETE_FILE__
<<<<< END FILE >>>>>"""
            
            with patch('engine.rollback.RollbackManager') as mock_manager:
                mock_instance = MagicMock()
                mock_instance.create_snapshot.return_value = MagicMock(id="test_snapshot")
                mock_manager.return_value = mock_instance
                
                _apply_changes(content)
            
            assert not Path("to_delete.py").exists()

