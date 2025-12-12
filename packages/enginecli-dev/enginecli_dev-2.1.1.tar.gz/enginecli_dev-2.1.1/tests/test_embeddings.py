"""
Tests for the embeddings/RAG module.
Note: Some tests require OPENAI_API_KEY to be set.
"""
import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch
import numpy as np

# Skip if openai not installed
pytest.importorskip("openai")
pytest.importorskip("numpy")

from engine.embeddings import (
    build_function_semantic_text,
    build_class_semantic_text,
    build_endpoint_semantic_text,
    build_component_semantic_text,
    VectorStore,
    EmbeddedItem,
    cosine_similarity,
    RAGIndexer,
)


class TestSemanticTextBuilders:
    """Tests for semantic text builders."""
    
    def test_build_function_semantic_text(self):
        """Test building semantic text for a function."""
        func = {
            "name": "create_user",
            "docstring": "Create a new user in the system",
            "parameters": ["name", "email", "password"],
            "return_type": "User",
            "file_path": "api/users.py",
            "decorators": ["router.post"],
            "is_async": True,
        }
        
        text = build_function_semantic_text(func)
        
        assert "create_user" in text
        assert "Create a new user" in text
        assert "name" in text
        assert "email" in text
        assert "User" in text
        assert "async" in text.lower()
    
    def test_build_class_semantic_text(self):
        """Test building semantic text for a class."""
        cls = {
            "name": "UserService",
            "docstring": "Service for user operations",
            "methods": ["create", "update", "delete"],
            "bases": ["BaseService"],
            "file_path": "services/user.py",
            "decorators": [],
        }
        
        text = build_class_semantic_text(cls)
        
        assert "UserService" in text
        assert "Service for user operations" in text
        assert "create" in text
        assert "BaseService" in text
    
    def test_build_endpoint_semantic_text(self):
        """Test building semantic text for an endpoint."""
        endpoint = {
            "method": "POST",
            "path": "/api/users",
            "function_name": "create_user",
            "file_path": "routes/users.py",
        }
        
        text = build_endpoint_semantic_text(endpoint)
        
        assert "POST" in text
        assert "/api/users" in text
        assert "create_user" in text
        assert "API endpoint" in text
    
    def test_build_component_semantic_text(self):
        """Test building semantic text for a React component."""
        component = {
            "name": "UserProfile",
            "props": ["userId", "showEmail"],
            "hooks": ["useState", "useEffect"],
            "file_path": "components/UserProfile.tsx",
        }
        
        text = build_component_semantic_text(component)
        
        assert "UserProfile" in text
        assert "React component" in text
        assert "userId" in text
        assert "useState" in text


class TestVectorStore:
    """Tests for the SQLite vector store."""
    
    def test_create_store(self):
        """Test creating a vector store."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "vectors.db"
            store = VectorStore(db_path)
            
            assert db_path.exists()
    
    def test_add_and_retrieve_item(self):
        """Test adding and retrieving an item."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "vectors.db"
            store = VectorStore(db_path)
            
            embedding = np.random.rand(1536).astype(np.float32)
            item = EmbeddedItem(
                id="test-123",
                item_type="function",
                name="test_func",
                file_path="test.py",
                line_number=10,
                semantic_text="test function for testing",
                source="def test_func(): pass",
                metadata={"key": "value"},
                embedding=embedding,
            )
            
            store.add_item(item)
            
            items = store.get_all_items()
            assert len(items) == 1
            assert items[0].name == "test_func"
            assert items[0].metadata == {"key": "value"}
    
    def test_add_multiple_items(self):
        """Test adding multiple items at once."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "vectors.db"
            store = VectorStore(db_path)
            
            items = []
            for i in range(5):
                embedding = np.random.rand(1536).astype(np.float32)
                items.append(EmbeddedItem(
                    id=f"test-{i}",
                    item_type="function",
                    name=f"func_{i}",
                    file_path=f"file_{i}.py",
                    line_number=i,
                    semantic_text=f"function {i}",
                    source=f"def func_{i}(): pass",
                    metadata={},
                    embedding=embedding,
                ))
            
            store.add_items(items)
            
            assert store.get_item_count() == 5
    
    def test_clear_store(self):
        """Test clearing the store."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "vectors.db"
            store = VectorStore(db_path)
            
            embedding = np.random.rand(1536).astype(np.float32)
            item = EmbeddedItem(
                id="test-123",
                item_type="function",
                name="test_func",
                file_path="test.py",
                line_number=10,
                semantic_text="test",
                source="def test(): pass",
                metadata={},
                embedding=embedding,
            )
            store.add_item(item)
            
            assert store.get_item_count() == 1
            
            store.clear()
            
            assert store.get_item_count() == 0
    
    def test_search(self):
        """Test vector search."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "vectors.db"
            store = VectorStore(db_path)
            
            # Add items with known embeddings
            items = []
            for i in range(3):
                embedding = np.zeros(1536, dtype=np.float32)
                embedding[i] = 1.0  # Different dimensions
                items.append(EmbeddedItem(
                    id=f"test-{i}",
                    item_type="function",
                    name=f"func_{i}",
                    file_path=f"file_{i}.py",
                    line_number=i,
                    semantic_text=f"function {i}",
                    source=f"def func_{i}(): pass",
                    metadata={},
                    embedding=embedding,
                ))
            
            store.add_items(items)
            
            # Search with embedding similar to first item
            query_embedding = np.zeros(1536, dtype=np.float32)
            query_embedding[0] = 1.0
            
            results = store.search(query_embedding, top_k=2)
            
            assert len(results) == 2
            assert results[0].item.name == "func_0"
            assert results[0].score > results[1].score


class TestCosineSimilarity:
    """Tests for cosine similarity function."""
    
    def test_identical_vectors(self):
        """Test similarity of identical vectors."""
        a = np.array([1.0, 2.0, 3.0])
        b = np.array([1.0, 2.0, 3.0])
        
        sim = cosine_similarity(a, b)
        
        assert sim == pytest.approx(1.0)
    
    def test_orthogonal_vectors(self):
        """Test similarity of orthogonal vectors."""
        a = np.array([1.0, 0.0, 0.0])
        b = np.array([0.0, 1.0, 0.0])
        
        sim = cosine_similarity(a, b)
        
        assert sim == pytest.approx(0.0)
    
    def test_opposite_vectors(self):
        """Test similarity of opposite vectors."""
        a = np.array([1.0, 2.0, 3.0])
        b = np.array([-1.0, -2.0, -3.0])
        
        sim = cosine_similarity(a, b)
        
        assert sim == pytest.approx(-1.0)
    
    def test_zero_vector(self):
        """Test similarity with zero vector."""
        a = np.array([1.0, 2.0, 3.0])
        b = np.array([0.0, 0.0, 0.0])
        
        sim = cosine_similarity(a, b)
        
        assert sim == 0.0


@pytest.mark.skipif(not os.getenv('OPENAI_API_KEY'), reason="OPENAI_API_KEY not set")
class TestRAGIndexerIntegration:
    """Integration tests for RAG indexer (requires API key)."""
    
    def test_build_from_index(self):
        """Test building RAG index from code index."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            
            index_data = {
                "functions": [
                    {
                        "name": "create_user",
                        "file_path": "api/users.py",
                        "line_number": 10,
                        "source": "def create_user(): pass",
                        "parameters": ["name"],
                        "return_type": "User",
                        "docstring": "Create a user",
                        "decorators": [],
                        "is_async": False,
                    }
                ],
                "classes": [],
                "endpoints": [],
                "components": [],
                "hooks": [],
            }
            
            indexer = RAGIndexer(project_dir, os.getenv('OPENAI_API_KEY'))
            count = indexer.build_from_index(index_data, show_progress=False)
            
            assert count == 1
    
    def test_search(self):
        """Test searching with RAG."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            
            index_data = {
                "functions": [
                    {
                        "name": "create_user",
                        "file_path": "api/users.py",
                        "line_number": 10,
                        "source": "def create_user(name): pass",
                        "parameters": ["name"],
                        "return_type": "User",
                        "docstring": "Create a new user",
                        "decorators": [],
                        "is_async": False,
                    },
                    {
                        "name": "process_payment",
                        "file_path": "api/payments.py",
                        "line_number": 10,
                        "source": "def process_payment(amount): pass",
                        "parameters": ["amount"],
                        "return_type": "Payment",
                        "docstring": "Process a payment",
                        "decorators": [],
                        "is_async": False,
                    },
                ],
                "classes": [],
                "endpoints": [],
                "components": [],
                "hooks": [],
            }
            
            api_key = os.getenv('OPENAI_API_KEY')
            indexer = RAGIndexer(project_dir, api_key)
            indexer.build_from_index(index_data, show_progress=False)
            
            # Search for user-related
            results = indexer.search("user registration", top_k=2)
            
            assert len(results) > 0
            # User-related should rank higher
            assert results[0].item.name == "create_user"


class TestRAGIndexerMocked:
    """Tests for RAG indexer with mocked API."""
    
    def test_build_from_empty_index(self):
        """Test building from empty index."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            
            with patch('engine.embeddings.EmbeddingService') as mock_service:
                indexer = RAGIndexer(project_dir, "fake-key")
                
                index_data = {
                    "functions": [],
                    "classes": [],
                    "endpoints": [],
                    "components": [],
                    "hooks": [],
                }
                
                count = indexer.build_from_index(index_data, show_progress=False)
                
                assert count == 0
    
    def test_make_id_unique(self):
        """Test that IDs are unique and deterministic."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            
            with patch('engine.embeddings.EmbeddingService'):
                indexer = RAGIndexer(project_dir, "fake-key")
                
                id1 = indexer._make_id("function", "file.py", "func")
                id2 = indexer._make_id("function", "file.py", "func")
                id3 = indexer._make_id("function", "file.py", "other_func")
                
                assert id1 == id2  # Same inputs = same ID
                assert id1 != id3  # Different inputs = different ID
