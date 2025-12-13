#!/usr/bin/env python3
"""Main entry point for ThreatWinds Pentest CLI."""

import click
import sys
from pathlib import Path

from twpt_cli import __version__
from twpt_cli.commands import (
    init,
    configure,
    install_frontend,
    schedule_pentest,
    get_pentest,
    download_evidence,
    list_pentests,
    update,
    uninstall,
    version_cmd,
    webui,
    chat,
    watch,
    custom_task,
    watch_task,
    plan,
    memory,
)


def _ensure_project_folders():
    """Ensure memory/ and playbooks/ folders exist with proper content.

    Creates the folders with README files if they don't exist.
    For memory/, also creates a default.md template.
    If creation fails, prints a warning but doesn't crash the CLI.
    """
    from twpt_cli.config.memory import ensure_memory_dir, get_memory_dir, get_memory_file_path
    from twpt_cli.config.playbooks import ensure_playbooks_dir, get_playbooks_dir

    # Create memory folder with README
    try:
        memory_dir = get_memory_dir()
        if not memory_dir.exists():
            ensure_memory_dir()
            # Also create default.md template
            default_path = get_memory_file_path("default")
            if not default_path.exists():
                default_content = """# Default Memory

This file is automatically included in all standard pentests.
Edit this file to add your default testing context and instructions.

## Example content:
- Always try default credentials (admin:admin, root:root)
- Focus on OWASP Top 10 vulnerabilities
- Document all findings with screenshots
"""
                default_path.write_text(default_content)
    except PermissionError:
        click.echo(
            "Warning: Cannot create memory/ folder (permission denied). "
            "Create it manually to use memory features.",
            err=True
        )
    except OSError as e:
        click.echo(
            f"Warning: Cannot create memory/ folder: {e}. "
            "Create it manually to use memory features.",
            err=True
        )

    # Create playbooks folder with README
    try:
        playbooks_dir = get_playbooks_dir()
        if not playbooks_dir.exists():
            ensure_playbooks_dir()
    except PermissionError:
        click.echo(
            "Warning: Cannot create playbooks/ folder (permission denied). "
            "Create it manually to use playbooks features.",
            err=True
        )
    except OSError as e:
        click.echo(
            f"Warning: Cannot create playbooks/ folder: {e}. "
            "Create it manually to use playbooks features.",
            err=True
        )


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="twpt-cli")
@click.option(
    '--shell', '-s',
    is_flag=True,
    help='Start interactive shell mode'
)
@click.pass_context
def cli(ctx, shell):
    """ThreatWinds Pentest CLI - AI-powered penetration testing.

    This CLI connects to a ThreatWinds agent server for AI-powered
    automated penetration testing.

    Start without arguments or use --shell to enter interactive mode.

    \b
    SETUP:
      twpt-cli configure                    Configure API credentials
      twpt-cli init --host <ip>             Connect to remote agent server

    \b
    QUICK START:
      twpt-cli run example.com --watch      Run pentest with live output
      twpt-cli run example.com --safe       Safe/non-destructive mode
      twpt-cli list                         List recent pentests
      twpt-cli get <id>                     Get pentest details

    \b
    PLAYBOOKS (Custom Plans):
      Markdown files in playbooks/ folder defining pentest methodology.

      twpt-cli plan list                    List saved playbooks
      twpt-cli plan edit web-audit          Create/edit a playbook
      twpt-cli run target --plan web-audit  Run with playbook

    \b
    MEMORY (Context/Notes):
      Notes in memory/ folder passed to AI agent during pentests.
      memory/default.md is AUTO-INCLUDED in standard pentests.

      twpt-cli memory list                  List saved items
      twpt-cli memory edit default          Edit default memory

      Using memory with run (@name=file, "text"=inline):
        twpt-cli run target -m @sqli        Load memory/sqli.md
        twpt-cli run target -m "Check XSS"  Inline context
        twpt-cli run target -m @a -m @b     Multiple files

    \b
    FOLDERS (auto-created):
      memory/      Context notes (default.md auto-included)
      playbooks/   Custom pentest plans
    """
    # Ensure context object exists
    ctx.ensure_object(dict)

    # Ensure memory/ and playbooks/ folders exist
    _ensure_project_folders()

    # If no command is given or shell flag is used, start interactive shell
    if ctx.invoked_subcommand is None or shell:
        from twpt_cli.shell import InteractiveShell
        shell = InteractiveShell()
        shell.run()
        sys.exit(0)


# Register all commands
cli.add_command(init.init)
cli.add_command(configure.configure)
cli.add_command(install_frontend.install_frontend)

# Add run command (primary) with legacy alias
cli.add_command(schedule_pentest.schedule_pentest)  # Legacy alias
cli.add_command(schedule_pentest.schedule_pentest, name="run")  # Primary command

# Add get command (primary) with legacy alias
cli.add_command(get_pentest.get_pentest)  # Legacy alias
cli.add_command(get_pentest.get_pentest, name="get")  # Primary command

# Add download command (primary) with legacy alias
cli.add_command(download_evidence.download_evidence)  # Legacy alias
cli.add_command(download_evidence.download_evidence, name="download")  # Primary command

# Add list command (primary) with legacy alias
cli.add_command(list_pentests.list_pentests)  # Legacy alias
cli.add_command(list_pentests.list_pentests, name="list")  # Primary command

cli.add_command(update.update_latest)
cli.add_command(uninstall.uninstall)
cli.add_command(version_cmd.version)
cli.add_command(webui.webui)

# Chat command for asking questions about pentest results
cli.add_command(chat.chat)

# Watch command for late-join streaming to running pentests
cli.add_command(watch.watch)

# Custom task command for ad-hoc pentesting tasks
cli.add_command(custom_task.custom_task, name="task")

# Watch-task command for monitoring running custom tasks
cli.add_command(watch_task.watch_task, name="watch-task")

# Plan command for managing custom pentest plans
cli.add_command(plan.plan)

# Memory command for managing pentest context/notes
cli.add_command(memory.memory)


def main():
    """Main entry point for the CLI."""
    # Check if no arguments provided - start shell
    if len(sys.argv) == 1:
        # No arguments, start interactive shell
        from twpt_cli.shell import InteractiveShell
        shell = InteractiveShell()
        shell.run()
        sys.exit(0)

    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n\nOperation cancelled by user.", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"\nError: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()