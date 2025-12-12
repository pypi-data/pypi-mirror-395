"""
Embeddings module for RAG-based context retrieval.
Uses sentence-transformers for FREE local embeddings (no API key needed).
"""
import json
import sqlite3
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    HAS_EMBEDDINGS = True
except ImportError:
    HAS_EMBEDDINGS = False


# ============================================================
# Configuration
# ============================================================

# Using a small, fast model optimized for code/technical content
# all-MiniLM-L6-v2 is ~80MB, fast, and works well
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384  # Dimension for MiniLM
DEFAULT_TOP_K = 10


# ============================================================
# Data Classes
# ============================================================

@dataclass
class EmbeddedItem:
    """An indexed item with its embedding."""
    id: str
    item_type: str  # 'function', 'class', 'endpoint', 'component'
    name: str
    file_path: str
    line_number: int
    semantic_text: str  # The text that was embedded
    source: str  # Actual source code
    metadata: Dict[str, Any]  # Additional info
    embedding: Optional[np.ndarray] = None


@dataclass 
class SearchResult:
    """A search result with similarity score."""
    item: EmbeddedItem
    score: float


# ============================================================
# Semantic Text Builders
# ============================================================

def build_function_semantic_text(func: Dict) -> str:
    """Build searchable text for a function."""
    parts = [
        func.get('name', ''),
        func.get('docstring', '') or '',
        f"Parameters: {', '.join(func.get('parameters', []))}",
        f"Returns: {func.get('return_type', 'None')}",
        f"File: {func.get('file_path', '')}",
    ]
    if func.get('decorators'):
        parts.append(f"Decorators: {', '.join(func.get('decorators', []))}")
    if func.get('is_async'):
        parts.append("async function")
    return ' '.join(parts)


def build_class_semantic_text(cls: Dict) -> str:
    """Build searchable text for a class."""
    parts = [
        f"class {cls.get('name', '')}",
        cls.get('docstring', '') or '',
        f"Methods: {', '.join(cls.get('methods', []))}",
        f"Inherits: {', '.join(cls.get('bases', []))}",
        f"File: {cls.get('file_path', '')}",
    ]
    if cls.get('decorators'):
        parts.append(f"Decorators: {', '.join(cls.get('decorators', []))}")
    return ' '.join(parts)


def build_endpoint_semantic_text(endpoint: Dict) -> str:
    """Build searchable text for an API endpoint."""
    parts = [
        f"{endpoint.get('method', 'GET')} {endpoint.get('path', '')}",
        endpoint.get('function_name', ''),
        f"API endpoint route handler",
        f"File: {endpoint.get('file_path', '')}",
    ]
    return ' '.join(parts)


def build_component_semantic_text(component: Dict) -> str:
    """Build searchable text for a React component."""
    parts = [
        f"React component {component.get('name', '')}",
        f"Props: {', '.join(component.get('props', []))}",
        f"File: {component.get('file_path', '')}",
    ]
    if component.get('hooks'):
        parts.append(f"Hooks: {', '.join(component.get('hooks', []))}")
    return ' '.join(parts)


def build_hook_semantic_text(hook: Dict) -> str:
    """Build searchable text for a React hook."""
    parts = [
        f"React hook {hook.get('name', '')}",
        f"Custom hook function",
        f"File: {hook.get('file_path', '')}",
    ]
    return ' '.join(parts)


# ============================================================
# Embedding Service
# ============================================================

class EmbeddingService:
    """Handles embedding generation using sentence-transformers (FREE, local)."""
    
    _model = None  # Singleton to avoid reloading
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize embedding service. api_key is ignored (kept for compatibility)."""
        if not HAS_EMBEDDINGS:
            raise ImportError(
                "sentence-transformers package required. Run: pip install sentence-transformers"
            )
        
        # Use singleton pattern - model is loaded once
        if EmbeddingService._model is None:
            EmbeddingService._model = SentenceTransformer(EMBEDDING_MODEL)
        
        self.model = EmbeddingService._model
    
    def embed_text(self, text: str) -> np.ndarray:
        """Embed a single text string."""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.astype(np.float32)
    
    def embed_batch(self, texts: List[str], batch_size: int = 100) -> List[np.ndarray]:
        """Embed multiple texts in batches."""
        embeddings = self.model.encode(texts, convert_to_numpy=True, batch_size=batch_size)
        return [e.astype(np.float32) for e in embeddings]


# ============================================================
# Vector Store (SQLite + NumPy)
# ============================================================

class VectorStore:
    """SQLite-based vector store for embeddings."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize the database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id TEXT PRIMARY KEY,
                item_type TEXT,
                name TEXT,
                file_path TEXT,
                line_number INTEGER,
                semantic_text TEXT,
                source TEXT,
                metadata TEXT,
                embedding BLOB
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_item_type ON items(item_type)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_file_path ON items(file_path)
        """)
        
        conn.commit()
        conn.close()
    
    def clear(self):
        """Clear all items from the store."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("DELETE FROM items")
        conn.commit()
        conn.close()
    
    def add_item(self, item: EmbeddedItem):
        """Add an item to the store."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        embedding_bytes = item.embedding.tobytes() if item.embedding is not None else None
        
        cursor.execute("""
            INSERT OR REPLACE INTO items 
            (id, item_type, name, file_path, line_number, semantic_text, source, metadata, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.id,
            item.item_type,
            item.name,
            item.file_path,
            item.line_number,
            item.semantic_text,
            item.source,
            json.dumps(item.metadata),
            embedding_bytes,
        ))
        
        conn.commit()
        conn.close()
    
    def add_items(self, items: List[EmbeddedItem]):
        """Add multiple items to the store."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for item in items:
            embedding_bytes = item.embedding.tobytes() if item.embedding is not None else None
            cursor.execute("""
                INSERT OR REPLACE INTO items 
                (id, item_type, name, file_path, line_number, semantic_text, source, metadata, embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.id,
                item.item_type,
                item.name,
                item.file_path,
                item.line_number,
                item.semantic_text,
                item.source,
                json.dumps(item.metadata),
                embedding_bytes,
            ))
        
        conn.commit()
        conn.close()
    
    def get_all_items(self) -> List[EmbeddedItem]:
        """Get all items from the store."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM items")
        rows = cursor.fetchall()
        conn.close()
        
        items = []
        for row in rows:
            embedding = np.frombuffer(row[8], dtype=np.float32) if row[8] else None
            items.append(EmbeddedItem(
                id=row[0],
                item_type=row[1],
                name=row[2],
                file_path=row[3],
                line_number=row[4],
                semantic_text=row[5],
                source=row[6],
                metadata=json.loads(row[7]),
                embedding=embedding,
            ))
        
        return items
    
    def get_item_count(self) -> int:
        """Get the number of items in the store."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def search(self, query_embedding: np.ndarray, top_k: int = DEFAULT_TOP_K) -> List[SearchResult]:
        """Search for similar items using cosine similarity."""
        items = self.get_all_items()
        
        if not items:
            return []
        
        # Calculate cosine similarity for all items
        results = []
        for item in items:
            if item.embedding is not None:
                score = cosine_similarity(query_embedding, item.embedding)
                results.append(SearchResult(item=item, score=score))
        
        # Sort by score descending
        results.sort(key=lambda x: x.score, reverse=True)
        
        return results[:top_k]


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# ============================================================
# RAG Index Builder
# ============================================================

class RAGIndexer:
    """Builds and manages the RAG index for a codebase."""
    
    def __init__(self, project_dir: Path, api_key: Optional[str] = None):
        """Initialize RAG indexer. api_key is ignored (kept for compatibility)."""
        self.project_dir = project_dir
        self.index_dir = project_dir / ".engine"
        self.index_dir.mkdir(exist_ok=True)
        
        self.store = VectorStore(self.index_dir / "vectors.db")
        # Always create embedding service (it's free now!)
        self.embedding_service = EmbeddingService()
    
    def build_from_index(self, index_data: Dict[str, Any], show_progress: bool = True) -> int:
        """
        Build RAG index from existing code index.
        
        Args:
            index_data: The parsed code index (functions, classes, endpoints, etc.)
            show_progress: Show progress output
        
        Returns:
            Number of items indexed
        """
        # Clear existing index
        self.store.clear()
        
        # Collect all items to embed
        items_to_embed: List[EmbeddedItem] = []
        
        # Process functions
        for func in index_data.get('functions', []):
            item_id = self._make_id('function', func['file_path'], func['name'])
            items_to_embed.append(EmbeddedItem(
                id=item_id,
                item_type='function',
                name=func['name'],
                file_path=func['file_path'],
                line_number=func['line_number'],
                semantic_text=build_function_semantic_text(func),
                source=func.get('source', ''),
                metadata={
                    'parameters': func.get('parameters', []),
                    'return_type': func.get('return_type'),
                    'decorators': func.get('decorators', []),
                    'is_async': func.get('is_async', False),
                    'docstring': func.get('docstring'),
                },
            ))
        
        # Process classes
        for cls in index_data.get('classes', []):
            item_id = self._make_id('class', cls['file_path'], cls['name'])
            items_to_embed.append(EmbeddedItem(
                id=item_id,
                item_type='class',
                name=cls['name'],
                file_path=cls['file_path'],
                line_number=cls['line_number'],
                semantic_text=build_class_semantic_text(cls),
                source=cls.get('source', ''),
                metadata={
                    'methods': cls.get('methods', []),
                    'bases': cls.get('bases', []),
                    'decorators': cls.get('decorators', []),
                    'docstring': cls.get('docstring'),
                },
            ))
        
        # Process API endpoints
        for endpoint in index_data.get('endpoints', []):
            item_id = self._make_id('endpoint', endpoint['file_path'], f"{endpoint['method']}_{endpoint['path']}")
            items_to_embed.append(EmbeddedItem(
                id=item_id,
                item_type='endpoint',
                name=f"{endpoint['method']} {endpoint['path']}",
                file_path=endpoint['file_path'],
                line_number=endpoint['line_number'],
                semantic_text=build_endpoint_semantic_text(endpoint),
                source=endpoint.get('source', ''),
                metadata={
                    'method': endpoint['method'],
                    'path': endpoint['path'],
                    'function_name': endpoint['function_name'],
                },
            ))
        
        # Process React components
        for component in index_data.get('components', []):
            item_id = self._make_id('component', component['file_path'], component['name'])
            items_to_embed.append(EmbeddedItem(
                id=item_id,
                item_type='component',
                name=component['name'],
                file_path=component['file_path'],
                line_number=component.get('line_number', 1),
                semantic_text=build_component_semantic_text(component),
                source=component.get('source', ''),
                metadata={
                    'props': component.get('props', []),
                    'hooks': component.get('hooks', []),
                },
            ))
        
        # Process React hooks
        for hook in index_data.get('hooks', []):
            item_id = self._make_id('hook', hook['file_path'], hook['name'])
            items_to_embed.append(EmbeddedItem(
                id=item_id,
                item_type='hook',
                name=hook['name'],
                file_path=hook['file_path'],
                line_number=hook.get('line_number', 1),
                semantic_text=build_hook_semantic_text(hook),
                source=hook.get('source', ''),
                metadata={},
            ))
        
        if not items_to_embed:
            return 0
        
        if show_progress:
            print(f"Embedding {len(items_to_embed)} items...")
        
        # Generate embeddings in batch
        semantic_texts = [item.semantic_text for item in items_to_embed]
        embeddings = self.embedding_service.embed_batch(semantic_texts)
        
        # Attach embeddings to items
        for item, embedding in zip(items_to_embed, embeddings):
            item.embedding = embedding
        
        # Store in vector database
        self.store.add_items(items_to_embed)
        
        if show_progress:
            print(f"Indexed {len(items_to_embed)} items")
        
        return len(items_to_embed)
    
    def search(self, query: str, top_k: int = DEFAULT_TOP_K) -> List[SearchResult]:
        """
        Search for relevant code items.
        
        Args:
            query: The search query (e.g., "add stripe payment webhook")
            top_k: Number of results to return
        
        Returns:
            List of search results with scores
        """
        query_embedding = self.embedding_service.embed_text(query)
        return self.store.search(query_embedding, top_k)
    
    def _make_id(self, item_type: str, file_path: str, name: str) -> str:
        """Create a unique ID for an item."""
        content = f"{item_type}:{file_path}:{name}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]


# ============================================================
# High-Level API
# ============================================================

def build_rag_index(
    project_dir: Path,
    index_data: Dict[str, Any],
    api_key: Optional[str] = None,
) -> int:
    """
    Build a RAG index for a project.
    
    Args:
        project_dir: Project root directory
        index_data: Parsed code index from AST indexer
        api_key: Ignored (kept for compatibility)
    
    Returns:
        Number of items indexed
    """
    indexer = RAGIndexer(project_dir)
    return indexer.build_from_index(index_data)


def search_codebase(
    project_dir: Path,
    query: str,
    top_k: int = DEFAULT_TOP_K,
    api_key: Optional[str] = None,
) -> List[SearchResult]:
    """
    Search the codebase using RAG.
    
    Args:
        project_dir: Project root directory
        query: Search query
        top_k: Number of results
        api_key: Ignored (kept for compatibility)
    
    Returns:
        List of relevant search results
    """
    indexer = RAGIndexer(project_dir)
    return indexer.search(query, top_k)
