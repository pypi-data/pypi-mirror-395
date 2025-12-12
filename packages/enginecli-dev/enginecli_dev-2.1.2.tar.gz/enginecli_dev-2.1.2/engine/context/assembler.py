"""
Context Assembler - assembles relevant code context for a task.
Supports three modes:
1. Hybrid mode (default) - Fast keyword first, RAG fallback if needed
2. RAG mode - Semantic search (slower but more accurate for vague queries)
3. Keyword mode - Fast keyword matching
"""
import json
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


# Thresholds for hybrid mode
KEYWORD_MIN_RESULTS_FOR_RAG_SKIP = 3  # Skip RAG if keyword finds this many
KEYWORD_MIN_RELEVANCE_SCORE = 0.5     # Minimum relevance to count as "good" match


@dataclass
class ContextItem:
    """A piece of context to include."""
    type: str  # function, class, component, endpoint, etc.
    name: str
    file_path: str
    source: str
    relevance: float


class ContextAssembler:
    """Assembles relevant context for code generation."""
    
    def __init__(self, index: Dict[str, Any], max_tokens: int = 8000, project_dir: Path = None):
        self.index = index
        self.max_tokens = max_tokens
        self.project_dir = project_dir or Path.cwd()
        # Rough estimate: 4 chars per token
        self.max_chars = max_tokens * 4
        
        # Check if RAG index exists
        self.rag_available = self._check_rag_available()
        
        # Build known names for specific intent detection
        self._known_files = self._extract_known_files()
        self._known_names = self._extract_known_names()
    
    def _check_rag_available(self) -> bool:
        """Check if RAG embeddings are available."""
        vectors_db = self.project_dir / ".engine" / "vectors.db"
        return vectors_db.exists()
    
    def _extract_known_files(self) -> set:
        """Extract all known file paths from index."""
        files = set()
        for key in ['functions', 'classes', 'endpoints', 'components', 'interfaces', 'hooks']:
            for item in self.index.get(key, []):
                if 'file_path' in item:
                    files.add(item['file_path'])
                    # Also add just the filename
                    files.add(Path(item['file_path']).name)
        return files
    
    def _extract_known_names(self) -> set:
        """Extract all known function/class/component names."""
        names = set()
        for key in ['functions', 'classes', 'endpoints', 'components', 'interfaces', 'hooks']:
            for item in self.index.get(key, []):
                if 'name' in item:
                    names.add(item['name'].lower())
                if 'function_name' in item:
                    names.add(item['function_name'].lower())
        return names
    
    def _has_specific_intent(self, task: str) -> bool:
        """Check if query references specific files or functions."""
        task_lower = task.lower()
        
        # Check for file references
        for file in self._known_files:
            if file.lower() in task_lower:
                return True
        
        # Check for function/class name references
        for name in self._known_names:
            # Match whole word only
            if re.search(rf'\b{re.escape(name)}\b', task_lower):
                return True
        
        # Check for file path patterns
        if re.search(r'\b\w+\.(py|ts|tsx|js|jsx)\b', task_lower):
            return True
        
        return False
    
    def _count_quality_results(self, items: List[ContextItem]) -> int:
        """Count results with good relevance scores."""
        return sum(1 for item in items if item.relevance >= KEYWORD_MIN_RELEVANCE_SCORE)
    
    def assemble(
        self,
        task: str,
        file_hints: List[str] = None,
        type_hints: List[str] = None,
        mode: str = "hybrid",  # "hybrid", "rag", "keyword"
    ) -> str:
        """
        Assemble context relevant to a task.
        
        Args:
            task: The task description
            file_hints: Files to prioritize
            type_hints: Types to prioritize (function, class, etc.)
            mode: Search mode - "hybrid" (default), "rag", or "keyword"
        
        Returns:
            Assembled context string
        """
        # Force keyword if RAG not available
        if mode in ("hybrid", "rag") and not self.rag_available:
            mode = "keyword"
        
        if mode == "keyword":
            return self._assemble_keyword(task, file_hints, type_hints)
        
        if mode == "rag":
            return self._assemble_with_rag(task, file_hints)
        
        # Hybrid mode (default) - smart decision
        return self._assemble_hybrid(task, file_hints, type_hints)
    
    def _assemble_hybrid(
        self,
        task: str,
        file_hints: List[str] = None,
        type_hints: List[str] = None,
    ) -> str:
        """
        Smart hybrid assembly - keyword first, RAG fallback if needed.
        
        Strategy:
        1. If query has specific intent (file/function name) → keyword only
        2. Run fast keyword search
        3. If keyword finds >= 3 quality results → use keyword
        4. Otherwise → fall back to RAG for semantic search
        """
        # Step 1: Check for specific intent
        if self._has_specific_intent(task):
            # User referenced specific code - keyword is sufficient
            return self._assemble_keyword(task, file_hints, type_hints)
        
        # Step 2: Run fast keyword search
        items = self._gather_items(task, file_hints, type_hints)
        items = self._rank_items(items, task)
        
        # Step 3: Check if keyword found enough quality results
        quality_count = self._count_quality_results(items[:10])
        
        if quality_count >= KEYWORD_MIN_RESULTS_FOR_RAG_SKIP:
            # Keyword found good matches - no need for RAG
            items = self._select_items(items)
            return self._format_context(items)
        
        # Step 4: Fall back to RAG for better semantic matching
        try:
            return self._assemble_with_rag(task, file_hints)
        except Exception:
            # If RAG fails, use keyword results anyway
            items = self._select_items(items)
            return self._format_context(items)
    
    def _assemble_keyword(
        self,
        task: str,
        file_hints: List[str] = None,
        type_hints: List[str] = None,
    ) -> str:
        """Assemble context using keyword matching only."""
        items = self._gather_items(task, file_hints, type_hints)
        items = self._rank_items(items, task)
        items = self._select_items(items)
        return self._format_context(items)
    
    def _assemble_with_rag(self, task: str, file_hints: List[str] = None) -> str:
        """Assemble context using RAG vector search."""
        from engine.embeddings import RAGIndexer
        
        indexer = RAGIndexer(self.project_dir)
        
        # Search for relevant items
        results = indexer.search(task, top_k=15)
        
        if not results:
            # Fall back to keyword search
            return self._assemble_keyword(task, file_hints)
        
        # Convert search results to ContextItems
        items = []
        for result in results:
            items.append(ContextItem(
                type=result.item.item_type,
                name=result.item.name,
                file_path=result.item.file_path,
                source=result.item.source,
                relevance=result.score,
            ))
        
        # Boost items matching file hints
        if file_hints:
            for item in items:
                for hint in file_hints:
                    if hint.lower() in item.file_path.lower():
                        item.relevance += 0.5
        
        # Re-sort after boosting
        items.sort(key=lambda x: x.relevance, reverse=True)
        
        # Select within token budget
        items = self._select_items(items)
        
        return self._format_context(items)
    
    def _gather_items(
        self,
        task: str,
        file_hints: List[str] = None,
        type_hints: List[str] = None,
    ) -> List[ContextItem]:
        """Gather all potential context items."""
        items = []
        
        # Python constructs
        for func in self.index.get("functions", []):
            items.append(ContextItem(
                type="function",
                name=func["name"],
                file_path=func["file_path"],
                source=func["source"],
                relevance=0.0,
            ))
        
        for cls in self.index.get("classes", []):
            items.append(ContextItem(
                type="class",
                name=cls["name"],
                file_path=cls["file_path"],
                source=cls["source"],
                relevance=0.0,
            ))
        
        for endpoint in self.index.get("endpoints", []):
            items.append(ContextItem(
                type="endpoint",
                name=f"{endpoint['method']} {endpoint['path']}",
                file_path=endpoint["file_path"],
                source=endpoint["source"],
                relevance=0.0,
            ))
        
        # TypeScript/React constructs
        for comp in self.index.get("components", []):
            items.append(ContextItem(
                type="component",
                name=comp["name"],
                file_path=comp["file_path"],
                source=comp["source"],
                relevance=0.0,
            ))
        
        for iface in self.index.get("interfaces", []):
            items.append(ContextItem(
                type="interface",
                name=iface["name"],
                file_path=iface["file_path"],
                source=iface["source"],
                relevance=0.0,
            ))
        
        for hook in self.index.get("hooks", []):
            items.append(ContextItem(
                type="hook",
                name=hook["name"],
                file_path=hook["file_path"],
                source=hook["source"],
                relevance=0.0,
            ))
        
        # Boost items matching file hints
        if file_hints:
            for item in items:
                for hint in file_hints:
                    if hint.lower() in item.file_path.lower():
                        item.relevance += 0.5
        
        # Boost items matching type hints
        if type_hints:
            for item in items:
                if item.type in type_hints:
                    item.relevance += 0.3
        
        return items
    
    def _rank_items(self, items: List[ContextItem], task: str) -> List[ContextItem]:
        """Rank items by relevance to the task."""
        task_lower = task.lower()
        task_words = set(task_lower.split())
        
        for item in items:
            # Name matching (strong signal)
            name_lower = item.name.lower()
            if name_lower in task_lower:
                item.relevance += 1.0
            
            # Word overlap
            name_words = set(name_lower.replace("_", " ").replace("-", " ").split())
            overlap = len(task_words & name_words)
            item.relevance += overlap * 0.3
            
            # File path matching
            path_lower = item.file_path.lower()
            if any(word in path_lower for word in task_words if len(word) > 3):
                item.relevance += 0.4
            
            # Source content matching
            source_lower = item.source.lower()
            for word in task_words:
                if len(word) > 3 and word in source_lower:
                    item.relevance += 0.1
            
            # Type-based boost for common tasks
            if "api" in task_lower or "endpoint" in task_lower or "route" in task_lower:
                if item.type == "endpoint":
                    item.relevance += 0.5
            
            if "component" in task_lower or "react" in task_lower:
                if item.type == "component":
                    item.relevance += 0.5
            
            if "model" in task_lower or "class" in task_lower or "schema" in task_lower:
                if item.type == "class":
                    item.relevance += 0.5
            
            if "hook" in task_lower:
                if item.type == "hook":
                    item.relevance += 0.5
        
        # Sort by relevance
        items.sort(key=lambda x: x.relevance, reverse=True)
        
        return items
    
    def _select_items(self, items: List[ContextItem]) -> List[ContextItem]:
        """Select items that fit within token budget."""
        selected = []
        total_chars = 0
        
        for item in items:
            item_chars = len(item.source) + len(item.file_path) + 50  # overhead
            
            if total_chars + item_chars <= self.max_chars:
                selected.append(item)
                total_chars += item_chars
            
            # Stop if we've selected enough high-relevance items
            if len(selected) >= 20:
                break
        
        return selected
    
    def _format_context(self, items: List[ContextItem]) -> str:
        """Format selected items into context string."""
        if not items:
            return "No relevant code found in the index."
        
        sections = []
        
        # Group by file
        by_file: Dict[str, List[ContextItem]] = {}
        for item in items:
            if item.file_path not in by_file:
                by_file[item.file_path] = []
            by_file[item.file_path].append(item)
        
        for file_path, file_items in by_file.items():
            section = f"### {file_path}\n\n"
            for item in file_items:
                section += f"**{item.type}: {item.name}**\n"
                section += f"```\n{item.source}\n```\n\n"
            sections.append(section)
        
        return "\n".join(sections)
    
    def get_relevant_files(self, task: str, mode: str = "hybrid") -> List[str]:
        """Get list of files relevant to a task."""
        # Force keyword if RAG not available
        if mode in ("hybrid", "rag") and not self.rag_available:
            mode = "keyword"
        
        if mode == "rag":
            return self._get_files_rag(task)
        
        if mode == "keyword":
            return self._get_files_keyword(task)
        
        # Hybrid mode
        return self._get_files_hybrid(task)
    
    def _get_files_hybrid(self, task: str) -> List[str]:
        """Get files using hybrid approach."""
        # Check specific intent
        if self._has_specific_intent(task):
            return self._get_files_keyword(task)
        
        # Run keyword search
        items = self._gather_items(task)
        items = self._rank_items(items, task)
        quality_count = self._count_quality_results(items[:10])
        
        if quality_count >= KEYWORD_MIN_RESULTS_FOR_RAG_SKIP:
            # Use keyword results
            files = []
            seen = set()
            for item in items[:10]:
                if item.file_path not in seen:
                    files.append(item.file_path)
                    seen.add(item.file_path)
            return files
        
        # Fall back to RAG
        try:
            return self._get_files_rag(task)
        except Exception:
            return self._get_files_keyword(task)
    
    def _get_files_keyword(self, task: str) -> List[str]:
        """Get files using keyword search."""
        items = self._gather_items(task)
        items = self._rank_items(items, task)
        
        files = []
        seen = set()
        for item in items[:10]:
            if item.file_path not in seen:
                files.append(item.file_path)
                seen.add(item.file_path)
        return files
    
    def _get_files_rag(self, task: str) -> List[str]:
        """Get files using RAG search."""
        from engine.embeddings import RAGIndexer
        
        indexer = RAGIndexer(self.project_dir)
        results = indexer.search(task, top_k=10)
        
        files = []
        seen = set()
        for result in results:
            if result.item.file_path not in seen:
                files.append(result.item.file_path)
                seen.add(result.item.file_path)
        return files


def load_index(index_path: Path) -> Dict[str, Any]:
    """Load index from file."""
    with open(index_path) as f:
        return json.load(f)


def assemble_context(
    index_path: Path,
    task: str,
    max_tokens: int = 8000,
    file_hints: List[str] = None,
    project_dir: Path = None,
    mode: str = "hybrid",
) -> str:
    """
    Assemble context for a task.
    
    Args:
        index_path: Path to index JSON file
        task: Task description
        max_tokens: Maximum context tokens
        file_hints: Files to prioritize
        project_dir: Project directory for RAG
        mode: Search mode - "hybrid", "rag", or "keyword"
    
    Returns:
        Assembled context string
    """
    index = load_index(index_path)
    assembler = ContextAssembler(index, max_tokens, project_dir or index_path.parent)
    return assembler.assemble(task, file_hints, mode=mode)
