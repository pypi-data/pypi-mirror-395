"""Plan (playbook) management commands for custom pentest plans."""

import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

from twpt_cli.config.playbooks import (
    save_playbook,
    save_playbook_from_file,
    get_playbook,
    list_playbooks,
    delete_playbook,
    get_playbooks_dir,
    ensure_playbooks_dir,
    playbook_exists,
)

console = Console()


@click.group()
def plan():
    """Manage custom pentest playbooks.

    Playbooks are markdown documents that define multi-step pentest methodologies.
    The AI agent executes each section systematically, following your custom workflow.

    \b
    STORAGE:
      Playbooks are stored in the playbooks/ folder (auto-created on CLI start).
      Each playbook is a .md file that can be edited directly or via 'plan edit'.

    \b
    PLAYBOOK FORMAT:
      Playbooks use markdown with sections for each phase:

        # Web Application Audit
        ## Phase 1: Reconnaissance
        - [ ] Enumerate subdomains
        - [ ] Identify technologies
        ## Phase 2: Vulnerability Scan
        - [ ] Test for SQLi
        - [ ] Check for XSS

    \b
    COMMANDS:
      plan init                          Create playbooks/ folder with README
      plan save <file> <name>            Save a playbook from a markdown file
      plan list                          List all saved playbooks
      plan show <name> [--content]       Show playbook details
      plan edit <name>                   Open playbook in default editor
      plan delete <name>                 Delete a playbook
      plan preview <file>                Preview a plan file before saving
      plan path                          Show playbooks folder path

    \b
    USING PLAYBOOKS:
      twpt-cli run target.com --plan web-audit       Use saved playbook
      twpt-cli run target.com --plan file:./plan.md  Use file directly

    \b
    NOTE:
      When using a playbook, memory/default.md is NOT auto-included.
      Use --memory explicitly if you need additional context.
    """
    pass


@plan.command()
def init():
    """Initialize the playbooks folder with README.

    Creates the playbooks/ folder in the current directory if it doesn't exist,
    along with a README explaining how to create and use playbooks.

    Example:
        twpt-cli plan init
    """
    playbooks_dir = ensure_playbooks_dir()
    console.print(f"[green]Playbooks folder initialized: {playbooks_dir}[/green]")
    console.print("\nNext steps:", style="cyan")
    console.print("  1. Create .md files in the playbooks/ folder", style="dim")
    console.print("  2. Run with: twpt-cli run <target> --plan <name>", style="dim")


@plan.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.argument('name', required=False)
@click.option('--name', '-n', 'name_opt', help='Name for the playbook (alternative to positional)')
def save(file_path: str, name: Optional[str], name_opt: Optional[str]):
    """Save a playbook from a markdown file.

    \b
    Arguments:
        FILE_PATH  Path to the markdown file containing the plan
        NAME       Name for the playbook (optional if using --name)

    The file is copied to the playbooks/ folder with the given name.

    Examples:
        twpt-cli plan save ./webapp-audit.md web-audit
        twpt-cli plan save ./api-test.md --name api-test
    """
    # Use positional name or --name option
    plan_name = name or name_opt
    if not plan_name:
        # Use filename as default name
        plan_name = Path(file_path).stem
        console.print(f"[dim]Using filename as name: {plan_name}[/dim]")

    try:
        result = save_playbook_from_file(file_path, plan_name)

        action = result["action"]
        console.print(f"\n[green bold]Playbook {action}: {result['name']}[/green bold]")
        console.print(f"  File: {result['file_path']}", style="dim")
        console.print(f"\n[dim]Use with: twpt-cli run <target> --plan {result['name']}[/dim]")

    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Failed to save playbook: {e}[/red]")
        sys.exit(1)


@plan.command(name='list')
def list_cmd():
    """List all saved playbooks.

    Shows all .md files in the playbooks/ folder (excluding README.md).

    Examples:
        twpt-cli plan list
    """
    items = list_playbooks()

    if not items:
        playbooks_dir = get_playbooks_dir()
        if not playbooks_dir.exists():
            console.print("[yellow]Playbooks folder not found[/yellow]")
            console.print(f"\nRun 'twpt-cli plan init' to create it", style="dim")
        else:
            console.print("[yellow]No playbooks found[/yellow]")
            console.print(f"\nCreate playbooks in: {playbooks_dir}", style="dim")
            console.print("Or use: twpt-cli plan save <file> <name>", style="dim")
        return

    # Create table
    table = Table(title="Playbooks", show_header=True, header_style="bold cyan")
    table.add_column("Name", style="white")
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

        table.add_row(
            item['name'],
            size_str,
            modified,
        )

    console.print(table)
    console.print(f"\nFolder: {get_playbooks_dir()}", style="dim")


@plan.command()
@click.argument('name')
@click.option('--content', '-c', is_flag=True, help='Show full playbook content')
def show(name: str, content: bool):
    """Show details of a saved playbook.

    NAME is the playbook name (with or without .md extension).

    Examples:
        twpt-cli plan show web-audit
        twpt-cli plan show api-test --content
    """
    playbook_data = get_playbook(name)

    if not playbook_data:
        console.print(f"[red]Playbook not found: {name}[/red]")
        console.print(f"\nLooking in: {get_playbooks_dir()}", style="dim")

        # Show available items
        items = list_playbooks()
        if items:
            console.print("\nAvailable playbooks:", style="dim")
            for item in items[:5]:
                console.print(f"  - {item['name']}", style="dim")
        sys.exit(1)

    # Display playbook info
    console.print(f"\n[cyan]{'=' * 50}[/cyan]")
    console.print(f"[cyan bold]Playbook: {playbook_data['name']}[/cyan bold]")
    console.print(f"[cyan]{'=' * 50}[/cyan]\n")

    console.print(f"File: {playbook_data['file_path']}", style="dim")

    # Parse content for stats
    plan_content = playbook_data.get('content', '')
    lines = plan_content.split('\n')
    sections = [l for l in lines if l.startswith('#')]

    console.print(f"Lines: {len(lines)}", style="dim")
    console.print(f"Sections: {len(sections)}", style="dim")

    if sections:
        console.print("\nSections:", style="white")
        for section in sections[:10]:
            console.print(f"  {section}", style="yellow")
        if len(sections) > 10:
            console.print(f"  ... and {len(sections) - 10} more", style="dim")

    # Show content if requested
    if content:
        console.print(f"\n[cyan]{'─' * 50}[/cyan]")
        console.print("[cyan bold]Content:[/cyan bold]\n")
        syntax = Syntax(plan_content, "markdown", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, border_style="cyan"))

    console.print(f"\n[dim]Use with: twpt-cli run <target> --plan {playbook_data['name']}[/dim]")


@plan.command()
@click.argument('name')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation')
def delete(name: str, force: bool):
    """Delete a saved playbook.

    NAME is the playbook name (with or without .md extension).

    Examples:
        twpt-cli plan delete old-plan
        twpt-cli plan delete web-audit --force
    """
    # Check if playbook exists
    playbook_data = get_playbook(name)
    if not playbook_data:
        console.print(f"[red]Playbook not found: {name}[/red]")
        sys.exit(1)

    # Confirm deletion
    if not force:
        console.print(f"Playbook: {playbook_data['name']}")
        preview = playbook_data['content'][:50] + '...' if len(playbook_data['content']) > 50 else playbook_data['content']
        console.print(f"Preview: {preview}", style="dim")

        if not click.confirm(f"\nDelete this playbook?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

    # Delete the playbook
    if delete_playbook(name):
        console.print(f"[green]Playbook deleted: {name}[/green]")
    else:
        console.print("[red]Failed to delete playbook[/red]")
        sys.exit(1)


@plan.command()
@click.argument('name')
def edit(name: str):
    """Open a playbook in the default editor.

    NAME is the playbook name (with or without .md extension).
    If the playbook doesn't exist, it will be created.

    Examples:
        twpt-cli plan edit web-audit
        twpt-cli plan edit new-plan
    """
    import subprocess
    import os

    ensure_playbooks_dir()

    # Normalize name and get file path
    from twpt_cli.config.playbooks import get_playbook_file_path
    file_path = get_playbook_file_path(name)

    # Create template file if it doesn't exist
    if not file_path.exists():
        template = f'''# {name}

## Overview
Describe the purpose of this pentest plan.

## Phase 1: Reconnaissance
- [ ] Task 1
- [ ] Task 2

## Phase 2: Vulnerability Assessment
- [ ] Task 1
- [ ] Task 2

## Phase 3: Exploitation
- [ ] Task 1
- [ ] Task 2

## Deliverables
- Summary of findings
- Risk ratings
'''
        file_path.write_text(template)
        console.print(f"[cyan]Created new playbook: {file_path}[/cyan]")

    # Get the editor
    editor = os.environ.get('EDITOR', os.environ.get('VISUAL', 'nano'))

    console.print(f"Opening {file_path} with {editor}...", style="dim")

    try:
        subprocess.run([editor, str(file_path)], check=True)
        console.print(f"[green]Playbook saved: {name}[/green]")
    except FileNotFoundError:
        console.print(f"[red]Editor not found: {editor}[/red]")
        console.print(f"Edit the file manually: {file_path}", style="dim")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Editor exited with error: {e}[/red]")
        sys.exit(1)


@plan.command()
@click.argument('file_path', type=click.Path(exists=True))
def preview(file_path: str):
    """Preview a plan file before saving.

    FILE_PATH is the path to the markdown file.

    Examples:
        twpt-cli plan preview ./my-plan.md
    """
    try:
        content = Path(file_path).read_text()

        # Basic stats
        lines = content.split('\n')
        sections = [l for l in lines if l.startswith('#')]

        console.print(f"\n[cyan]{'=' * 50}[/cyan]")
        console.print(f"[cyan bold]Plan Preview[/cyan bold]")
        console.print(f"[cyan]{'=' * 50}[/cyan]\n")

        console.print(f"File: {file_path}", style="white")
        console.print(f"Lines: {len(lines)}", style="dim")
        console.print(f"Sections: {len(sections)}", style="dim")

        if sections:
            console.print("\nSections found:", style="white")
            for section in sections[:10]:
                console.print(f"  {section}", style="yellow")
            if len(sections) > 10:
                console.print(f"  ... and {len(sections) - 10} more", style="dim")

        # Show content preview
        console.print(f"\n[cyan]{'─' * 50}[/cyan]")
        syntax = Syntax(content, "markdown", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title="Content Preview", border_style="cyan"))

        console.print(f"\nTo save: twpt-cli plan save {file_path} <name>", style="cyan")
        console.print(f"To use directly: twpt-cli run <target> --plan file:{file_path}", style="cyan")

    except FileNotFoundError as e:
        console.print(f"[red]File not found: {e}[/red]")
        sys.exit(1)


@plan.command()
def path():
    """Show the playbooks folder path.

    Example:
        twpt-cli plan path
    """
    playbooks_dir = get_playbooks_dir()
    console.print(f"{playbooks_dir}")

    if playbooks_dir.exists():
        items = list_playbooks()
        console.print(f"\n[dim]{len(items)} playbook(s) found[/dim]")
    else:
        console.print("[dim]Folder does not exist. Run 'plan init' to create it.[/dim]")
