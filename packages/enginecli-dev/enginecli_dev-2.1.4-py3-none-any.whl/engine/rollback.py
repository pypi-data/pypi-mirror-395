"""
Rollback System - saves and restores file states.

Provides safety net for code generation by:
1. Snapshotting files before modification
2. Storing snapshots with metadata
3. Allowing instant rollback to previous state
"""
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass, asdict


SNAPSHOTS_DIR = ".engine/snapshots"
MAX_SNAPSHOTS = 10  # Keep last N snapshots


@dataclass
class FileState:
    """State of a single file."""
    path: str
    existed: bool
    content: Optional[str] = None  # None if file didn't exist


@dataclass
class Snapshot:
    """A snapshot of file states before modification."""
    id: str
    timestamp: str
    task: str
    files: List[FileState]
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "task": self.task,
            "files": [asdict(f) for f in self.files],
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Snapshot":
        return cls(
            id=data["id"],
            timestamp=data["timestamp"],
            task=data["task"],
            files=[FileState(**f) for f in data["files"]],
        )


class RollbackManager:
    """Manages file snapshots and rollback operations."""
    
    def __init__(self, project_dir: Path = None):
        self.project_dir = project_dir or Path.cwd()
        self.snapshots_dir = self.project_dir / SNAPSHOTS_DIR
    
    def create_snapshot(self, file_paths: List[str], task: str) -> Snapshot:
        """
        Create a snapshot of the current state of files.
        
        Args:
            file_paths: List of file paths that will be modified
            task: Description of the task being performed
        
        Returns:
            Snapshot object with file states
        """
        # Generate snapshot ID with milliseconds for uniqueness
        timestamp = datetime.now()
        snapshot_id = timestamp.strftime("%Y%m%d_%H%M%S") + f"_{timestamp.microsecond // 1000:03d}"
        
        # Create snapshot directory
        snapshot_dir = self.snapshots_dir / snapshot_id
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Capture file states
        file_states = []
        for file_path in file_paths:
            full_path = self.project_dir / file_path
            
            if full_path.exists():
                # File exists - save its content
                content = full_path.read_text()
                file_states.append(FileState(
                    path=file_path,
                    existed=True,
                    content=content,
                ))
                
                # Also save a copy of the file
                backup_path = snapshot_dir / file_path
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(full_path, backup_path)
            else:
                # File doesn't exist - mark it
                file_states.append(FileState(
                    path=file_path,
                    existed=False,
                    content=None,
                ))
        
        # Create snapshot
        snapshot = Snapshot(
            id=snapshot_id,
            timestamp=timestamp.isoformat(),
            task=task,
            files=file_states,
        )
        
        # Save manifest
        manifest_path = snapshot_dir / "manifest.json"
        manifest_path.write_text(json.dumps(snapshot.to_dict(), indent=2))
        
        # Cleanup old snapshots
        self._cleanup_old_snapshots()
        
        return snapshot
    
    def rollback(self, snapshot_id: str = None) -> bool:
        """
        Rollback to a snapshot.
        
        Args:
            snapshot_id: Specific snapshot to rollback to (default: latest)
        
        Returns:
            True if rollback succeeded
        """
        # Get snapshot to restore
        if snapshot_id is None:
            snapshot = self.get_latest_snapshot()
        else:
            snapshot = self.get_snapshot(snapshot_id)
        
        if snapshot is None:
            return False
        
        # Restore each file
        for file_state in snapshot.files:
            full_path = self.project_dir / file_state.path
            
            if file_state.existed:
                # Restore file content
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(file_state.content)
            else:
                # File didn't exist before - delete it
                if full_path.exists():
                    full_path.unlink()
                    
                    # Clean up empty parent directories
                    self._cleanup_empty_dirs(full_path.parent)
        
        # Remove the snapshot after successful rollback
        snapshot_dir = self.snapshots_dir / snapshot.id
        if snapshot_dir.exists():
            shutil.rmtree(snapshot_dir)
        
        return True
    
    def get_latest_snapshot(self) -> Optional[Snapshot]:
        """Get the most recent snapshot."""
        snapshots = self.list_snapshots()
        return snapshots[0] if snapshots else None
    
    def get_snapshot(self, snapshot_id: str) -> Optional[Snapshot]:
        """Get a specific snapshot by ID."""
        snapshot_dir = self.snapshots_dir / snapshot_id
        manifest_path = snapshot_dir / "manifest.json"
        
        if not manifest_path.exists():
            return None
        
        data = json.loads(manifest_path.read_text())
        return Snapshot.from_dict(data)
    
    def list_snapshots(self) -> List[Snapshot]:
        """List all available snapshots, newest first."""
        if not self.snapshots_dir.exists():
            return []
        
        snapshots = []
        for snapshot_dir in sorted(self.snapshots_dir.iterdir(), reverse=True):
            if snapshot_dir.is_dir():
                manifest_path = snapshot_dir / "manifest.json"
                if manifest_path.exists():
                    try:
                        data = json.loads(manifest_path.read_text())
                        snapshots.append(Snapshot.from_dict(data))
                    except (json.JSONDecodeError, KeyError):
                        continue
        
        return snapshots
    
    def _cleanup_old_snapshots(self):
        """Remove snapshots beyond MAX_SNAPSHOTS limit."""
        snapshots = self.list_snapshots()
        
        if len(snapshots) > MAX_SNAPSHOTS:
            for old_snapshot in snapshots[MAX_SNAPSHOTS:]:
                snapshot_dir = self.snapshots_dir / old_snapshot.id
                if snapshot_dir.exists():
                    shutil.rmtree(snapshot_dir)
    
    def _cleanup_empty_dirs(self, dir_path: Path):
        """Remove empty parent directories up to project root."""
        while dir_path != self.project_dir:
            if dir_path.exists() and not any(dir_path.iterdir()):
                dir_path.rmdir()
                dir_path = dir_path.parent
            else:
                break
    
    def clear_all_snapshots(self):
        """Remove all snapshots."""
        if self.snapshots_dir.exists():
            shutil.rmtree(self.snapshots_dir)


def create_snapshot(file_paths: List[str], task: str, project_dir: Path = None) -> Snapshot:
    """
    Convenience function to create a snapshot.
    
    Args:
        file_paths: Files that will be modified
        task: Description of the task
        project_dir: Project directory (default: cwd)
    
    Returns:
        Snapshot object
    """
    manager = RollbackManager(project_dir)
    return manager.create_snapshot(file_paths, task)


def rollback(snapshot_id: str = None, project_dir: Path = None) -> bool:
    """
    Convenience function to rollback.
    
    Args:
        snapshot_id: Specific snapshot (default: latest)
        project_dir: Project directory (default: cwd)
    
    Returns:
        True if successful
    """
    manager = RollbackManager(project_dir)
    return manager.rollback(snapshot_id)


def list_snapshots(project_dir: Path = None) -> List[Snapshot]:
    """
    Convenience function to list snapshots.
    
    Args:
        project_dir: Project directory (default: cwd)
    
    Returns:
        List of snapshots, newest first
    """
    manager = RollbackManager(project_dir)
    return manager.list_snapshots()
