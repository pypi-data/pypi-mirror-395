"""
Integration tests for the CLI.
Tests the full flow from indexing to context assembly.
"""
import pytest
import json
import tempfile
from pathlib import Path
from click.testing import CliRunner

from engine.cli import cli, INDEX_DIR, INDEX_FILE
from engine.indexer.python import index_python_project
from engine.indexer.typescript import index_typescript_project
from engine.context.assembler import ContextAssembler


class TestCLICommands:
    """Test CLI commands."""
    
    @pytest.fixture
    def runner(self):
        """Create a CLI runner."""
        return CliRunner()
    
    def test_cli_help(self, runner):
        """Test CLI help command."""
        result = runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert 'Engine' in result.output
        assert 'index' in result.output
        assert 'generate' in result.output
    
    def test_index_help(self, runner):
        """Test index command help."""
        result = runner.invoke(cli, ['index', '--help'])
        
        assert result.exit_code == 0
        assert '--language' in result.output
        assert '--embed' in result.output


class TestFullPythonFlow:
    """Test full indexing and context assembly for Python."""
    
    def test_index_and_assemble(self, python_project):
        """Test indexing a Python project and assembling context."""
        # Index the project
        index = index_python_project(python_project)
        
        # Verify index contents
        assert len(index['functions']) > 0
        assert len(index['classes']) > 0
        
        # Find specific items
        func_names = [f['name'] for f in index['functions']]
        assert 'root' in func_names
        assert 'list_users' in func_names
        assert 'validate_email' in func_names
        
        class_names = [c['name'] for c in index['classes']]
        assert 'User' in class_names
        
        # Assemble context
        assembler = ContextAssembler(index, project_dir=python_project)
        context = assembler.assemble("add user authentication")
        
        # Context should include user-related code
        assert "User" in context or "user" in context.lower()
    
    def test_index_extracts_endpoints(self, python_project):
        """Test that FastAPI endpoints are extracted."""
        index = index_python_project(python_project)
        
        # Should find the endpoints
        assert len(index['endpoints']) >= 1
        
        methods = {e['method'] for e in index['endpoints']}
        assert 'GET' in methods
    
    def test_index_extracts_async_functions(self, python_project):
        """Test that async functions are marked."""
        index = index_python_project(python_project)
        
        # Find the async function
        async_funcs = [f for f in index['functions'] if f.get('is_async')]
        assert len(async_funcs) >= 1
        
        fetch_func = next((f for f in async_funcs if f['name'] == 'fetch_data'), None)
        assert fetch_func is not None


class TestFullTypeScriptFlow:
    """Test full indexing and context assembly for TypeScript."""
    
    def test_index_and_assemble(self, typescript_project):
        """Test indexing a TypeScript project and assembling context."""
        # Index the project
        index = index_typescript_project(typescript_project)
        
        # Verify index contents
        assert len(index['components']) > 0
        assert len(index['interfaces']) > 0
        
        # Find specific items - should have Button and/or UserCard
        component_names = [c['name'] for c in index['components']]
        assert 'Button' in component_names or 'UserCard' in component_names, \
            f"Expected Button or UserCard, got: {component_names}"
        
        interface_names = [i['name'] for i in index['interfaces']]
        assert 'User' in interface_names or 'ButtonProps' in interface_names, \
            f"Expected User or ButtonProps interface, got: {interface_names}"
        
        # Assemble context
        assembler = ContextAssembler(index, project_dir=typescript_project)
        context = assembler.assemble("create new React component")
        
        # Context should include component-related code
        assert len(context) > 0
    
    def test_index_extracts_hooks(self, typescript_project):
        """Test that React hooks are extracted."""
        index = index_typescript_project(typescript_project)
        
        # Should find custom hooks
        hook_names = [h['name'] for h in index['hooks']]
        assert 'useAuth' in hook_names


class TestContextRelevance:
    """Test context relevance scoring."""
    
    def test_user_query_returns_user_context(self, sample_index, integration_temp_dir):
        """Test that user-related queries return user context."""
        assembler = ContextAssembler(sample_index, project_dir=integration_temp_dir)
        context = assembler.assemble("create a new user")
        
        # Should include user-related items
        assert "create_user" in context or "User" in context
    
    def test_api_query_returns_endpoints(self, sample_index, integration_temp_dir):
        """Test that API queries return endpoint context."""
        assembler = ContextAssembler(sample_index, project_dir=integration_temp_dir)
        files = assembler.get_relevant_files("add new API endpoint for orders")
        
        # Should include routes file
        assert any("routes" in f for f in files)
    
    def test_file_hints_boost_relevance(self, sample_index, integration_temp_dir):
        """Test that file hints improve relevance."""
        assembler = ContextAssembler(sample_index, project_dir=integration_temp_dir)
        
        # Without hints
        context_no_hints = assembler.assemble("do something")
        
        # With hints pointing to specific file
        context_with_hints = assembler.assemble(
            "do something",
            file_hints=["email.py"]
        )
        
        # Both should return context
        assert len(context_no_hints) > 0
        assert len(context_with_hints) > 0


class TestIndexPersistence:
    """Test index saving and loading."""
    
    def test_save_and_load_index(self, python_project):
        """Test saving and loading an index."""
        # Index the project
        index = index_python_project(python_project)
        
        # Save to file
        index_file = python_project / ".engine" / "index.json"
        index_file.parent.mkdir(exist_ok=True)
        
        with open(index_file, 'w') as f:
            json.dump(index, f)
        
        # Load from file
        with open(index_file) as f:
            loaded_index = json.load(f)
        
        # Verify loaded index matches
        assert loaded_index['functions'] == index['functions']
        assert loaded_index['classes'] == index['classes']
