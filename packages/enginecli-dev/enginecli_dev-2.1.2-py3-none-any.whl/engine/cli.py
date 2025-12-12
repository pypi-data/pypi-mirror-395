#!/usr/bin/env python3
"""
Engine CLI - AI-powered code generation.

This is a thin client that:
- Indexes code locally (fast)
- Assembles context locally
- Calls Engine API for generation (prompts hidden server-side)
"""
import sys
import json
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from engine.client.api import (
    get_api_client,
    APIError,
    AuthenticationError,
    UsageLimitError,
    FeatureNotAvailableError,
)
from engine.client.auth import (
    save_license,
    get_license_key,
    get_stored_license,
    clear_license,
    is_license_stored,
)
from engine.indexer.python import index_python_project
from engine.indexer.typescript import index_typescript_project
from engine.context.assembler import ContextAssembler, load_index
from engine.config import get_config, set_config, get_api_url

console = Console()

# Index file location
INDEX_DIR = Path(".engine")
INDEX_FILE = INDEX_DIR / "index.json"


def get_project_index() -> dict:
    """Load or create project index."""
    if not INDEX_FILE.exists():
        console.print("[yellow]No index found. Run 'engine index' first.[/yellow]")
        sys.exit(1)
    
    with open(INDEX_FILE) as f:
        return json.load(f)


def detect_language() -> str:
    """Detect primary project language."""
    cwd = Path.cwd()
    
    # Check for TypeScript/JavaScript
    if (cwd / "package.json").exists():
        return "typescript"
    if list(cwd.glob("*.tsx")) or list(cwd.glob("*.ts")):
        return "typescript"
    
    # Check for Python
    if (cwd / "requirements.txt").exists():
        return "python"
    if (cwd / "pyproject.toml").exists():
        return "python"
    if list(cwd.glob("*.py")):
        return "python"
    
    return "python"  # default


@click.group()
@click.version_option(version="2.1.2")
def cli():
    """Engine - AI-powered code generation."""
    pass


# ============================================================
# Index Commands
# ============================================================

@cli.command()
@click.option("--language", "-l", type=click.Choice(["python", "typescript", "auto"]), default="auto")
@click.option("--embed", "-e", is_flag=True, help="Build embeddings for RAG (semantic search)")
@click.option("--force", "-f", is_flag=True, help="Force full re-index (ignore cache)")
def index(language: str, embed: bool, force: bool):
    """Index the current project (incrementally by default)."""
    from engine.indexer.incremental import incremental_index
    
    cwd = Path.cwd()
    
    if language == "auto":
        language = detect_language()
    
    INDEX_DIR.mkdir(exist_ok=True)
    
    # Use incremental indexing
    if force:
        console.print(f"[blue]Full re-indexing {language} project...[/blue]")
    else:
        console.print(f"[blue]Indexing {language} project (incremental)...[/blue]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning files...", total=None)
        
        index_data, stats = incremental_index(cwd, language, force=force)
        
        progress.update(task, description="Index complete")
    
    # Print summary
    summary = []
    for key, items in index_data.items():
        if items:
            summary.append(f"{key}: {len(items)}")
    
    console.print(f"[green]✓ Indexed:[/green] {', '.join(summary)}")
    
    # Show incremental stats
    if stats["added"] or stats["modified"] or stats["deleted"]:
        changes = []
        if stats["added"]:
            changes.append(f"[green]+{stats['added']} new[/green]")
        if stats["modified"]:
            changes.append(f"[yellow]~{stats['modified']} modified[/yellow]")
        if stats["deleted"]:
            changes.append(f"[red]-{stats['deleted']} deleted[/red]")
        console.print(f"[dim]Changes: {', '.join(changes)} ({stats['unchanged']} unchanged)[/dim]")
    else:
        console.print(f"[dim]No changes detected ({stats['total']} files)[/dim]")
    
    console.print(f"[dim]Index saved to {INDEX_FILE}[/dim]")
    
    # Build embeddings if requested
    if embed:
        try:
            from engine.embeddings import RAGIndexer, HAS_EMBEDDINGS
            
            if not HAS_EMBEDDINGS:
                console.print("[yellow]⚠ sentence-transformers not installed.[/yellow]")
                console.print("[dim]Run: pip install sentence-transformers[/dim]")
                return
            
            console.print("\n[blue]Building embeddings for RAG...[/blue]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Generating embeddings...", total=None)
                
                indexer = RAGIndexer(cwd)
                count = indexer.build_from_index(index_data, show_progress=False)
            
            console.print(f"[green]✓ Embedded {count} items for semantic search[/green]")
            console.print("[dim]RAG mode enabled - context search will use semantic similarity[/dim]")
        
        except ImportError as e:
            console.print(f"[yellow]⚠ Missing dependencies: {e}[/yellow]")
            console.print("[dim]Run: pip install sentence-transformers numpy[/dim]")
        except Exception as e:
            console.print(f"[red]✗ Embedding failed: {e}[/red]")


@cli.command()
def status():
    """Show index and license status."""
    cwd = Path.cwd()
    
    # Index status
    if INDEX_FILE.exists():
        index_data = get_project_index()
        console.print("[green]✓ Index:[/green] Found")
        for key, items in index_data.items():
            if items:
                console.print(f"  • {key}: {len(items)}")
        
        # Check index state for last indexed time
        state_file = cwd / ".engine" / "index_state.json"
        if state_file.exists():
            try:
                with open(state_file) as f:
                    state = json.load(f)
                last_indexed = state.get("last_indexed", "")
                file_count = len(state.get("files", {}))
                if last_indexed:
                    console.print(f"  • [dim]Last indexed: {last_indexed[:19]} ({file_count} files tracked)[/dim]")
            except (json.JSONDecodeError, IOError):
                pass
        
        # Check RAG status
        vectors_db = cwd / ".engine" / "vectors.db"
        if vectors_db.exists():
            console.print("  • [green]RAG: Enabled[/green] (semantic search)")
        else:
            console.print("  • [dim]RAG: Not enabled (run 'engine index --embed')[/dim]")
    else:
        console.print("[yellow]✗ Index:[/yellow] Not found (run 'engine index')")
    
    console.print()
    
    # License status
    stored = get_stored_license()
    if stored:
        console.print(f"[green]✓ License:[/green] {stored.tier.upper()}")
        console.print(f"  • Key: {stored.license_key[:20]}...")
        
        # Get usage from API
        try:
            client = get_api_client()
            usage = client.get_usage()
            console.print(f"  • Daily: {usage.daily_used}/{usage.daily_limit} ({usage.daily_remaining} remaining)")
            console.print(f"  • Monthly: {usage.monthly_used}/{usage.monthly_limit} ({usage.monthly_remaining} remaining)")
        except APIError:
            console.print("  [dim]Could not fetch usage (offline?)[/dim]")
    else:
        console.print("[yellow]✗ License:[/yellow] Not activated")
        console.print("  Run 'engine license activate <key>' or 'engine license trial <email>'")


# ============================================================
# Generate Commands
# ============================================================

@cli.command()
@click.argument("task", required=False, default=None)
@click.option("--file", "-f", multiple=True, help="Files to focus on")
@click.option("--dry-run", is_flag=True, help="Show what would be generated without applying")
@click.option("--no-stream", is_flag=True, help="Disable streaming output")
def generate(task: str, file: tuple, dry_run: bool, no_stream: bool):
    """Generate code for a task. Run without arguments for guided suggestions."""
    # Check license
    if not is_license_stored():
        console.print("[red]No license found.[/red]")
        console.print("Run 'engine license activate <key>' or 'engine license trial <email>'")
        sys.exit(1)
    
    # If no task provided, show onboarding/suggestions
    if not task:
        task = _show_task_suggestions()
        if not task:
            return
    
    # Load index
    index_data = get_project_index()
    
    # Assemble context (uses RAG if available)
    console.print("[blue]Assembling context...[/blue]")
    assembler = ContextAssembler(index_data, project_dir=Path.cwd())
    context = assembler.assemble(task, file_hints=list(file) if file else None)
    relevant_files = assembler.get_relevant_files(task)
    
    if dry_run:
        console.print("\n[yellow]Dry run - context that would be sent:[/yellow]")
        console.print(Panel(context[:2000] + "..." if len(context) > 2000 else context))
        console.print(f"\n[dim]Relevant files: {', '.join(relevant_files[:5])}[/dim]")
        return
    
    try:
        client = get_api_client()
        
        if no_stream:
            # Non-streaming mode
            _generate_no_stream(client, task, context, relevant_files)
        else:
            # Streaming mode (default)
            _generate_with_stream(client, task, context, relevant_files)
    
    except AuthenticationError as e:
        console.print(f"[red]Authentication error:[/red] {e}")
        sys.exit(1)
    
    except UsageLimitError as e:
        _show_upgrade_prompt(e)
        sys.exit(1)
    
    except APIError as e:
        console.print(f"[red]API error:[/red] {e}")
        sys.exit(1)


def _show_task_suggestions() -> str:
    """Show interactive task suggestions for onboarding."""
    console.print("\n[bold cyan]🚀 What would you like to build?[/bold cyan]\n")
    
    # Detect project type for relevant suggestions
    cwd = Path.cwd()
    has_fastapi = any(cwd.glob("**/main.py")) or any(cwd.glob("**/app.py"))
    has_django = any(cwd.glob("**/manage.py"))
    has_react = (cwd / "package.json").exists()
    
    # Build suggestions based on project type
    suggestions = []
    
    if has_fastapi or has_django or (not has_react):
        suggestions.extend([
            ("1", "Add JWT authentication with login/register endpoints", "🔐"),
            ("2", "Create a new model with full CRUD API endpoints", "📦"),
            ("3", "Add Stripe payment webhook handler", "💳"),
            ("4", "Add rate limiting middleware", "🛡️"),
            ("5", "Create comprehensive tests for existing endpoints", "🧪"),
        ])
    
    if has_react:
        suggestions.extend([
            ("1", "Add user authentication with login/signup forms", "🔐"),
            ("2", "Create a data table component with sorting and filtering", "📊"),
            ("3", "Add a settings page with form validation", "⚙️"),
            ("4", "Create a dashboard with charts and metrics", "📈"),
            ("5", "Add dark mode toggle with theme context", "🌙"),
        ])
    
    if not suggestions:
        suggestions = [
            ("1", "Add user authentication", "🔐"),
            ("2", "Create a new model with CRUD operations", "📦"),
            ("3", "Add API endpoints for a new feature", "🔌"),
            ("4", "Create unit tests for existing code", "🧪"),
            ("5", "Add input validation and error handling", "✅"),
        ]
    
    # Display suggestions
    for num, desc, icon in suggestions:
        console.print(f"  [cyan]{num}[/cyan]  {icon}  {desc}")
    
    console.print(f"\n  [dim]c[/dim]     ✏️   Enter custom task")
    console.print(f"  [dim]q[/dim]     🚪  Quit\n")
    
    # Get user choice
    choice = click.prompt(
        "Choose an option",
        type=str,
        default="c"
    ).strip().lower()
    
    if choice == "q":
        console.print("[dim]Cancelled.[/dim]")
        return None
    
    if choice == "c":
        task = click.prompt("Describe what you want to build")
        return task
    
    # Find matching suggestion
    for num, desc, _ in suggestions:
        if choice == num:
            console.print(f"\n[green]Selected:[/green] {desc}\n")
            return desc
    
    # Treat as custom input if no match
    return choice


def _show_upgrade_prompt(e):
    """Show a helpful upgrade prompt when usage limit is hit."""
    console.print("\n[bold yellow]⚠️  Generation limit reached[/bold yellow]\n")
    
    # Show current usage
    console.print(f"  {e.limit_name}: {e.current}/{e.limit} used\n")
    
    # Show upgrade benefits
    console.print("[bold]Upgrade to Engine Pro ($39/mo):[/bold]")
    console.print("  ✓ 200 generations per month")
    console.print("  ✓ Instant rollback safety net")
    console.print("  ✓ Full tool-use verification")
    console.print("  ✓ Priority support\n")
    
    console.print("[bold]Or Engine Team ($119/mo):[/bold]")
    console.print("  ✓ 500 generations per month")
    console.print("  ✓ Shared pattern library")
    console.print("  ✓ Team analytics dashboard")
    console.print("  ✓ Everything in Pro\n")
    
    console.print(f"[blue]→ Upgrade now:[/blue] {e.upgrade_url}")
    console.print("[dim]  Or run: engine upgrade[/dim]\n")


def _show_usage_meter(client):
    """Show usage meter after generation."""
    try:
        usage = client.get_usage()
        
        # Get stored license for tier info
        stored = get_stored_license()
        tier = stored.tier if stored else "trial"
        
        if tier == "trial":
            # Trial: show X/5 with emphasis
            remaining = usage.monthly_limit - usage.monthly_used
            if remaining <= 2:
                console.print(f"[yellow]📊 Trial: {usage.monthly_used}/{usage.monthly_limit} generations used ({remaining} remaining)[/yellow]")
                if remaining == 0:
                    console.print("[dim]   Run 'engine upgrade' to continue generating[/dim]")
            else:
                console.print(f"[dim]📊 Trial: {usage.monthly_used}/{usage.monthly_limit} generations ({remaining} remaining)[/dim]")
        else:
            # Paid tier: show monthly usage
            pct = (usage.monthly_used / usage.monthly_limit * 100) if usage.monthly_limit > 0 else 0
            if pct >= 80:
                console.print(f"[yellow]📊 Usage: {usage.monthly_used}/{usage.monthly_limit} this month ({pct:.0f}%)[/yellow]")
            else:
                console.print(f"[dim]📊 Usage: {usage.monthly_used}/{usage.monthly_limit} this month[/dim]")
    except Exception:
        # Silently skip if can't get usage
        pass
    
    console.print()  # Add spacing


def _generate_with_stream(client, task: str, context: str, relevant_files: list[str]):
    """Generate code with streaming output."""
    from rich.live import Live
    from rich.text import Text
    
    console.print("[blue]Generating code (streaming)...[/blue]\n")
    
    full_content = ""
    input_tokens = 0
    output_tokens = 0
    files_generated = []
    tool_calls_made = 0
    
    # Create a Live display for streaming output
    output_text = Text()
    
    with Live(output_text, console=console, refresh_per_second=15) as live:
        try:
            for event in client.generate_stream(
                task=task,
                context=context,
                file_paths=relevant_files,
                language=detect_language(),
            ):
                if event["type"] == "token":
                    output_text.append(event["content"])
                    full_content += event["content"]
                
                elif event["type"] == "tool_use":
                    tool_calls_made += 1
                    # Show tool usage inline
                    tool_name = event["tool"]
                    tool_input = event.get("input", {})
                    output_text.append(f"\n[🔧 {tool_name}]", style="dim cyan")
                
                elif event["type"] == "tool_result":
                    # Show tool result briefly
                    result = event.get("result", "")
                    # Truncate long results
                    if len(result) > 100:
                        result = result[:100] + "..."
                    output_text.append(f" → {result}\n", style="dim green")
                
                elif event["type"] == "done":
                    full_content = event["content"]
                    input_tokens = event["input_tokens"]
                    output_tokens = event["output_tokens"]
                    files_generated = event.get("files_generated", [])
                
                elif event["type"] == "error":
                    console.print(f"\n[red]Error:[/red] {event['message']}")
                    return
        
        except Exception as e:
            console.print(f"\n[red]Stream error:[/red] {e}")
            return
    
    # Display completion stats
    stats_line = f"\n\n[green]✓ Generated {len(files_generated)} file(s)[/green]"
    if tool_calls_made > 0:
        stats_line += f" [dim](verified with {tool_calls_made} tool calls)[/dim]"
    console.print(stats_line)
    console.print(f"[dim]Tokens: {input_tokens} in / {output_tokens} out[/dim]")
    
    # Show usage meter
    _show_usage_meter(client)
    
    # Apply changes
    if files_generated:
        # Offer preview option
        choice = click.prompt(
            "Apply changes?",
            type=click.Choice(['y', 'n', 'p'], case_sensitive=False),
            default='y',
            show_choices=True,
            prompt_suffix=" (y=yes, n=no, p=preview): "
        )
        
        if choice.lower() == 'p':
            _preview_changes(full_content)
            if click.confirm("Apply these changes?"):
                _apply_changes(full_content, task=task)
                console.print("[green]✓ Changes applied[/green]")
            else:
                console.print("[yellow]Changes not applied[/yellow]")
        elif choice.lower() == 'y':
            _apply_changes(full_content, task=task)
            console.print("[green]✓ Changes applied[/green]")
        else:
            console.print("[yellow]Changes not applied[/yellow]")


def _generate_no_stream(client, task: str, context: str, relevant_files: list[str]):
    """Generate code without streaming (original behavior)."""
    console.print("[blue]Generating code...[/blue]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        prog_task = progress.add_task("Calling Engine API...", total=None)
        
        response = client.generate(
            task=task,
            context=context,
            file_paths=relevant_files,
            language=detect_language(),
        )
    
    # Display result
    console.print(f"\n[green]✓ Generated {len(response.files_generated)} file(s)[/green]")
    console.print(f"[dim]Tokens: {response.input_tokens} in / {response.output_tokens} out[/dim]")
    
    # Show usage meter
    _show_usage_meter(client)
    
    # Show generated code
    console.print(Panel(
        Syntax(response.content, "python", theme="monokai"),
        title="Generated Code",
    ))
    
    # Apply changes
    if response.files_generated:
        choice = click.prompt(
            "Apply changes?",
            type=click.Choice(['y', 'n', 'p'], case_sensitive=False),
            default='y',
            show_choices=True,
            prompt_suffix=" (y=yes, n=no, p=preview): "
        )
        
        if choice.lower() == 'p':
            _preview_changes(response.content)
            if click.confirm("Apply these changes?"):
                _apply_changes(response.content, task=task)
                console.print("[green]✓ Changes applied[/green]")
            else:
                console.print("[yellow]Changes not applied[/yellow]")
        elif choice.lower() == 'y':
            _apply_changes(response.content, task=task)
            console.print("[green]✓ Changes applied[/green]")
        else:
            console.print("[yellow]Changes not applied[/yellow]")


@cli.command()
@click.argument("feature")
@click.option("--max-tasks", "-n", default=10, help="Maximum number of tasks")
@click.option("--execute", "-e", is_flag=True, help="Execute the plan immediately")
def plan(feature: str, max_tasks: int, execute: bool):
    """Create a multi-task plan for a feature."""
    if not is_license_stored():
        console.print("[red]No license found.[/red]")
        sys.exit(1)
    
    index_data = get_project_index()
    assembler = ContextAssembler(index_data)
    context = assembler.assemble(feature)
    
    console.print("[blue]Creating plan...[/blue]")
    
    try:
        client = get_api_client()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            prog_task = progress.add_task("Planning...", total=None)
            response = client.plan(feature, context, max_tasks)
        
        # Display plan
        console.print(f"\n[green]✓ Created {len(response.tasks)} tasks[/green]\n")
        
        table = Table(title="Implementation Plan")
        table.add_column("#", style="cyan")
        table.add_column("Task", style="white")
        table.add_column("Files", style="dim")
        
        for task in response.tasks:
            files = ", ".join(task.files[:3])
            if len(task.files) > 3:
                files += f" +{len(task.files) - 3}"
            table.add_row(str(task.id), task.title, files)
        
        console.print(table)
        
        if execute:
            if click.confirm("\nExecute this plan?"):
                _execute_plan(response.tasks, context)
    
    except FeatureNotAvailableError as e:
        console.print(f"[red]Feature not available:[/red] {e}")
        console.print(f"[blue]Upgrade at:[/blue] {e.upgrade_url}")
        sys.exit(1)
    
    except UsageLimitError as e:
        console.print(f"[red]Usage limit reached:[/red] {e.limit_name}")
        console.print(f"[blue]Upgrade at:[/blue] {e.upgrade_url}")
        sys.exit(1)
    
    except APIError as e:
        console.print(f"[red]API error:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.option("--context", "-c", help="Additional context")
def chat(context: str):
    """Chat about your codebase."""
    if not is_license_stored():
        console.print("[red]No license found.[/red]")
        sys.exit(1)
    
    index_data = get_project_index()
    assembler = ContextAssembler(index_data)
    
    history = []
    
    console.print("[blue]Engine Chat[/blue] (type 'exit' to quit)\n")
    
    client = get_api_client()
    
    while True:
        try:
            message = console.input("[green]You:[/green] ")
        except EOFError:
            break
        
        if message.lower() in ["exit", "quit", "q"]:
            break
        
        if not message.strip():
            continue
        
        # Assemble context for this message
        ctx = assembler.assemble(message)
        if context:
            ctx = f"{context}\n\n{ctx}"
        
        try:
            response = client.chat(message, ctx, history)
            
            console.print(f"\n[blue]Engine:[/blue] {response.content}\n")
            
            # Update history
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": response.content})
            
            # Keep history manageable
            if len(history) > 20:
                history = history[-20:]
        
        except APIError as e:
            console.print(f"[red]Error:[/red] {e}\n")


# ============================================================
# License Commands
# ============================================================

@cli.group()
def license():
    """Manage your license."""
    pass


@license.command()
@click.argument("key")
def activate(key: str):
    """Activate a license key."""
    console.print("[blue]Activating license...[/blue]")
    
    try:
        client = get_api_client()
        # Temporarily use the provided key
        client.license_key = key
        
        info = client.activate_license(key)
        
        # Save locally
        save_license(info.license_key, info.tier, info.limits)
        
        console.print(f"[green]✓ License activated![/green]")
        console.print(f"  Tier: {info.tier.upper()}")
        console.print(f"  Status: {info.status}")
        
        if info.limits:
            console.print(f"  Daily limit: {info.limits.get('generations_per_day', 'N/A')}")
            console.print(f"  Monthly limit: {info.limits.get('generations_per_month', 'N/A')}")
    
    except APIError as e:
        console.print(f"[red]Activation failed:[/red] {e}")
        sys.exit(1)


@license.command()
@click.argument("email")
def trial(email: str):
    """Start a free trial with email verification."""
    console.print("[blue]Requesting verification code...[/blue]")
    
    try:
        client = get_api_client()
        
        # Step 1: Request verification code
        result = client.request_trial(email)
        
        console.print(f"[green]✓ Verification code sent to {email}[/green]")
        console.print("[dim]Check your inbox (and spam folder)[/dim]\n")
        
        # Step 2: Prompt for code
        code = click.prompt("Enter the 6-digit code", type=str)
        
        console.print("[blue]Verifying code...[/blue]")
        
        # Step 3: Verify and create trial
        info = client.verify_trial(email, code.strip())
        
        # Save locally
        save_license(info.license_key, info.tier, info.limits)
        
        console.print(f"\n[green]✓ Trial activated for {email}![/green]")
        console.print(f"\nYou now have [bold]5 generations[/bold] to try Pro features:")
        console.print("  • engine plan - Multi-task planning")
        console.print("  • Extended context limits")
        console.print("  • Chat history")
        console.print(f"\n[dim]License key: {info.license_key}[/dim]")
        console.print("\n[blue]Upgrade at:[/blue] https://enginecli.dev/pricing")
    
    except APIError as e:
        console.print(f"[red]Trial creation failed:[/red] {e}")
        sys.exit(1)


@license.command(name="status")
def license_status():
    """Show license status."""
    stored = get_stored_license()
    
    if not stored:
        console.print("[yellow]No license activated.[/yellow]")
        console.print("Run 'engine license activate <key>' or 'engine license trial <email>'")
        return
    
    console.print(f"[green]License:[/green] {stored.tier.upper()}")
    console.print(f"Key: {stored.license_key}")
    console.print(f"Activated: {stored.activated_at}")
    
    # Get live status from API
    try:
        client = get_api_client()
        info = client.get_license_status()
        usage = client.get_usage()
        
        console.print(f"\n[blue]Usage:[/blue]")
        console.print(f"  Daily: {usage.daily_used}/{usage.daily_limit}")
        console.print(f"  Monthly: {usage.monthly_used}/{usage.monthly_limit}")
    except APIError:
        console.print("\n[dim]Could not fetch live status[/dim]")


@license.command()
def deactivate():
    """Deactivate license (for machine swap)."""
    if not is_license_stored():
        console.print("[yellow]No license to deactivate.[/yellow]")
        return
    
    if click.confirm("Deactivate license on this machine?"):
        try:
            client = get_api_client()
            client.deactivate_license()
            clear_license()
            console.print("[green]✓ License deactivated.[/green]")
            console.print("You can now activate on another machine.")
        except APIError as e:
            console.print(f"[red]Deactivation failed:[/red] {e}")


# ============================================================
# Upgrade Command
# ============================================================

@cli.command()
@click.option("--tier", "-t", type=click.Choice(["pro", "team"]), default=None,
              help="Tier to upgrade to")
def upgrade(tier: str):
    """Upgrade your Engine subscription."""
    import webbrowser
    
    base_url = get_api_url().replace("/v1", "")
    
    if not tier:
        console.print("\n[bold cyan]🚀 Upgrade Engine[/bold cyan]\n")
        console.print("[bold]Pro[/bold] - $39/month")
        console.print("  ✓ 200 generations/month")
        console.print("  ✓ Instant rollback")
        console.print("  ✓ Full tool-use verification")
        console.print("  ✓ Priority support\n")
        
        console.print("[bold]Team[/bold] - $119/month")
        console.print("  ✓ 500 generations/month")
        console.print("  ✓ Shared pattern library")
        console.print("  ✓ Team analytics dashboard")
        console.print("  ✓ Everything in Pro\n")
        
        tier = click.prompt(
            "Which tier",
            type=click.Choice(["pro", "team"]),
            default="pro"
        )
    
    # Open checkout page
    checkout_url = f"{base_url}/#pricing"
    console.print(f"\n[blue]Opening checkout...[/blue]")
    console.print(f"[dim]{checkout_url}[/dim]\n")
    
    try:
        webbrowser.open(checkout_url)
        console.print("[green]✓ Checkout page opened in browser[/green]")
        console.print("[dim]Complete payment to activate your subscription.[/dim]")
    except Exception:
        console.print(f"[yellow]Could not open browser. Visit:[/yellow]")
        console.print(f"  {checkout_url}")


# ============================================================
# Analytics Commands
# ============================================================

@cli.group()
def analytics():
    """View usage analytics and ROI reports."""
    pass


@analytics.command(name="stats")
@click.option("--period", "-p", default="month", 
              type=click.Choice(["today", "week", "month", "quarter", "year", "all"]),
              help="Time period")
def analytics_stats(period: str):
    """Show usage statistics."""
    if not is_license_stored():
        console.print("[red]No license found.[/red]")
        sys.exit(1)
    
    try:
        client = get_api_client()
        stats = client.get_analytics_stats(period)
        
        console.print(f"\n[bold blue]Usage Statistics ({period})[/bold blue]")
        console.print("─" * 40)
        
        # Generations
        console.print(f"\n[green]Generations:[/green]")
        console.print(f"  Total: {stats['total_generations']}")
        console.print(f"  Successful: {stats['successful_generations']}")
        console.print(f"  Failed: {stats['failed_generations']}")
        console.print(f"  Success Rate: {stats['performance']['success_rate']}%")
        
        # Tokens
        console.print(f"\n[green]Tokens:[/green]")
        console.print(f"  Input: {stats['tokens']['input']:,}")
        console.print(f"  Output: {stats['tokens']['output']:,}")
        console.print(f"  Total: {stats['tokens']['total']:,}")
        
        # Cost
        console.print(f"\n[green]Cost:[/green]")
        console.print(f"  Estimated: ${stats['cost']['estimated_usd']:.4f}")
        
        # Value
        console.print(f"\n[green]Value:[/green]")
        console.print(f"  Time Saved: {stats['time_saved']['hours']} hours")
        console.print(f"  Value Saved: ${stats['value']['estimated_usd']:.2f}")
        console.print(f"  ROI: {stats['value']['roi_multiplier']}x")
        
        # Performance
        console.print(f"\n[green]Performance:[/green]")
        console.print(f"  Avg Duration: {stats['performance']['average_duration_ms']}ms")
        
    except APIError as e:
        console.print(f"[red]Failed to fetch analytics:[/red] {e}")
        sys.exit(1)


@analytics.command(name="roi")
@click.option("--period", "-p", default="month",
              type=click.Choice(["today", "week", "month", "quarter", "year"]),
              help="Time period")
@click.option("--rate", "-r", default=75.0, help="Developer hourly rate (USD)")
def analytics_roi(period: str, rate: float):
    """Show ROI report for management."""
    if not is_license_stored():
        console.print("[red]No license found.[/red]")
        sys.exit(1)
    
    try:
        client = get_api_client()
        roi = client.get_analytics_roi(period, rate)
        
        console.print(f"\n[bold blue]ROI Report ({period})[/bold blue]")
        console.print("─" * 50)
        
        # Usage
        console.print(f"\n[green]Usage Summary:[/green]")
        console.print(f"  Successful Generations: {roi['usage']['successful_generations']}")
        console.print(f"  Success Rate: {roi['usage']['success_rate_percent']}%")
        
        # Costs
        console.print(f"\n[green]Costs:[/green]")
        console.print(f"  API Usage: ${roi['costs']['api_usage_usd']:.2f}")
        console.print(f"  Subscription: ${roi['costs']['subscription_usd']:.2f}")
        console.print(f"  [bold]Total: ${roi['costs']['total_cost_usd']:.2f}[/bold]")
        
        # Value
        console.print(f"\n[green]Value Generated:[/green]")
        console.print(f"  Time Saved: {roi['value']['time_saved_hours']} hours")
        console.print(f"  Value @ ${rate}/hr: ${roi['value']['value_saved_usd']:.2f}")
        console.print(f"  [bold]Net Value: ${roi['value']['net_value_usd']:.2f}[/bold]")
        
        # ROI Summary
        console.print(f"\n[bold green]ROI:[/bold green]")
        console.print(f"  Multiplier: {roi['roi']['multiplier']}x")
        console.print(f"  Percentage: {roi['roi']['percentage']}%")
        console.print(f"\n  [dim]{roi['roi']['summary']}[/dim]")
        
    except APIError as e:
        console.print(f"[red]Failed to fetch ROI:[/red] {e}")
        sys.exit(1)


@analytics.command(name="activity")
@click.option("--limit", "-n", default=10, help="Number of recent activities")
def analytics_activity(limit: int):
    """Show recent generation activity."""
    if not is_license_stored():
        console.print("[red]No license found.[/red]")
        sys.exit(1)
    
    try:
        client = get_api_client()
        data = client.get_analytics_activity(limit)
        
        console.print(f"\n[bold blue]Recent Activity[/bold blue]")
        console.print("─" * 60)
        
        for item in data["activity"]:
            status = "[green]✓[/green]" if item["success"] else "[red]✗[/red]"
            tokens = f"{item['tokens']['input']}→{item['tokens']['output']}"
            duration = f"{item['duration_ms']}ms"
            cost = f"${item['estimated_cost_usd']:.4f}"
            time = item["created_at"][:19].replace("T", " ")
            
            console.print(f"  {status} {item['request_type']:<15} {tokens:<12} {duration:<8} {cost:<10} {time}")
        
        console.print(f"\n[dim]Showing {data['count']} most recent activities[/dim]")
        
    except APIError as e:
        console.print(f"[red]Failed to fetch activity:[/red] {e}")
        sys.exit(1)


@analytics.command(name="team")
@click.argument("domain")
@click.option("--period", "-p", default="month", help="Time period")
def analytics_team(domain: str, period: str):
    """Show team usage statistics (Team/Enterprise only)."""
    if not is_license_stored():
        console.print("[red]No license found.[/red]")
        sys.exit(1)
    
    try:
        client = get_api_client()
        data = client.get_analytics_team(domain, period)
        
        if data["user_count"] == 0:
            console.print(f"[yellow]No users found for domain: {domain}[/yellow]")
            return
        
        console.print(f"\n[bold blue]Team Usage: {domain} ({period})[/bold blue]")
        console.print("─" * 60)
        
        # Team totals
        totals = data["totals"]
        console.print(f"\n[green]Team Totals:[/green]")
        console.print(f"  Users: {data['user_count']}")
        console.print(f"  Generations: {totals['generations']}")
        console.print(f"  Tokens: {totals['tokens']['total']:,}")
        console.print(f"  Cost: ${totals['cost']['estimated_usd']:.2f}")
        console.print(f"  Time Saved: {totals['time_saved']['hours']} hours")
        console.print(f"  Value: ${totals['value']['estimated_usd']:.2f}")
        console.print(f"  ROI: {totals['value']['roi_multiplier']}x")
        
        # Per-user breakdown
        console.print(f"\n[green]Per-User Breakdown:[/green]")
        for user in data["users"]:
            console.print(f"  {user['email']:<30} {user['total_generations']:>5} gens  ${user['estimated_cost_usd']:.2f}  {user['estimated_time_saved_hours']:.1f}h saved")
        
    except FeatureNotAvailableError:
        console.print("[yellow]Team analytics requires Team or Enterprise tier.[/yellow]")
        console.print("Upgrade at: https://enginecli.dev/pricing")
        sys.exit(1)
    except APIError as e:
        console.print(f"[red]Failed to fetch team analytics:[/red] {e}")
        sys.exit(1)


# ============================================================
# Pattern Commands
# ============================================================

@cli.group()
def patterns():
    """Manage code patterns for consistent generation."""
    pass


@patterns.command(name="list")
@click.option("--language", "-l", default=None, help="Filter by language")
def patterns_list(language: str):
    """List available patterns."""
    from engine.patterns import PatternManager, get_builtin_patterns
    
    cwd = Path.cwd()
    manager = PatternManager(cwd)
    
    # Get all patterns
    all_patterns = manager.get_all_patterns(language)
    builtin = get_builtin_patterns()
    
    if not all_patterns and not builtin:
        console.print("[yellow]No patterns found.[/yellow]")
        console.print("Run 'engine patterns add' to create a local pattern")
        return
    
    # Show built-in patterns
    console.print("\n[bold blue]Built-in Patterns[/bold blue]")
    console.print("─" * 50)
    for p in builtin:
        if language is None or p.language == language:
            tags = ", ".join(p.tags[:3]) if p.tags else ""
            console.print(f"  [{p.language}] [green]{p.name}[/green] - {p.description[:50]}...")
            if tags:
                console.print(f"         Tags: {tags}")
    
    # Show local/team patterns
    if all_patterns:
        console.print("\n[bold blue]Local/Team Patterns[/bold blue]")
        console.print("─" * 50)
        for p in all_patterns:
            tags = ", ".join(p.tags[:3]) if p.tags else ""
            console.print(f"  [{p.language}] [green]{p.name}[/green] ({p.id})")
            console.print(f"         {p.description[:60]}...")
            if tags:
                console.print(f"         Tags: {tags}")


@patterns.command(name="show")
@click.argument("pattern_id")
def patterns_show(pattern_id: str):
    """Show pattern details."""
    from engine.patterns import PatternManager, get_builtin_pattern
    
    cwd = Path.cwd()
    manager = PatternManager(cwd)
    
    # Check built-in first
    pattern = get_builtin_pattern(pattern_id)
    
    # Check local patterns
    if not pattern:
        library = manager.load_library()
        pattern = library.get_pattern(pattern_id)
    
    if not pattern:
        local_patterns = manager.load_local_patterns()
        for p in local_patterns:
            if p.id == pattern_id:
                pattern = p
                break
    
    if not pattern:
        console.print(f"[red]Pattern not found: {pattern_id}[/red]")
        sys.exit(1)
    
    # Display pattern
    console.print(f"\n[bold blue]{pattern.name}[/bold blue]")
    console.print("─" * 50)
    console.print(f"ID: {pattern.id}")
    console.print(f"Language: {pattern.language}")
    console.print(f"Description: {pattern.description}")
    
    if pattern.tags:
        console.print(f"Tags: {', '.join(pattern.tags)}")
    
    console.print(f"\n[green]Rules:[/green]")
    for rule in pattern.rules:
        console.print(f"  [{rule.severity.upper()}] {rule.description}")
    
    console.print(f"\n[green]Template:[/green]")
    from rich.syntax import Syntax
    syntax = Syntax(pattern.template, pattern.language, theme="monokai", line_numbers=True)
    console.print(syntax)


@patterns.command(name="add")
@click.option("--name", "-n", prompt=True, help="Pattern name")
@click.option("--language", "-l", prompt=True, type=click.Choice(["python", "typescript"]))
@click.option("--description", "-d", prompt=True, help="Pattern description")
@click.option("--file", "-f", type=click.Path(exists=True), help="Template file")
def patterns_add(name: str, language: str, description: str, file: str):
    """Add a local pattern."""
    from engine.patterns import PatternManager, Pattern, PatternRule
    import uuid
    
    cwd = Path.cwd()
    manager = PatternManager(cwd)
    
    # Read template from file or prompt
    if file:
        template = Path(file).read_text()
    else:
        console.print("\nEnter template code (end with Ctrl+D or empty line):")
        lines = []
        try:
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
        except EOFError:
            pass
        template = "\n".join(lines)
    
    if not template.strip():
        console.print("[red]Template cannot be empty[/red]")
        sys.exit(1)
    
    # Create pattern
    pattern = Pattern(
        id=f"local_{uuid.uuid4().hex[:8]}",
        name=name,
        description=description,
        language=language,
        template=template,
        rules=[
            PatternRule("Follow this pattern's structure", "required"),
        ],
        tags=[language, "local"],
    )
    
    manager.save_local_pattern(pattern)
    console.print(f"[green]✓ Pattern saved: {pattern.id}[/green]")
    console.print(f"This pattern will be used during code generation.")


@patterns.command(name="remove")
@click.argument("pattern_id")
def patterns_remove(pattern_id: str):
    """Remove a local pattern."""
    from engine.patterns import PatternManager
    
    cwd = Path.cwd()
    manager = PatternManager(cwd)
    
    if manager.delete_local_pattern(pattern_id):
        console.print(f"[green]✓ Pattern removed: {pattern_id}[/green]")
    else:
        console.print(f"[red]Pattern not found: {pattern_id}[/red]")
        sys.exit(1)


@patterns.command(name="sync")
def patterns_sync():
    """Sync patterns from team library."""
    if not is_license_stored():
        console.print("[red]No license found. Run 'engine license activate' first.[/red]")
        sys.exit(1)
    
    stored = get_stored_license()
    if stored.tier not in ("team", "enterprise"):
        console.print("[yellow]Team pattern sync requires Team or Enterprise tier.[/yellow]")
        console.print("Local patterns will still be used during generation.")
        return
    
    console.print("[blue]Syncing team patterns...[/blue]")
    
    try:
        from engine.patterns import PatternManager, PatternLibrary, Pattern, PatternRule
        
        client = get_api_client()
        
        # Fetch from API (this would need an API endpoint)
        # For now, show a message
        console.print("[dim]Team pattern sync coming soon![/dim]")
        console.print("Local patterns are available immediately.")
        
    except APIError as e:
        console.print(f"[red]Sync failed:[/red] {e}")
        sys.exit(1)


# ============================================================
# Config Commands
# ============================================================

@cli.group()
def config():
    """Manage configuration."""
    pass


@config.command(name="set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str):
    """Set a configuration value."""
    set_config(key, value)
    console.print(f"[green]✓ Set {key} = {value}[/green]")


@config.command(name="get")
@click.argument("key")
def config_get(key: str):
    """Get a configuration value."""
    from engine.config import get_config_value
    value = get_config_value(key)
    if value is not None:
        console.print(f"{key} = {value}")
    else:
        console.print(f"[yellow]{key} not set[/yellow]")


@config.command(name="list")
def config_list():
    """List all configuration."""
    from engine.config import get_config
    cfg = get_config()
    for key, value in cfg.items():
        console.print(f"{key} = {value}")


# ============================================================
# Helper Functions
# ============================================================

def _preview_changes(content: str):
    """Preview file changes with diffs before applying."""
    import difflib
    
    changes = _extract_file_changes(content)
    
    if not changes:
        console.print("[yellow]No changes to preview.[/yellow]")
        return
    
    console.print("\n[bold cyan]═══ PREVIEW ═══[/bold cyan]\n")
    
    for file_path, new_content in changes:
        path = Path(file_path)
        
        # Delete marker
        if new_content == '__DELETE_FILE__':
            console.print(f"[red]─── DELETE: {file_path} ───[/red]")
            continue
        
        # New file
        if not path.exists():
            console.print(f"[cyan]─── NEW: {file_path} ───[/cyan]")
            # Show first 20 lines
            lines = new_content.splitlines()[:20]
            for line in lines:
                console.print(f"[green]+ {line}[/green]")
            if len(new_content.splitlines()) > 20:
                console.print(f"[dim]... ({len(new_content.splitlines()) - 20} more lines)[/dim]")
            console.print()
            continue
        
        # Modified file - show diff
        console.print(f"[yellow]─── MODIFIED: {file_path} ───[/yellow]")
        old_content = path.read_text()
        
        diff = difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}",
            lineterm=""
        )
        
        diff_lines = list(diff)
        if not diff_lines:
            console.print("[dim]No changes[/dim]")
        else:
            # Show max 30 diff lines
            for i, line in enumerate(diff_lines[:30]):
                line = line.rstrip('\n')
                if line.startswith('+') and not line.startswith('+++'):
                    console.print(f"[green]{line}[/green]")
                elif line.startswith('-') and not line.startswith('---'):
                    console.print(f"[red]{line}[/red]")
                elif line.startswith('@@'):
                    console.print(f"[cyan]{line}[/cyan]")
                else:
                    console.print(f"[dim]{line}[/dim]")
            
            if len(diff_lines) > 30:
                console.print(f"[dim]... ({len(diff_lines) - 30} more lines)[/dim]")
        
        console.print()
    
    console.print("[bold cyan]═══ END PREVIEW ═══[/bold cyan]\n")


def _apply_changes(content: str, task: str = "code generation"):
    """
    Apply generated code to files.
    
    Creates a snapshot before applying changes for rollback safety.
    Includes: preview, auto-install deps, migration hints, git commit.
    """
    import re
    import subprocess
    import difflib
    from engine.rollback import RollbackManager
    
    # Extract all file changes first
    changes = _extract_file_changes(content)
    
    if not changes:
        console.print("[yellow]No file changes found in output.[/yellow]")
        return
    
    # Create snapshot before applying
    file_paths = [path for path, _ in changes]
    manager = RollbackManager(Path.cwd())
    snapshot = manager.create_snapshot(file_paths, task)
    console.print(f"[dim]Snapshot created: {snapshot.id}[/dim]")
    
    # Track changes for post-apply actions
    new_deps = []
    schema_changed = False
    modified_files = []
    new_files = []
    
    # Apply changes
    for file_path, file_content in changes:
        path = Path(file_path)
        
        # Check for delete marker
        if file_content == '__DELETE_FILE__':
            if path.exists():
                path.unlink()
                console.print(f"  [red]✗ Deleted[/red] {file_path}")
            continue
        
        # Track if new or modified
        is_new = not path.exists()
        if is_new:
            new_files.append(file_path)
        else:
            modified_files.append(file_path)
        
        # Write file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(file_content)
        
        status = "[cyan]+ New[/cyan]" if is_new else "[green]✓[/green]"
        console.print(f"  {status} {file_path}")
        
        # Check for new dependencies
        if file_path == "requirements.txt":
            new_deps = _detect_new_dependencies(file_content)
        elif file_path == "pyproject.toml" and "[project]" in file_content:
            new_deps = _detect_new_dependencies_pyproject(file_content)
        
        # Check for schema changes (model files)
        if "models" in file_path.lower() and not is_new:
            schema_changed = True
    
    console.print(f"\n[dim]Run 'engine rollback last' to undo these changes[/dim]")
    
    # Post-apply: Migration hints
    if schema_changed:
        console.print("\n[yellow]⚠️  Schema changes detected![/yellow]")
        console.print("[dim]If using SQLite, you may need to:[/dim]")
        console.print("  [cyan]rm *.db[/cyan]  (delete and recreate)")
        console.print("[dim]Or if using Alembic:[/dim]")
        console.print("  [cyan]alembic revision --autogenerate -m 'schema update'[/cyan]")
        console.print("  [cyan]alembic upgrade head[/cyan]")
    
    # Post-apply: Auto-install dependencies
    if new_deps:
        console.print(f"\n[yellow]📦 New dependencies detected:[/yellow] {', '.join(new_deps)}")
        if click.confirm("Install now?", default=True):
            _install_dependencies(new_deps)
    
    # Post-apply: Git commit
    if _is_git_repo():
        if click.confirm("\n[dim]Commit changes to git?[/dim]", default=False):
            _git_commit(task, file_paths)


def _detect_new_dependencies(requirements_content: str) -> list[str]:
    """Detect newly added dependencies in requirements.txt."""
    req_path = Path("requirements.txt")
    if not req_path.exists():
        return []
    
    try:
        old_deps = set()
        for line in req_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                # Extract package name (before ==, >=, etc.)
                pkg = line.split("==")[0].split(">=")[0].split("<=")[0].split("[")[0].strip()
                old_deps.add(pkg.lower())
        
        new_deps = []
        for line in requirements_content.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                pkg = line.split("==")[0].split(">=")[0].split("<=")[0].split("[")[0].strip()
                if pkg.lower() not in old_deps:
                    new_deps.append(pkg)
        
        return new_deps
    except Exception:
        return []


def _detect_new_dependencies_pyproject(content: str) -> list[str]:
    """Detect newly added dependencies in pyproject.toml."""
    # Simplified detection - just look for new packages
    return []  # TODO: Implement TOML parsing


def _install_dependencies(deps: list[str]):
    """Install dependencies using pip."""
    import subprocess
    
    console.print(f"[dim]Installing: {' '.join(deps)}[/dim]")
    try:
        result = subprocess.run(
            ["pip", "install"] + deps,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            console.print("[green]✓ Dependencies installed[/green]")
        else:
            console.print(f"[red]Installation failed:[/red] {result.stderr}")
    except Exception as e:
        console.print(f"[red]Failed to install:[/red] {e}")


def _is_git_repo() -> bool:
    """Check if current directory is a git repository."""
    return (Path.cwd() / ".git").exists()


def _git_commit(task: str, files: list[str]):
    """Commit changes to git."""
    import subprocess
    
    try:
        # Add files
        subprocess.run(["git", "add"] + files, capture_output=True)
        
        # Commit with task as message
        commit_msg = f"engine: {task[:50]}" if len(task) > 50 else f"engine: {task}"
        result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            console.print(f"[green]✓ Committed:[/green] {commit_msg}")
        else:
            console.print(f"[yellow]Git commit skipped:[/yellow] {result.stderr.strip()}")
    except Exception as e:
        console.print(f"[red]Git error:[/red] {e}")


def _extract_file_changes(content: str) -> list[tuple[str, str]]:
    """
    Extract file changes from generated content.
    Returns list of (path, content) tuples.
    """
    import re
    
    changes = []
    
    # Normalize line endings
    content = content.replace('\r\n', '\n')
    
    # Pattern: <<<<< FILE: path >>>>> ... <<<<< END FILE >>>>>
    # More flexible - doesn't require specific whitespace/newlines
    pattern = r'<{5}\s*FILE:\s*([^>]+?)\s*>{5}(.*?)<{5}\s*END\s*FILE\s*>{5}'
    matches = re.findall(pattern, content, re.DOTALL)
    
    if matches:
        for file_path, file_content in matches:
            # Clean up the content
            file_content = file_content.strip()
            file_path = file_path.strip()
            changes.append((file_path, file_content))
        return changes
    
    # Fall back to legacy format: FILE: path followed by code block
    legacy_pattern = r'^FILE:\s*(.+)$'
    parts = re.split(legacy_pattern, content, flags=re.MULTILINE)
    
    i = 1
    while i < len(parts):
        file_path = parts[i].strip()
        if i + 1 < len(parts):
            file_content = parts[i + 1].strip()
            
            # Extract from code blocks
            code_match = re.search(r'```\w*\n(.*?)```', file_content, re.DOTALL)
            if code_match:
                file_content = code_match.group(1)
            
            # Remove any trailing END FILE markers
            file_content = re.sub(r'\s*<{5}\s*END\s*FILE\s*>{5}\s*$', '', file_content)
            
            changes.append((file_path, file_content.strip()))
        i += 2
    
    return changes


def _execute_plan(tasks: list, context: str):
    """Execute a plan task by task."""
    client = get_api_client()
    
    for task in tasks:
        console.print(f"\n[blue]Task {task.id}:[/blue] {task.title}")
        
        try:
            response = client.generate(
                task=task.description,
                context=context,
                file_paths=task.files,
            )
            
            console.print(f"[green]✓ Generated[/green]")
            
            if click.confirm("Apply this task?"):
                _apply_changes(response.content, task=task.title)
            else:
                if click.confirm("Skip remaining tasks?"):
                    break
        
        except APIError as e:
            console.print(f"[red]Error:[/red] {e}")
            if not click.confirm("Continue with next task?"):
                break


# ============================================================
# Rollback Commands
# ============================================================

@cli.group()
def rollback():
    """Rollback file changes."""
    pass


@rollback.command(name="last")
def rollback_last():
    """Rollback to the last snapshot."""
    from engine.rollback import RollbackManager
    
    manager = RollbackManager(Path.cwd())
    snapshot = manager.get_latest_snapshot()
    
    if snapshot is None:
        console.print("[yellow]No snapshots available.[/yellow]")
        return
    
    console.print(f"[blue]Last snapshot:[/blue] {snapshot.id}")
    console.print(f"  Task: {snapshot.task}")
    console.print(f"  Files: {len(snapshot.files)}")
    
    for file_state in snapshot.files:
        status = "[green]existed[/green]" if file_state.existed else "[yellow]new[/yellow]"
        console.print(f"    • {file_state.path} ({status})")
    
    if click.confirm("\nRollback to this snapshot?"):
        if manager.rollback():
            console.print("[green]✓ Rollback complete[/green]")
        else:
            console.print("[red]Rollback failed[/red]")


@rollback.command(name="list")
def rollback_list():
    """List available snapshots."""
    from engine.rollback import RollbackManager
    
    manager = RollbackManager(Path.cwd())
    snapshots = manager.list_snapshots()
    
    if not snapshots:
        console.print("[yellow]No snapshots available.[/yellow]")
        return
    
    table = Table(title="Available Snapshots")
    table.add_column("ID", style="cyan")
    table.add_column("Timestamp", style="dim")
    table.add_column("Task")
    table.add_column("Files", justify="right")
    
    for snapshot in snapshots:
        # Parse timestamp for display
        from datetime import datetime
        ts = datetime.fromisoformat(snapshot.timestamp)
        ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
        
        # Truncate task if too long
        task_display = snapshot.task[:40] + "..." if len(snapshot.task) > 40 else snapshot.task
        
        table.add_row(
            snapshot.id,
            ts_str,
            task_display,
            str(len(snapshot.files)),
        )
    
    console.print(table)
    console.print(f"\n[dim]Use 'engine rollback to <id>' to rollback to a specific snapshot[/dim]")


@rollback.command(name="to")
@click.argument("snapshot_id")
def rollback_to(snapshot_id: str):
    """Rollback to a specific snapshot."""
    from engine.rollback import RollbackManager
    
    manager = RollbackManager(Path.cwd())
    snapshot = manager.get_snapshot(snapshot_id)
    
    if snapshot is None:
        console.print(f"[red]Snapshot '{snapshot_id}' not found.[/red]")
        console.print("Run 'engine rollback list' to see available snapshots.")
        return
    
    console.print(f"[blue]Snapshot:[/blue] {snapshot.id}")
    console.print(f"  Task: {snapshot.task}")
    console.print(f"  Files: {len(snapshot.files)}")
    
    for file_state in snapshot.files:
        status = "[green]existed[/green]" if file_state.existed else "[yellow]new[/yellow]"
        console.print(f"    • {file_state.path} ({status})")
    
    if click.confirm("\nRollback to this snapshot?"):
        if manager.rollback(snapshot_id):
            console.print("[green]✓ Rollback complete[/green]")
        else:
            console.print("[red]Rollback failed[/red]")


@rollback.command(name="clear")
def rollback_clear():
    """Clear all snapshots."""
    from engine.rollback import RollbackManager
    
    manager = RollbackManager(Path.cwd())
    snapshots = manager.list_snapshots()
    
    if not snapshots:
        console.print("[yellow]No snapshots to clear.[/yellow]")
        return
    
    if click.confirm(f"Clear {len(snapshots)} snapshot(s)?"):
        manager.clear_all_snapshots()
        console.print("[green]✓ All snapshots cleared[/green]")


# ============================================================
# Undo Shortcut (alias for rollback last)
# ============================================================

@cli.command()
def undo():
    """Undo the last code generation (shortcut for 'rollback last')."""
    from engine.rollback import RollbackManager
    
    manager = RollbackManager(Path.cwd())
    snapshot = manager.get_latest_snapshot()
    
    if snapshot is None:
        console.print("[yellow]Nothing to undo.[/yellow]")
        return
    
    console.print(f"[blue]Undo:[/blue] {snapshot.task}")
    console.print(f"[dim]Files: {', '.join(f.path for f in snapshot.files)}[/dim]")
    
    if click.confirm("Undo these changes?"):
        if manager.rollback():
            console.print("[green]✓ Undo complete[/green]")
        else:
            console.print("[red]Undo failed[/red]")


# ============================================================
# Entry Point
# ============================================================

def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
