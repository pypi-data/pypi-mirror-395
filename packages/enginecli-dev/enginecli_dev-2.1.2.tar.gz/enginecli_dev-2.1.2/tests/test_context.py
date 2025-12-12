"""
Tests for the context assembler.
"""
import pytest
import tempfile
from pathlib import Path

from engine.context.assembler import ContextAssembler, ContextItem


class TestContextAssembler:
    """Tests for the context assembler."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    @pytest.fixture
    def sample_index(self):
        """Sample index for testing."""
        return {
            "functions": [
                {
                    "name": "create_user",
                    "file_path": "api/users.py",
                    "line_number": 10,
                    "source": "def create_user(name: str, email: str):\n    pass",
                    "parameters": ["name", "email"],
                    "return_type": "User",
                    "docstring": "Create a new user",
                },
                {
                    "name": "delete_user",
                    "file_path": "api/users.py",
                    "line_number": 20,
                    "source": "def delete_user(user_id: int):\n    pass",
                    "parameters": ["user_id"],
                    "return_type": "None",
                    "docstring": "Delete a user",
                },
                {
                    "name": "process_payment",
                    "file_path": "api/payments.py",
                    "line_number": 10,
                    "source": "def process_payment(amount: float):\n    pass",
                    "parameters": ["amount"],
                    "return_type": "Payment",
                    "docstring": "Process a payment",
                },
                {
                    "name": "send_email",
                    "file_path": "utils/email.py",
                    "line_number": 5,
                    "source": "def send_email(to: str, subject: str):\n    pass",
                    "parameters": ["to", "subject"],
                    "return_type": "bool",
                    "docstring": "Send an email",
                },
            ],
            "classes": [
                {
                    "name": "User",
                    "file_path": "models/user.py",
                    "line_number": 1,
                    "source": "class User:\n    pass",
                    "methods": ["__init__", "save", "delete"],
                    "bases": ["BaseModel"],
                    "docstring": "User model",
                },
                {
                    "name": "Payment",
                    "file_path": "models/payment.py",
                    "line_number": 1,
                    "source": "class Payment:\n    pass",
                    "methods": ["__init__", "process", "refund"],
                    "bases": ["BaseModel"],
                    "docstring": "Payment model",
                },
            ],
            "endpoints": [
                {
                    "method": "GET",
                    "path": "/users",
                    "function_name": "list_users",
                    "file_path": "api/routes.py",
                    "line_number": 10,
                    "source": "@router.get('/users')\ndef list_users():\n    pass",
                },
                {
                    "method": "POST",
                    "path": "/users",
                    "function_name": "create_user",
                    "file_path": "api/routes.py",
                    "line_number": 15,
                    "source": "@router.post('/users')\ndef create_user():\n    pass",
                },
                {
                    "method": "POST",
                    "path": "/payments",
                    "function_name": "create_payment",
                    "file_path": "api/routes.py",
                    "line_number": 20,
                    "source": "@router.post('/payments')\ndef create_payment():\n    pass",
                },
            ],
            "components": [],
            "interfaces": [],
            "hooks": [],
        }
    
    def test_assemble_basic(self, sample_index, temp_dir):
        """Test basic context assembly."""
        assembler = ContextAssembler(sample_index, project_dir=temp_dir)
        context = assembler.assemble("create a new user")
        
        assert context is not None
        assert len(context) > 0
        assert "create_user" in context
    
    def test_relevance_ranking_by_name(self, sample_index, temp_dir):
        """Test that items with matching names rank higher."""
        assembler = ContextAssembler(sample_index, project_dir=temp_dir)
        
        # Search for user-related items
        items = assembler._gather_items("user management")
        items = assembler._rank_items(items, "user management")
        
        # User-related items should rank higher
        top_names = [item.name for item in items[:3]]
        assert any("user" in name.lower() for name in top_names)
    
    def test_relevance_ranking_by_type(self, sample_index, temp_dir):
        """Test type-based relevance boosting."""
        assembler = ContextAssembler(sample_index, project_dir=temp_dir)
        
        # Search for API endpoints
        items = assembler._gather_items("add new api endpoint")
        items = assembler._rank_items(items, "add new api endpoint")
        
        # Endpoints should rank higher
        top_types = [item.type for item in items[:3]]
        assert "endpoint" in top_types
    
    def test_file_hints_boost(self, sample_index, temp_dir):
        """Test that file hints boost relevance."""
        assembler = ContextAssembler(sample_index, project_dir=temp_dir)
        
        # Without file hints
        items_no_hints = assembler._gather_items("process something")
        items_no_hints = assembler._rank_items(items_no_hints, "process something")
        
        # With file hints
        items_with_hints = assembler._gather_items("process something", file_hints=["payments"])
        items_with_hints = assembler._rank_items(items_with_hints, "process something")
        
        # Payment-related items should rank higher with hints
        payment_rank_with_hints = next(
            (i for i, item in enumerate(items_with_hints) if "payment" in item.name.lower()),
            999
        )
        payment_rank_no_hints = next(
            (i for i, item in enumerate(items_no_hints) if "payment" in item.name.lower()),
            999
        )
        
        assert payment_rank_with_hints <= payment_rank_no_hints
    
    def test_token_budget(self, sample_index, temp_dir):
        """Test that context respects token budget."""
        # Small budget
        assembler = ContextAssembler(sample_index, max_tokens=100, project_dir=temp_dir)
        context = assembler.assemble("anything")
        
        # Should be limited (100 tokens ≈ 400 chars)
        assert len(context) < 1000
    
    def test_get_relevant_files(self, sample_index, temp_dir):
        """Test getting relevant files."""
        assembler = ContextAssembler(sample_index, project_dir=temp_dir)
        files = assembler.get_relevant_files("create user")
        
        assert isinstance(files, list)
        assert len(files) > 0
        # User-related files should be included
        assert any("user" in f.lower() for f in files)
    
    def test_format_context(self, sample_index, temp_dir):
        """Test context formatting."""
        assembler = ContextAssembler(sample_index, project_dir=temp_dir)
        
        items = [
            ContextItem(
                type="function",
                name="test_func",
                file_path="test.py",
                source="def test_func(): pass",
                relevance=1.0,
            )
        ]
        
        context = assembler._format_context(items)
        
        assert "test.py" in context
        assert "test_func" in context
        assert "def test_func()" in context
    
    def test_empty_index(self, temp_dir):
        """Test with empty index."""
        empty_index = {
            "functions": [],
            "classes": [],
            "endpoints": [],
            "components": [],
            "interfaces": [],
            "hooks": [],
        }
        
        assembler = ContextAssembler(empty_index, project_dir=temp_dir)
        context = assembler.assemble("anything")
        
        assert "No relevant code found" in context
    
    def test_select_items_budget(self, sample_index, temp_dir):
        """Test item selection respects budget."""
        assembler = ContextAssembler(sample_index, max_tokens=50, project_dir=temp_dir)
        
        items = assembler._gather_items("test")
        items = assembler._rank_items(items, "test")
        selected = assembler._select_items(items)
        
        # Should select fewer items due to small budget
        assert len(selected) < len(items)
    
    def test_component_relevance(self, temp_dir):
        """Test React component relevance."""
        index = {
            "functions": [],
            "classes": [],
            "endpoints": [],
            "components": [
                {
                    "name": "UserProfile",
                    "file_path": "components/UserProfile.tsx",
                    "source": "export const UserProfile = () => <div />;",
                },
                {
                    "name": "PaymentForm",
                    "file_path": "components/PaymentForm.tsx",
                    "source": "export const PaymentForm = () => <form />;",
                },
            ],
            "interfaces": [],
            "hooks": [],
        }
        
        assembler = ContextAssembler(index, project_dir=temp_dir)
        items = assembler._gather_items("create react component")
        items = assembler._rank_items(items, "create react component")
        
        # Components should rank high for component-related queries
        assert items[0].type == "component"


class TestContextItem:
    """Tests for ContextItem dataclass."""
    
    def test_create_context_item(self):
        """Test creating a ContextItem."""
        item = ContextItem(
            type="function",
            name="test",
            file_path="test.py",
            source="def test(): pass",
            relevance=0.5,
        )
        
        assert item.type == "function"
        assert item.name == "test"
        assert item.relevance == 0.5


class TestHybridMode:
    """Tests for hybrid search mode."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    @pytest.fixture
    def sample_index(self):
        """Sample index for testing."""
        return {
            "functions": [
                {
                    "name": "create_user",
                    "file_path": "api/users.py",
                    "line_number": 10,
                    "source": "def create_user(name: str):\n    pass",
                },
                {
                    "name": "process_payment",
                    "file_path": "api/payments.py",
                    "line_number": 10,
                    "source": "def process_payment(amount: float):\n    pass",
                },
            ],
            "classes": [],
            "endpoints": [],
            "components": [],
            "interfaces": [],
            "hooks": [],
        }
    
    def test_specific_intent_file_reference(self, sample_index, temp_dir):
        """Test that file references are detected as specific intent."""
        assembler = ContextAssembler(sample_index, project_dir=temp_dir)
        
        # Should detect file reference
        assert assembler._has_specific_intent("modify users.py file")
        assert assembler._has_specific_intent("update api/users.py")
        assert assembler._has_specific_intent("edit main.ts")
    
    def test_specific_intent_function_reference(self, sample_index, temp_dir):
        """Test that function references are detected as specific intent."""
        assembler = ContextAssembler(sample_index, project_dir=temp_dir)
        
        # Should detect function reference
        assert assembler._has_specific_intent("update the create_user function")
        assert assembler._has_specific_intent("fix process_payment")
    
    def test_no_specific_intent_vague_query(self, sample_index, temp_dir):
        """Test that vague queries are NOT detected as specific intent."""
        assembler = ContextAssembler(sample_index, project_dir=temp_dir)
        
        # Should NOT detect specific intent
        assert not assembler._has_specific_intent("add payment processing")
        assert not assembler._has_specific_intent("improve performance")
        assert not assembler._has_specific_intent("add authentication")
    
    def test_quality_result_counting(self, sample_index, temp_dir):
        """Test counting of quality results."""
        assembler = ContextAssembler(sample_index, project_dir=temp_dir)
        
        items = [
            ContextItem(type="function", name="a", file_path="a.py", source="", relevance=0.8),
            ContextItem(type="function", name="b", file_path="b.py", source="", relevance=0.6),
            ContextItem(type="function", name="c", file_path="c.py", source="", relevance=0.3),
            ContextItem(type="function", name="d", file_path="d.py", source="", relevance=0.1),
        ]
        
        # Only 2 items have relevance >= 0.5
        count = assembler._count_quality_results(items)
        assert count == 2
    
    def test_mode_keyword_explicit(self, sample_index, temp_dir):
        """Test explicit keyword mode."""
        assembler = ContextAssembler(sample_index, project_dir=temp_dir)
        context = assembler.assemble("create user", mode="keyword")
        
        assert len(context) > 0
        assert "create_user" in context
    
    def test_mode_hybrid_default(self, sample_index, temp_dir):
        """Test that hybrid is the default mode."""
        assembler = ContextAssembler(sample_index, project_dir=temp_dir)
        
        # Should work without specifying mode (defaults to hybrid)
        context = assembler.assemble("create user")
        assert len(context) > 0
    
    def test_known_files_extraction(self, sample_index, temp_dir):
        """Test that known files are extracted from index."""
        assembler = ContextAssembler(sample_index, project_dir=temp_dir)
        
        assert "api/users.py" in assembler._known_files
        assert "users.py" in assembler._known_files
        assert "payments.py" in assembler._known_files
    
    def test_known_names_extraction(self, sample_index, temp_dir):
        """Test that known names are extracted from index."""
        assembler = ContextAssembler(sample_index, project_dir=temp_dir)
        
        assert "create_user" in assembler._known_names
        assert "process_payment" in assembler._known_names
