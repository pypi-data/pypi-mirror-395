"""Memory management commands for pentest context/notes."""

import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from twpt_cli.config.memory import (
    save_memory,
    get_memory,
    list_memory,
    delete_memory,
    get_memory_dir,
    ensure_memory_dir,
    memory_exists,
    DEFAULT_MEMORY_FILE,
)

console = Console()


@click.group()
def memory():
    """Manage pentest memory/context notes.

    Memory items are notes or context that persist throughout all phases of a
    pentest. The AI agent keeps these in mind during reconnaissance, scanning,
    exploitation, and reporting.

    \b
    STORAGE:
      Memory items are stored in the memory/ folder (auto-created on CLI start).
      Each item is a .md file that can be edited directly or via 'memory edit'.

    \b
    DEFAULT MEMORY (memory/default.md):
      This file is AUTOMATICALLY included in every standard pentest.
      Great for your preferred methodology, common credentials, tool preferences.
      Note: default.md is NOT included when using custom playbooks (--plan).

    \b
    COMMANDS:
      memory list                       List all saved memory items
      memory edit <name>                Open in default editor (creates if new)
      memory show <name>                Show memory item content
      memory save <name> <content>      Save a memory item from CLI
      memory delete <name>              Delete a memory item
      memory path                       Show memory folder path

    \b
    USING MEMORY WITH RUN COMMAND:
      Use @name to load saved files, plain text for inline context:

      -m @name           Load memory/name.md file
      -m "plain text"    Inline context (not saved)

    \b
    EXAMPLES:

    Managing memory:
      twpt-cli memory list                              # See all saved items
      twpt-cli memory edit default                      # Edit default memory
      twpt-cli memory edit sqli                         # Create/edit sqli.md
      twpt-cli memory save creds "admin:admin"          # Quick save from CLI
      twpt-cli memory show brute-force                  # View content
      twpt-cli memory delete old-notes                  # Delete an item

    \b
    Using memory in pentests:
      twpt-cli run target.com                           # Uses default.md
      twpt-cli run target.com -m @sqli                  # Load sqli.md
      twpt-cli run target.com -m "Check /admin"         # Inline text
      twpt-cli run target.com -m @creds -m @sqli        # Multiple files
      twpt-cli run target.com -m @tips -m "Be thorough" # File + inline
      twpt-cli run target.com --no-default-memory       # Skip default.md
    """
    pass


@memory.command()
def init():
    """Initialize the memory folder with README.

    Creates the memory/ folder in the current directory if it doesn't exist,
    along with a README explaining how to use memory items.

    Example:
        twpt-cli memory init
    """
    memory_dir = ensure_memory_dir()
    console.print(f"[green]Memory folder initialized: {memory_dir}[/green]")
    console.print("\nNext steps:", style="cyan")
    console.print(f"  1. Create {memory_dir}/default.md for default context", style="dim")
    console.print(f"  2. Create additional .md files for specific use cases", style="dim")
    console.print(f"  3. Run pentest with: twpt-cli run <target>", style="dim")


@memory.command()
@click.argument('name')
@click.argument('content')
def save(name: str, content: str):
    """Save a memory item to the memory folder.

    \b
    Arguments:
        NAME     Name for the memory item (becomes filename.md)
        CONTENT  The memory content/note text

    The content is saved as a markdown file in the memory/ folder.
    Use "default" as the name to create the default memory item.

    Examples:
        twpt-cli memory save brute-force "Always try brute force on SSH"
        twpt-cli memory save default "Focus on web application testing"
        twpt-cli memory save sqli "Test all forms for SQL injection"
    """
    try:
        result = save_memory(name=name, content=content)

        action = result["action"]
        console.print(f"\n[green bold]Memory {action}: {result['name']}[/green bold]")
        console.print(f"  File: {result['file_path']}", style="dim")

        if result['name'] == 'default':
            console.print("\n[cyan]This is the default memory - it will be included in all standard pentests.[/cyan]")
        else:
            console.print(f"\n[dim]Use with: twpt-cli run <target> --memory {result['name']}[/dim]")

    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Failed to save memory: {e}[/red]")
        sys.exit(1)


@memory.command(name='list')
def list_cmd():
    """List all memory items in the memory folder.

    Shows all .md files in the memory/ folder (excluding README.md).

    Examples:
        twpt-cli memory list
    """
    items = list_memory()

    if not items:
        memory_dir = get_memory_dir()
        if not memory_dir.exists():
            console.print("[yellow]Memory folder not found[/yellow]")
            console.print(f"\nRun 'twpt-cli memory init' to create it", style="dim")
        else:
            console.print("[yellow]No memory items found[/yellow]")
            console.print(f"\nCreate memory items in: {memory_dir}", style="dim")
            console.print("Or use: twpt-cli memory save <name> <content>", style="dim")
        return

    # Create table
    table = Table(title="Memory Items", show_header=True, header_style="bold cyan")
    table.add_column("Name", style="white")
    table.add_column("Type", style="green")
    table.add_column("Size", style="dim")
    table.add_column("Modified", style="dim")

    for item in items:
        # Format the modified timestamp
        modified = datetime.fromtimestamp(item['modified']).strftime('%Y-%m-%d %H:%M')

        # Format size
        size = item['size']
        if size < 1024:
            size_str = f"{size} B"
        else:
            size_str = f"{size // 1024} KB"

        item_type = "[cyan]default[/cyan]" if item['is_default'] else "custom"

        table.add_row(
            item['name'],
            item_type,
            size_str,
            modified,
        )

    console.print(table)
    console.print(f"\nFolder: {get_memory_dir()}", style="dim")


@memory.command()
@click.argument('name')
def show(name: str):
    """Show contents of a memory item.

    NAME is the memory item name (with or without .md extension).

    Examples:
        twpt-cli memory show brute-force
        twpt-cli memory show default
    """
    item_data = get_memory(name)

    if not item_data:
        console.print(f"[red]Memory item not found: {name}[/red]")
        console.print(f"\nLooking in: {get_memory_dir()}", style="dim")

        # Show available items
        items = list_memory()
        if items:
            console.print("\nAvailable items:", style="dim")
            for item in items[:5]:
                console.print(f"  - {item['name']}", style="dim")
        sys.exit(1)

    # Display item info
    is_default = item_data['name'] == 'default'

    console.print(f"\n[cyan]{'=' * 50}[/cyan]")
    if is_default:
        console.print(f"[cyan bold]Memory: {item_data['name']} (DEFAULT)[/cyan bold]")
    else:
        console.print(f"[cyan bold]Memory: {item_data['name']}[/cyan bold]")
    console.print(f"[cyan]{'=' * 50}[/cyan]\n")

    console.print(f"File: {item_data['file_path']}", style="dim")

    if is_default:
        console.print("[cyan]This memory is auto-included in all standard pentests[/cyan]")

    # Show content
    console.print(f"\n[cyan]{'─' * 50}[/cyan]")
    console.print("[cyan bold]Content:[/cyan bold]\n")
    console.print(Panel(item_data['content'], border_style="cyan"))

    if not is_default:
        console.print(f"\n[dim]Use with: twpt-cli run <target> --memory {item_data['name']}[/dim]")


@memory.command()
@click.argument('name')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation')
def delete(name: str, force: bool):
    """Delete a memory item.

    NAME is the memory item name (with or without .md extension).

    Examples:
        twpt-cli memory delete old-notes
        twpt-cli memory delete brute-force --force
    """
    # Check if item exists
    item_data = get_memory(name)
    if not item_data:
        console.print(f"[red]Memory item not found: {name}[/red]")
        sys.exit(1)

    # Confirm deletion
    if not force:
        console.print(f"Memory: {item_data['name']}")
        preview = item_data['content'][:50] + '...' if len(item_data['content']) > 50 else item_data['content']
        console.print(f"Preview: {preview}", style="dim")

        if item_data['name'] == 'default':
            console.print("[yellow]Warning: This is the default memory item![/yellow]")

        if not click.confirm(f"\nDelete this memory item?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

    # Delete the item
    if delete_memory(name):
        console.print(f"[green]Memory deleted: {name}[/green]")
    else:
        console.print("[red]Failed to delete memory item[/red]")
        sys.exit(1)


@memory.command()
@click.argument('name')
def edit(name: str):
    """Open a memory item in the default editor.

    NAME is the memory item name (with or without .md extension).
    If the item doesn't exist, it will be created.

    Examples:
        twpt-cli memory edit brute-force
        twpt-cli memory edit default
    """
    import subprocess
    import os

    ensure_memory_dir()

    # Normalize name and get file path
    from twpt_cli.config.memory import get_memory_file_path
    file_path = get_memory_file_path(name)

    # Create empty file if it doesn't exist
    if not file_path.exists():
        file_path.write_text(f"# {name}\n\nAdd your memory content here.\n")
        console.print(f"[cyan]Created new memory file: {file_path}[/cyan]")

    # Get the editor
    editor = os.environ.get('EDITOR', os.environ.get('VISUAL', 'nano'))

    console.print(f"Opening {file_path} with {editor}...", style="dim")

    try:
        subprocess.run([editor, str(file_path)], check=True)
        console.print(f"[green]Memory item saved: {name}[/green]")
    except FileNotFoundError:
        console.print(f"[red]Editor not found: {editor}[/red]")
        console.print(f"Edit the file manually: {file_path}", style="dim")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Editor exited with error: {e}[/red]")
        sys.exit(1)


@memory.command()
def path():
    """Show the memory folder path.

    Example:
        twpt-cli memory path
    """
    memory_dir = get_memory_dir()
    console.print(f"{memory_dir}")

    if memory_dir.exists():
        items = list_memory()
        console.print(f"\n[dim]{len(items)} memory item(s) found[/dim]")

        # Check for default
        default_exists = any(i['is_default'] for i in items)
        if default_exists:
            console.print("[cyan]default.md present (auto-included)[/cyan]")
        else:
            console.print("[dim]No default.md (create one for auto-inclusion)[/dim]")
    else:
        console.print("[dim]Folder does not exist. Run 'memory init' to create it.[/dim]")
