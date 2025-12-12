"""
Incremental Indexer - only re-indexes files that have changed.

This is critical for performance on large codebases (100k+ LOC).
Instead of re-scanning everything, we:
1. Track file modification times and content hashes
2. Only re-parse files that have changed
3. Remove entries for deleted files
4. Merge new/updated entries with existing index
"""
import hashlib
import json
import os
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple

from engine.indexer.python import PythonIndexer, index_python_project
from engine.indexer.typescript import TypeScriptIndexer, index_typescript_project


@dataclass
class FileMetadata:
    """Metadata for tracking file changes."""
    path: str
    mtime: float  # Modification time
    size: int     # File size in bytes
    content_hash: str  # SHA256 of content


@dataclass
class IndexState:
    """
    State of the index including file metadata.
    Stored in .engine/index_state.json
    """
    version: str = "1.0"
    language: str = "python"
    last_indexed: str = ""
    files: Dict[str, Dict] = field(default_factory=dict)  # path -> FileMetadata as dict
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "IndexState":
        return cls(
            version=data.get("version", "1.0"),
            language=data.get("language", "python"),
            last_indexed=data.get("last_indexed", ""),
            files=data.get("files", {}),
        )


class IncrementalIndexer:
    """
    Manages incremental indexing of codebases.
    
    Tracks file changes and only re-indexes what's necessary.
    """
    
    def __init__(self, root_dir: Path, language: str = "python"):
        self.root_dir = root_dir
        self.language = language
        self.engine_dir = root_dir / ".engine"
        self.index_file = self.engine_dir / "index.json"
        self.state_file = self.engine_dir / "index_state.json"
        
        # File extensions to index
        self.extensions = {
            "python": [".py"],
            "typescript": [".ts", ".tsx", ".js", ".jsx"],
        }
    
    def _get_file_metadata(self, file_path: Path) -> FileMetadata:
        """Get metadata for a file."""
        stat = file_path.stat()
        
        # Calculate content hash
        with open(file_path, "rb") as f:
            content_hash = hashlib.sha256(f.read()).hexdigest()
        
        return FileMetadata(
            path=str(file_path.relative_to(self.root_dir)),
            mtime=stat.st_mtime,
            size=stat.st_size,
            content_hash=content_hash,
        )
    
    def _scan_files(self, exclude_dirs: List[str] = None) -> Dict[str, FileMetadata]:
        """Scan all relevant files and return their metadata."""
        exclude_dirs = exclude_dirs or [
            'venv', 'env', '.venv', '__pycache__', 'node_modules', 
            '.git', '.engine', 'dist', 'build', '.next'
        ]
        
        files = {}
        extensions = self.extensions.get(self.language, [".py"])
        
        for ext in extensions:
            for file_path in self.root_dir.rglob(f"*{ext}"):
                # Skip excluded directories
                if any(excl in file_path.parts for excl in exclude_dirs):
                    continue
                
                try:
                    metadata = self._get_file_metadata(file_path)
                    files[metadata.path] = metadata
                except (OSError, IOError):
                    continue
        
        return files
    
    def _load_state(self) -> Optional[IndexState]:
        """Load previous index state."""
        if not self.state_file.exists():
            return None
        
        try:
            with open(self.state_file) as f:
                data = json.load(f)
            return IndexState.from_dict(data)
        except (json.JSONDecodeError, IOError):
            return None
    
    def _save_state(self, state: IndexState):
        """Save index state."""
        self.engine_dir.mkdir(exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump(state.to_dict(), f, indent=2)
    
    def _load_index(self) -> Optional[Dict[str, Any]]:
        """Load existing index."""
        if not self.index_file.exists():
            return None
        
        try:
            with open(self.index_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def _save_index(self, index: Dict[str, Any]):
        """Save index."""
        self.engine_dir.mkdir(exist_ok=True)
        with open(self.index_file, "w") as f:
            json.dump(index, f, indent=2)
    
    def _file_changed(
        self, 
        current: FileMetadata, 
        previous: Dict
    ) -> bool:
        """Check if a file has changed."""
        # Compare mtime first (fast)
        if current.mtime != previous.get("mtime"):
            return True
        
        # Compare size (fast)
        if current.size != previous.get("size"):
            return True
        
        # Compare hash (most reliable)
        if current.content_hash != previous.get("content_hash"):
            return True
        
        return False
    
    def _compute_changes(
        self,
        current_files: Dict[str, FileMetadata],
        previous_state: Optional[IndexState],
    ) -> Tuple[Set[str], Set[str], Set[str]]:
        """
        Compute what files have changed.
        
        Returns:
            Tuple of (added, modified, deleted) file paths
        """
        added = set()
        modified = set()
        deleted = set()
        
        if previous_state is None:
            # No previous state - everything is new
            return set(current_files.keys()), set(), set()
        
        previous_files = previous_state.files
        
        # Find added and modified files
        for path, metadata in current_files.items():
            if path not in previous_files:
                added.add(path)
            elif self._file_changed(metadata, previous_files[path]):
                modified.add(path)
        
        # Find deleted files
        for path in previous_files:
            if path not in current_files:
                deleted.add(path)
        
        return added, modified, deleted
    
    def _index_files(self, file_paths: Set[str]) -> Dict[str, Any]:
        """Index specific files."""
        if not file_paths:
            return {
                "functions": [],
                "classes": [],
                "endpoints": [],
                "imports": [],
                "components": [],
                "interfaces": [],
                "hooks": [],
            }
        
        if self.language == "python":
            indexer = PythonIndexer(self.root_dir)
            for path in file_paths:
                try:
                    indexer._index_file(self.root_dir / path)
                except Exception:
                    continue
            return indexer.to_dict()
        else:
            indexer = TypeScriptIndexer(self.root_dir)
            for path in file_paths:
                try:
                    indexer._index_file(self.root_dir / path)
                except Exception:
                    continue
            return indexer.to_dict()
    
    def _merge_indices(
        self,
        existing: Dict[str, Any],
        new_entries: Dict[str, Any],
        modified_files: Set[str],
        deleted_files: Set[str],
    ) -> Dict[str, Any]:
        """
        Merge new index entries with existing index.
        
        Removes entries from modified/deleted files, adds new entries.
        """
        result = {}
        
        # Files to remove entries from
        files_to_remove = modified_files | deleted_files
        
        for key in ["functions", "classes", "endpoints", "imports", 
                    "components", "interfaces", "hooks"]:
            existing_items = existing.get(key, [])
            new_items = new_entries.get(key, [])
            
            # Filter out items from modified/deleted files
            filtered = [
                item for item in existing_items
                if item.get("file_path") not in files_to_remove
            ]
            
            # Add new items
            result[key] = filtered + new_items
        
        return result
    
    def index(
        self, 
        force: bool = False,
        exclude_dirs: List[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, int]]:
        """
        Perform incremental index.
        
        Args:
            force: If True, re-index everything
            exclude_dirs: Directories to exclude
        
        Returns:
            Tuple of (index_data, stats)
            stats contains: added, modified, deleted, unchanged counts
        """
        # Scan current files
        current_files = self._scan_files(exclude_dirs)
        
        # Load previous state
        previous_state = None if force else self._load_state()
        existing_index = None if force else self._load_index()
        
        # Compute changes
        added, modified, deleted = self._compute_changes(
            current_files, previous_state
        )
        
        # Calculate unchanged
        unchanged = len(current_files) - len(added) - len(modified)
        
        stats = {
            "added": len(added),
            "modified": len(modified),
            "deleted": len(deleted),
            "unchanged": unchanged,
            "total": len(current_files),
        }
        
        # Fast path: nothing changed
        if not added and not modified and not deleted and existing_index:
            return existing_index, stats
        
        # Index changed files
        files_to_index = added | modified
        new_entries = self._index_files(files_to_index)
        
        # Merge with existing or start fresh
        if existing_index and not force:
            final_index = self._merge_indices(
                existing_index, new_entries, modified, deleted
            )
        else:
            final_index = new_entries
        
        # Save state
        new_state = IndexState(
            language=self.language,
            last_indexed=datetime.now().isoformat(),
            files={path: asdict(meta) for path, meta in current_files.items()},
        )
        
        self._save_state(new_state)
        self._save_index(final_index)
        
        return final_index, stats


def incremental_index(
    root_dir: Path,
    language: str = "python",
    force: bool = False,
) -> Tuple[Dict[str, Any], Dict[str, int]]:
    """
    Convenience function for incremental indexing.
    
    Args:
        root_dir: Project root directory
        language: "python" or "typescript"
        force: If True, re-index everything
    
    Returns:
        Tuple of (index_data, stats)
    """
    indexer = IncrementalIndexer(root_dir, language)
    return indexer.index(force=force)
