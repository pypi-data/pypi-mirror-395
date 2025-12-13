#!/usr/bin/env python3
"""Interactive shell for ThreatWinds Pentest CLI."""

import os
import sys
import atexit
import threading
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any, Iterable
import shlex

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from rich.markdown import Markdown
from rich import print as rprint

# prompt_toolkit imports for enhanced input
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion, WordCompleter, merge_completers
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles import Style as PTStyle
from prompt_toolkit.formatted_text import HTML, FormattedText, ANSI
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.document import Document

from twpt_cli import __version__
from twpt_cli.config import (
    load_credentials,
    load_endpoint_config,
    check_configured,
    get_api_endpoint,
    get_grpc_endpoint,
)

# Import command implementations
from twpt_cli.commands import (
    init,
    configure,
    schedule_pentest,
    get_pentest,
    download_evidence,
    update,
    uninstall,
    version_cmd,
    webui,
    chat,
    watch,
    custom_task,
)
from twpt_cli.request_interpreter import AIRequestInterpreter, interpret_request, extract_target_from_text

# History file
HISTORY_FILE = Path.home() / ".twpt" / ".history"


def truncate_pentest_id(pentest_id: str, max_length: int = 20) -> str:
    """
    Truncate a pentest ID for display purposes.

    Handles both formats intelligently:
    - UUID (af590497-2e14-4406-8f80-4d3c793194bc): Shows first 8 + last 4 chars
    - Friendly ID (swift-falcon-strikes): Shows full ID if short, or first 2 words

    Args:
        pentest_id: The pentest ID to truncate
        max_length: Maximum length for the output (default: 20)

    Returns:
        Truncated ID suitable for display
    """
    if not pentest_id:
        return ""

    # If already short enough, return as-is
    if len(pentest_id) <= max_length:
        return pentest_id

    parts = pentest_id.split('-')

    # UUID format: 5 parts (show first 8 + last 4)
    if len(parts) == 5 and len(pentest_id) == 36:
        return f"{pentest_id[:8]}...{pentest_id[-4:]}"

    # Friendly ID format: show first 2 words if too long
    if len(parts) >= 3 and all(p.isalpha() for p in parts[:3]):
        # Show first two words + ellipsis
        short = f"{parts[0]}-{parts[1]}..."
        if len(short) <= max_length:
            return short
        # If still too long, just truncate
        return f"{pentest_id[:max_length-3]}..."

    # Fallback: simple truncation
    return f"{pentest_id[:max_length-3]}..."

# ═══════════════════════════════════════════════════════════════════════════════
# Command Definitions for Autocompletion
# ═══════════════════════════════════════════════════════════════════════════════

COMMANDS = {
    "run": {
        "help": "Run a new pentest against a target",
        "args": ["<target>"],
        "options": {
            "--safe": "Use safe/non-destructive mode",
            "--no-exploit": "Skip exploitation phase",
            "--watch": "Watch progress in real-time",
            "--plan": "Playbook: <name> or file:<path>",
            "--scope": "Scope: holistic or targeted",
            "-m, --memory": "Memory: @name (file) or \"text\" (inline)",
            "--no-default-memory": "Skip memory/default.md",
        },
        "examples": [
            "run example.com --watch",
            "run example.com --safe --no-exploit",
            "run example.com --plan web-audit",
            "run example.com --plan file:./custom.md",
            "run example.com -m @brute-force",
            'run example.com -m "Focus on SQL injection"',
            "run example.com -m @creds -m @sqli --watch",
        ],
    },
    "get": {
        "help": "Get details of a specific pentest",
        "args": ["<pentest-id>"],
        "options": {},
    },
    "download": {
        "help": "Download evidence and reports",
        "args": ["<pentest-id>"],
        "options": {
            "--output": "Output directory path",
            "--no-extract": "Keep as ZIP archive",
        },
    },
    "list": {
        "help": "List recent pentests",
        "args": [],
        "options": {
            "--page": "Page number",
            "--page-size": "Results per page",
            "--all": "Show all pentests",
        },
    },
    "watch": {
        "help": "Watch a running pentest live",
        "args": ["[pentest-id]"],
        "options": {
            "--no-history": "Skip historical events",
            "-q": "Only show important updates",
        },
        "examples": [
            "watch              # Auto-selects latest pentest",
            "watch abc123       # Watch specific pentest",
        ],
    },
    "stop": {
        "help": "Stop watching current pentest",
        "args": [],
        "options": {},
    },
    "hint": {
        "help": "Inject a hint/context into the running pentest",
        "args": ["<hint text>"],
        "options": {
            "--high": "Send with HIGH priority",
            "--immediate": "Send with IMMEDIATE priority (interrupts agent)",
        },
        "examples": [
            "hint Try SQL injection on /api/login",
            "hint --high Focus on the admin panel",
            "hint --immediate Stop and check port 8443",
        ],
    },
    "chat": {
        "help": "Chat with AI about pentest results",
        "args": ["<pentest-id>", "[question]"],
        "options": {
            "--interactive": "Interactive chat mode",
            "-i": "Interactive chat mode",
        },
    },
    "init": {
        "help": "Connect to remote agent server",
        "args": ["<host>", "<port>"],
        "options": {
            "--local": "Use local agent (Kali only)",
            "--skip-test": "Skip connection test",
        },
    },
    "configure": {
        "help": "Configure API credentials",
        "args": [],
        "options": {
            "--skip-validation": "Skip credential validation",
        },
    },
    "status": {
        "help": "Show current configuration",
        "args": [],
        "options": {},
    },
    "update": {
        "help": "Update the toolkit",
        "args": [],
        "options": {
            "--force": "Force update even if current",
        },
    },
    "uninstall": {
        "help": "Uninstall the toolkit",
        "args": [],
        "options": {
            "--remove-data": "Also remove data files",
        },
    },
    "version": {
        "help": "Show version information",
        "args": [],
        "options": {
            "--detailed": "Show detailed info",
            "-d": "Show detailed info",
        },
    },
    "webui": {
        "help": "Launch web interface (background)",
        "args": [],
        "options": {
            "--host": "Bind host address",
            "--port": "Bind port number",
            "--debug": "Enable debug mode",
        },
    },
    "stopweb": {
        "help": "Stop background web interface",
        "args": [],
        "options": {},
    },
    "help": {
        "help": "Show help information",
        "args": ["[command]"],
        "options": {},
    },
    "clear": {
        "help": "Clear the screen",
        "args": [],
        "options": {},
    },
    "exit": {
        "help": "Exit the shell",
        "args": [],
        "options": {},
    },
    "quit": {
        "help": "Exit the shell",
        "args": [],
        "options": {},
    },
    "q": {
        "help": "Exit the shell",
        "args": [],
        "options": {},
    },
    "task": {
        "help": "Run a custom pentesting task",
        "args": ["<description>"],
        "options": {
            "--target": "Target IP, domain, or URL",
            "-t": "Target (short)",
            "--session": "Continue existing session",
            "-s": "Session (short)",
            "--list": "List task sessions",
            "--close": "Close a task session",
        },
    },
    "plan": {
        "help": "Manage custom pentest playbooks",
        "args": ["<subcommand>"],
        "options": {
            "init": "Initialize playbooks/ folder",
            "save": "Save playbook from file",
            "list": "List saved playbooks",
            "show": "Show playbook details",
            "edit": "Edit in $EDITOR",
            "delete": "Delete a playbook",
            "preview": "Preview before saving",
            "path": "Show folder path",
        },
        "examples": [
            "plan list",
            "plan edit web-audit",
            "plan save ./my-plan.md web-audit",
            "plan show web-audit --content",
            "plan delete old-plan --force",
            "# Then use with: run target --plan web-audit",
        ],
    },
    "memory": {
        "help": "Manage pentest memory/context notes",
        "args": ["<subcommand>"],
        "options": {
            "init": "Initialize memory/ folder",
            "save": "Save a memory item",
            "list": "List saved items",
            "show": "Show item content",
            "edit": "Edit in $EDITOR",
            "delete": "Delete an item",
            "path": "Show folder path",
        },
        "examples": [
            "memory list",
            "memory edit default",
            'memory save sqli "Test all forms for SQL injection"',
            "memory show brute-force",
            "memory delete old-notes --force",
            "# Then use with: run target -m @sqli",
        ],
    },
}

# Option value completions
OPTION_VALUES = {
    "--scope": ["holistic", "targeted"],
    "--type": ["black-box", "white-box"],
    "--style": ["aggressive", "safe"],
}

# ═══════════════════════════════════════════════════════════════════════════════
# Custom Completer
# ═══════════════════════════════════════════════════════════════════════════════

class TWPTCompleter(Completer):
    """Smart completer for TWPT CLI commands with context awareness."""

    def __init__(self, shell: 'InteractiveShell'):
        self.shell = shell
        self._pentest_cache: List[tuple] = []  # List of (id, status, target)
        self._cache_time: float = 0
        self._cache_ttl: float = 30.0  # Cache for 30 seconds

    def _refresh_pentest_cache(self) -> List[tuple]:
        """Refresh the pentest ID cache if stale."""
        import time
        now = time.time()

        if now - self._cache_time < self._cache_ttl and self._pentest_cache:
            return self._pentest_cache

        try:
            creds = load_credentials()
            if not creds:
                return self._pentest_cache

            from twpt_cli.sdk import HTTPClient
            client = HTTPClient(get_api_endpoint(), creds)
            response = client.list_pentests(page=1, page_size=20)

            self._pentest_cache = []
            for p in response.pentests:
                target = ""
                if p.targets and len(p.targets) > 0:
                    target = p.targets[0].target[:20]
                self._pentest_cache.append((p.id, p.status, target))

            self._cache_time = now
            client.close()
        except Exception:
            pass

        return self._pentest_cache

    def get_completions(self, document: Document, complete_event) -> Iterable[Completion]:
        text = document.text_before_cursor
        word = document.get_word_before_cursor()

        # Parse what we have so far
        parts = text.split()

        # Empty or completing first word -> command completion
        if not parts or (len(parts) == 1 and not text.endswith(' ')):
            prefix = parts[0] if parts else ""
            for cmd, info in COMMANDS.items():
                if cmd.startswith(prefix):
                    yield Completion(
                        cmd,
                        start_position=-len(prefix),
                        display=HTML(f'<b>{cmd}</b>'),
                        display_meta=info["help"],
                    )
            return

        # Have a command - get its definition
        cmd = parts[0].lower()
        if cmd not in COMMANDS:
            return

        cmd_info = COMMANDS[cmd]
        options = cmd_info.get("options", {})

        # Check if previous word is an option that takes a value
        if len(parts) >= 2:
            prev = parts[-1] if text.endswith(' ') else (parts[-2] if len(parts) > 1 else "")
            if prev in OPTION_VALUES:
                values = OPTION_VALUES[prev]
                prefix = word if not text.endswith(' ') else ""
                for val in values:
                    if val.startswith(prefix):
                        yield Completion(
                            val,
                            start_position=-len(prefix),
                            display=val,
                        )
                return

        # Complete options
        used_options = set(parts[1:])

        if text.endswith(' ') or word.startswith('-'):
            prefix = word if word.startswith('-') else ""
            for opt, desc in options.items():
                if opt not in used_options and opt.startswith(prefix):
                    yield Completion(
                        opt,
                        start_position=-len(prefix),
                        display=HTML(f'<ansicyan>{opt}</ansicyan>'),
                        display_meta=desc,
                    )

        # Suggest pentest IDs for commands that need them
        if cmd in ['get', 'download', 'watch', 'chat']:
            # Only suggest if we're in the argument position
            non_opts = [p for p in parts[1:] if not p.startswith('-')]
            if not non_opts or (len(non_opts) == 1 and not text.endswith(' ') and not parts[-1].startswith('-')):
                prefix = word if not word.startswith('-') else ""

                # Get cached pentest list
                pentests = self._refresh_pentest_cache()

                # Status colors for display
                status_colors = {
                    "PENDING": "ansiyellow",
                    "IN_PROGRESS": "ansiblue",
                    "COMPLETED": "ansigreen",
                    "FAILED": "ansired",
                }

                for pid, status, target in pentests:
                    if pid.startswith(prefix):
                        color = status_colors.get(status, "ansiwhite")
                        # Show short ID with color based on status
                        display_id = truncate_pentest_id(pid)
                        meta = f"{status}"
                        if target:
                            meta += f" • {target}"

                        yield Completion(
                            pid,
                            start_position=-len(prefix),
                            display=HTML(f'<{color}>{display_id}</{color}>'),
                            display_meta=meta,
                        )


# ═══════════════════════════════════════════════════════════════════════════════
# Custom Lexer for Syntax Highlighting
# ═══════════════════════════════════════════════════════════════════════════════

class TWPTLexer(Lexer):
    """Syntax highlighter for TWPT CLI commands."""

    @staticmethod
    def _is_pentest_id(text: str) -> bool:
        """
        Check if text looks like a pentest ID.

        Matches:
        - UUIDs: 36 chars with hyphens (e.g., "af590497-2e14-4406-8f80-4d3c793194bc")
        - Friendly IDs: word-word-word format (e.g., "swift-falcon-strikes")
        - Friendly IDs with suffix: word-word-word-N (e.g., "swift-falcon-strikes-2")
        """
        if not text or not isinstance(text, str):
            return False

        parts = text.split('-')

        # UUID format: 5 parts with hex characters
        if len(parts) == 5 and len(text) == 36:
            return all(p.isalnum() for p in parts)

        # Friendly ID format: 3 or 4 parts (4 if numeric suffix)
        if len(parts) == 3:
            # word-word-word: all parts should be alphabetic
            return all(p.isalpha() for p in parts)
        elif len(parts) == 4:
            # word-word-word-N: first 3 alphabetic, last numeric
            return all(p.isalpha() for p in parts[:3]) and parts[3].isdigit()

        return False

    def lex_document(self, document: Document):
        def get_tokens(line_number):
            line = document.lines[line_number]
            parts = line.split()

            if not parts:
                return [('', line)]

            result = []
            idx = 0

            for i, part in enumerate(parts):
                # Find where this part starts
                while idx < len(line) and line[idx] == ' ':
                    result.append(('', ' '))
                    idx += 1

                if i == 0:
                    # Command - bold cyan if valid, red if invalid
                    if part.lower() in COMMANDS:
                        result.append(('class:command', part))
                    else:
                        result.append(('class:error', part))
                elif part.startswith('--') or part.startswith('-'):
                    # Option - cyan
                    result.append(('class:option', part))
                elif part.startswith('"') or part.startswith("'"):
                    # Quoted string - yellow
                    result.append(('class:string', part))
                else:
                    # Argument - green for IDs, white otherwise
                    # Match both UUIDs (36 chars) and friendly IDs (word-word-word format)
                    if self._is_pentest_id(part):
                        result.append(('class:id', part))
                    else:
                        result.append(('class:arg', part))

                idx += len(part)

            # Remaining whitespace
            while idx < len(line):
                result.append(('', line[idx]))
                idx += 1

            return result

        return get_tokens


# ═══════════════════════════════════════════════════════════════════════════════
# Style Configuration
# ═══════════════════════════════════════════════════════════════════════════════

PROMPT_STYLE = PTStyle.from_dict({
    # Input styling
    'command': '#00d7ff bold',      # Cyan bold for commands
    'option': '#87d7ff',            # Light cyan for options
    'arg': '#ffffff',               # White for arguments
    'string': '#ffd700',            # Gold for strings
    'id': '#87ff87',                # Light green for IDs
    'error': '#ff5f5f',             # Red for errors

    # Input separator (visual line above input area)
    'input-separator': '#5f5f87',   # Muted purple/gray for separator line

    # Prompt styling
    'prompt': '#d787ff bold',       # Magenta for prompt name
    'prompt.bracket': '#6c6c6c',    # Gray for brackets
    'prompt.status': '#87ff87',     # Green for status
    'prompt.status.warning': '#ffd700',  # Yellow for warnings
    'prompt.status.error': '#ff5f5f',    # Red for errors
    'prompt.arrow': '#ffffff bold', # White for arrow

    # Completion menu
    'completion-menu': 'bg:#1c1c1c #d0d0d0',
    'completion-menu.completion': '',
    'completion-menu.completion.current': 'bg:#3a3a3a #ffffff bold',
    'completion-menu.meta': '#6c6c6c italic',
    'completion-menu.meta.current': '#949494 italic',

    # Scrollbar
    'scrollbar.background': 'bg:#3a3a3a',
    'scrollbar.button': 'bg:#6c6c6c',
})


# ═══════════════════════════════════════════════════════════════════════════════
# Watch Manager
# ═══════════════════════════════════════════════════════════════════════════════

class WatchManager:
    """Manages background watch processes."""

    def __init__(self, console: Console):
        self.console = console
        self.watch_process: Optional[subprocess.Popen] = None
        self.watch_thread: Optional[threading.Thread] = None
        self.watching_pentest_id: Optional[str] = None
        self._stop_event = threading.Event()
        self._output_lock = threading.Lock()

    def is_watching(self) -> bool:
        return self.watch_process is not None and self.watch_process.poll() is None

    def start_watch(self, pentest_id: str, args: List[str]) -> bool:
        if self.is_watching():
            self.stop_watch(silent=True)

        self._stop_event.clear()
        self.watching_pentest_id = pentest_id

        cli_args = [pentest_id] + args
        cmd = [sys.executable, "-m", "twpt_cli.main", "watch"] + cli_args

        try:
            self.watch_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True,
            )

            self.watch_thread = threading.Thread(
                target=self._watch_output_loop,
                daemon=True
            )
            self.watch_thread.start()
            return True

        except Exception as e:
            self.console.print(f"[red]Failed to start watch: {e}[/red]")
            self.watch_process = None
            return False

    def _watch_output_loop(self):
        try:
            while not self._stop_event.is_set() and self.watch_process:
                if self.watch_process.poll() is not None:
                    break

                line = self.watch_process.stdout.readline()
                if line:
                    with self._output_lock:
                        sys.stdout.write('\r' + ' ' * 100 + '\r')
                        sys.stdout.write(line)
                        sys.stdout.flush()

        except Exception:
            pass
        finally:
            self._cleanup()

    def _cleanup(self):
        if self.watch_process:
            try:
                self.watch_process.terminate()
                self.watch_process.wait(timeout=2)
            except Exception:
                try:
                    self.watch_process.kill()
                except Exception:
                    pass
        self.watch_process = None
        self.watching_pentest_id = None

    def stop_watch(self, silent: bool = False) -> bool:
        if not self.is_watching():
            return False

        pentest_id = self.watching_pentest_id
        self._stop_event.set()

        if self.watch_process:
            try:
                self.watch_process.terminate()
                self.watch_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.watch_process.kill()
            except Exception:
                pass

        self._cleanup()

        if not silent:
            self.console.print(f"\n[yellow]Stopped watching pentest {pentest_id}[/yellow]")

        return True


# ═══════════════════════════════════════════════════════════════════════════════
# Interactive Shell
# ═══════════════════════════════════════════════════════════════════════════════

class InteractiveShell:
    """Interactive shell for ThreatWinds Pentest CLI."""

    def __init__(self):
        self.console = Console()
        self.running = True
        self.watch_manager = WatchManager(self.console)
        self.last_pentest_id = None
        self.input_mode = "command"  # 'command' or 'freeform'
        self.webui_process: Optional[subprocess.Popen] = None

        # Setup history directory
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Create prompt session with all enhancements
        # Note: mouse_support=False to allow normal text selection/copying in terminal
        self.session = PromptSession(
            history=FileHistory(str(HISTORY_FILE)),
            auto_suggest=AutoSuggestFromHistory(),
            completer=TWPTCompleter(self),
            lexer=TWPTLexer(),
            style=PROMPT_STYLE,
            complete_while_typing=True,
            enable_history_search=True,
            mouse_support=False,
            complete_in_thread=True,
        )

        # Build command handlers
        self.command_handlers = self._build_command_handlers()

    def _build_command_handlers(self) -> Dict[str, callable]:
        return {
            "run": self.cmd_run,
            "get": self.cmd_get,
            "download": self.cmd_download,
            "list": self.cmd_list,
            "watch": self.cmd_watch,
            "stop": self.cmd_stop,
            "hint": self.cmd_hint,
            "chat": self.cmd_chat,
            "init": self.cmd_init,
            "configure": self.cmd_configure,
            "status": self.cmd_status,
            "update": self.cmd_update,
            "uninstall": self.cmd_uninstall,
            "version": self.cmd_version,
            "webui": self.cmd_webui,
            "stopweb": self.cmd_stopweb,
            "help": self.cmd_help,
            "clear": self.cmd_clear,
            "exit": self.cmd_exit,
            "quit": self.cmd_exit,
            "q": self.cmd_exit,
            "task": self.cmd_task,
            "plan": self.cmd_plan,
            "memory": self.cmd_memory,
            "done": self.cmd_done,  # No-op - handles leftover "done" from guided mode
        }

    def get_input_separator(self) -> str:
        """Get the visual separator line above the input area."""
        try:
            width = os.get_terminal_size().columns
        except OSError:
            width = 80

        # Create separator with context hint
        if self.watch_manager.is_watching():
            hint = " Type to add instructions • 'stop' to go back "
        else:
            hint = " Enter command or describe task "

        # Calculate padding
        hint_len = len(hint)
        if width > hint_len + 4:
            left_pad = (width - hint_len) // 2
            right_pad = width - hint_len - left_pad
            separator = "─" * left_pad + hint + "─" * right_pad
        else:
            separator = "─" * width

        return separator

    def get_prompt(self) -> FormattedText:
        """Build the formatted prompt with visual separator."""
        from twpt_cli.config import IS_KALI_LINUX

        endpoint_config = load_endpoint_config()
        creds = load_credentials()

        parts = []

        # Add separator line above prompt
        separator = self.get_input_separator()
        parts.append(('class:input-separator', separator))
        parts.append(('', '\n'))

        # App name
        parts.append(('class:prompt', 'twpt'))
        parts.append(('class:prompt.bracket', ' ['))

        # Endpoint status
        if endpoint_config and endpoint_config.get("use_remote"):
            host = endpoint_config.get("api_host", "?")
            parts.append(('class:prompt.status', host))
        elif IS_KALI_LINUX:
            parts.append(('class:prompt.status.warning', 'local'))
        else:
            parts.append(('class:prompt.status.error', 'no server'))

        parts.append(('', ' '))

        # Auth status
        if creds:
            parts.append(('class:prompt.status', '●'))
        else:
            parts.append(('class:prompt.status.error', '●'))

        # Watch indicator
        if self.watch_manager.is_watching():
            parts.append(('', ' '))
            # Use truncate_pentest_id for consistent display of both UUID and friendly IDs
            display_id = truncate_pentest_id(self.watch_manager.watching_pentest_id, max_length=16)
            parts.append(('class:prompt.status', f'◉ {display_id}'))

        parts.append(('class:prompt.bracket', ']'))
        parts.append(('class:prompt.arrow', ' ❯ '))

        return FormattedText(parts)


    def parse_command(self, line: str) -> tuple:
        if not line.strip():
            return None, []

        try:
            parts = shlex.split(line)
        except ValueError as e:
            self.console.print(f"[red]Parse error: {e}[/red]")
            return None, []

        if not parts:
            return None, []

        return parts[0].lower(), parts[1:]

    def _is_natural_language_input(self, cmd: str, args: List[str], full_line: str) -> bool:
        """
        Detect if the input appears to be natural language rather than command syntax.

        Uses keyword-based heuristics and regex patterns to detect targets vs text.

        Examples that SHOULD be detected as natural language:
        - "run a pentest on example.com" → natural language (has "a")
        - "run port scan on example.com" → natural language ("run port" isn't valid)
        - "do a subdomain discovery" → natural language
        - "scan example.com for vulnerabilities" → natural language
        - "check if port 443 is open" → natural language

        Examples that are proper commands:
        - "run example.com" → command (run + target)
        - "run example.com --safe" → command
        - "list" → command
        - "get abc-123" → command
        - "watch abc-123" → command

        Returns:
            True if this looks like natural language, False if it's command syntax
        """
        import re

        if not cmd:
            return False

        # Commands that are not ambiguous - never natural language (fast path)
        unambiguous_commands = {
            'list', 'get', 'download', 'watch', 'stop', 'chat', 'init',
            'configure', 'status', 'update', 'uninstall', 'version',
            'webui', 'stopweb', 'help', 'clear', 'exit', 'quit', 'q', 'task',
            'done'
        }

        if cmd in unambiguous_commands:
            return False

        # Regex patterns for targets
        # Domain: example.com, sub.example.com, example.co.uk
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$'
        # IP address: 192.168.1.1, 10.0.0.1
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}(/\d{1,2})?$'
        # URL: http://example.com, https://test.org/path
        url_pattern = r'^https?://'

        # Natural language indicators (filler words)
        nl_indicators = {
            'a', 'an', 'the', 'on', 'for', 'if', 'is', 'are', 'what',
            'how', 'please', 'can', 'could', 'would', 'should', 'let',
            'me', 'my', 'this', 'that', 'some', 'any', 'all', 'using',
            'with', 'against', 'from', 'into', 'about', 'and', 'or'
        }

        # Check if first argument is a natural language indicator
        if args and args[0].lower() in nl_indicators:
            return True

        # For "run" command specifically
        if cmd == 'run':
            if not args:
                return False  # Just "run" - treat as command

            first_arg = args[0]

            # Check if first arg looks like a target using regex
            if re.match(domain_pattern, first_arg):
                return False  # It's a domain
            if re.match(ip_pattern, first_arg):
                return False  # It's an IP
            if re.match(url_pattern, first_arg):
                return False  # It's a URL

            # If first arg is a common action word, it's natural language
            action_words = {
                'a', 'an', 'the', 'port', 'full', 'quick', 'deep', 'simple',
                'pentest', 'scan', 'test', 'check', 'audit', 'assessment',
                'vulnerability', 'security', 'network', 'web', 'subdomain'
            }
            if first_arg.lower() in action_words:
                return True

        # Sentence starters that are almost always natural language
        sentence_starters = {'do', 'scan', 'check', 'find', 'test', 'perform', 'execute', 'start'}
        if cmd in sentence_starters:
            return True

        # Check for conversational patterns in the full line
        conversational_patterns = [
            r'\s+a\s+', r'\s+an\s+', r'\s+the\s+', r'\s+on\s+', r'\s+for\s+', r'\s+if\s+',
            r'\s+me\s+', r'\s+my\s+', r'\s+please\b', r'\s+can\s+you', r'\s+could\s+you',
            r'\s+i\s+want', r'\s+i\s+need', r"let's", r'\s+using\s+', r'\s+with\s+'
        ]
        full_lower = f" {full_line.lower()} "
        for pattern in conversational_patterns:
            if re.search(pattern, full_lower):
                return True

        return False

    def run(self):
        """Run the interactive shell."""
        self.show_banner()

        while self.running:
            try:
                line = self.session.prompt(
                    self.get_prompt(),
                )

                if not line:
                    continue

                cmd, args = self.parse_command(line)

                if not cmd:
                    continue

                # When watching, treat most input as context injection
                if self.watch_manager.is_watching():
                    # Only these commands work while watching
                    if cmd in ['stop', 'q', 'quit', 'exit']:
                        if cmd == 'stop':
                            self.watch_manager.stop_watch()
                        else:
                            self.watch_manager.stop_watch(silent=True)
                            self.cmd_exit([])
                    else:
                        # Everything else is a context injection hint
                        self._inject_context_hint(line)
                    continue

                # Normal command processing when not watching
                # Detect if this looks like natural language vs a proper command
                if self._is_natural_language_input(cmd, args, line):
                    # Natural language - interpret with AI
                    self._handle_freeform_input(line)
                elif cmd in self.command_handlers:
                    # Proper command syntax
                    self.command_handlers[cmd](args)
                else:
                    # Not a recognized command - treat as a custom task request
                    self._handle_freeform_input(line)

            except KeyboardInterrupt:
                if self.watch_manager.is_watching():
                    self.watch_manager.stop_watch()
                else:
                    self.console.print()
            except EOFError:
                self.cmd_exit([])
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")

    def _inject_context_hint(self, line: str):
        """Inject a context hint into the running pentest.

        Called when user types anything while watching a pentest.
        Supports priority prefixes: ! for HIGH, !! for IMMEDIATE.

        Args:
            line: The user's input line
        """
        pentest_id = self.watch_manager.watching_pentest_id
        if not pentest_id:
            return

        # Parse priority from prefix
        priority = "NORMAL"
        hint_text = line.strip()

        if hint_text.startswith("!!"):
            priority = "IMMEDIATE"
            hint_text = hint_text[2:].strip()
        elif hint_text.startswith("!"):
            priority = "HIGH"
            hint_text = hint_text[1:].strip()

        if not hint_text:
            return

        # Send the hint via gRPC
        try:
            import asyncio
            from twpt_cli.config import load_credentials, get_grpc_endpoint
            from twpt_cli.sdk import GRPCClient

            creds = load_credentials()
            if not creds:
                self.console.print("[red]Not configured[/red]")
                return

            async def send_hint():
                client = GRPCClient(get_grpc_endpoint(), creds)
                try:
                    await client.connect()

                    # Create inject context request
                    inject_request = client.create_inject_context_request(
                        pentest_id=pentest_id,
                        context=hint_text,
                        priority=priority
                    )

                    # Use the interactive stream to send the request and get response
                    request_queue, response_stream, cleanup = await client.subscribe_pentest_stream_interactive(
                        pentest_id, include_history=False
                    )

                    # Send the inject request
                    await request_queue.put(inject_request)

                    # Wait for acknowledgement
                    try:
                        async for response in response_stream:
                            if response.get('type') == 'context_ack':
                                if response.get('accepted'):
                                    self.console.print(
                                        f"[green]→ Hint sent ({priority})[/green]"
                                    )
                                else:
                                    self.console.print(
                                        f"[yellow]✗ {response.get('message', 'Rejected')}[/yellow]"
                                    )
                                break
                            elif response.get('type') == 'error':
                                self.console.print(f"[red]Error: {response.get('error', '')}[/red]")
                                break
                            elif response.get('type') == 'subscribe_response':
                                continue
                    except asyncio.TimeoutError:
                        self.console.print(f"[green]→ Hint sent ({priority})[/green]")

                    await cleanup()

                finally:
                    await client.close()

            asyncio.run(send_hint())

        except Exception as e:
            self.console.print(f"[red]Failed to send hint: {e}[/red]")

    def show_banner(self):
        """Show the shell banner."""
        banner = """
[bold cyan]╔══════════════════════════════════════════════════╗[/bold cyan]
[bold cyan]║[/bold cyan]  [bold white]ThreatWinds Pentest CLI[/bold white]                         [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]  [dim]Version {version}[/dim]{padding}[bold cyan]║[/bold cyan]
[bold cyan]╚══════════════════════════════════════════════════╝[/bold cyan]
""".format(version=__version__, padding=" " * (38 - len(__version__)))

        self.console.print(banner)
        self.console.print("[dim]  Tab[/dim] autocomplete  [dim]•[/dim]  [dim]↑↓[/dim] history  [dim]•[/dim]  [dim]help[/dim] commands")
        self.console.print()

    # ═══════════════════════════════════════════════════════════════════════════
    # Command Implementations
    # ═══════════════════════════════════════════════════════════════════════════

    def cmd_run(self, args: List[str]):
        """Run a new pentest."""
        if not args:
            self.console.print("[red]Error: Target required[/red]")
            self.console.print("[dim]Usage: run <target> [--safe] [--no-exploit] [--watch] [--scope holistic|targeted] [--plan <name>] [-m <memory>][/dim]")
            return

        has_watch = "--watch" in args

        try:
            cli_args = []

            if "--config-file" in args:
                idx = args.index("--config-file")
                if idx + 1 < len(args):
                    cli_args.extend(["--config-file", args[idx + 1]])
            else:
                # Extract target - first non-flag argument
                target = None
                for i, arg in enumerate(args):
                    if not arg.startswith("-") and not arg.startswith("@"):
                        # Check if previous arg was a flag that takes a value
                        if i > 0 and args[i-1] in ["--plan", "--scope", "-m", "--memory"]:
                            continue
                        target = arg
                        break

                if not target:
                    self.console.print("[red]Error: Target required[/red]")
                    return

                cli_args.extend(["--target", target])

            if "--safe" in args:
                cli_args.append("--safe")
            if "--no-exploit" in args:
                cli_args.append("--no-exploit")
            if "--no-default-memory" in args:
                cli_args.append("--no-default-memory")
            if has_watch:
                cli_args.append("--watch")

            # Handle --plan option
            if "--plan" in args:
                idx = args.index("--plan")
                if idx + 1 < len(args):
                    cli_args.extend(["--plan", args[idx + 1]])

            # Handle --scope option
            if "--scope" in args:
                idx = args.index("--scope")
                if idx + 1 < len(args):
                    cli_args.extend(["--scope", args[idx + 1]])

            # Handle memory options (-m and --memory) - can appear multiple times
            i = 0
            while i < len(args):
                if args[i] in ["-m", "--memory"]:
                    if i + 1 < len(args):
                        cli_args.extend(["-m", args[i + 1]])
                        i += 2
                    else:
                        i += 1
                else:
                    i += 1

            if has_watch:
                cmd = [sys.executable, "-m", "twpt_cli.main", "run"] + cli_args
                try:
                    subprocess.run(cmd, check=False)
                except KeyboardInterrupt:
                    self.console.print("\n[yellow]Interrupted[/yellow]")
            else:
                from click.testing import CliRunner
                runner = CliRunner()
                result = runner.invoke(schedule_pentest.schedule_pentest, cli_args, catch_exceptions=False)

                if result.output:
                    sys.stdout.write(result.output)
                    sys.stdout.flush()

        except SystemExit:
            pass
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def cmd_get(self, args: List[str]):
        """Get pentest details."""
        if not args:
            if self.last_pentest_id:
                pentest_id = self.last_pentest_id
                self.console.print(f"[dim]Using last pentest: {pentest_id}[/dim]")
            else:
                self.console.print("[red]Error: Pentest ID required[/red]")
                return
        else:
            pentest_id = args[0]
            self.last_pentest_id = pentest_id

        try:
            from click.testing import CliRunner
            runner = CliRunner()
            result = runner.invoke(get_pentest.get_pentest, [pentest_id], catch_exceptions=False)

            if result.output:
                sys.stdout.write(result.output)
                sys.stdout.flush()

        except SystemExit:
            pass
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def cmd_download(self, args: List[str]):
        """Download pentest evidence."""
        if not args:
            if self.last_pentest_id:
                pentest_id = self.last_pentest_id
                self.console.print(f"[dim]Using last pentest: {pentest_id}[/dim]")
            else:
                self.console.print("[red]Error: Pentest ID required[/red]")
                return
        else:
            pentest_id = args[0]
            self.last_pentest_id = pentest_id

        cli_args = [pentest_id]

        if "--output" in args:
            idx = args.index("--output")
            if idx + 1 < len(args):
                cli_args.extend(["--output", args[idx + 1]])

        if "--no-extract" in args:
            cli_args.append("--no-extract")

        try:
            from click.testing import CliRunner
            runner = CliRunner()
            result = runner.invoke(download_evidence.download_evidence, cli_args, catch_exceptions=False)

            if result.output:
                sys.stdout.write(result.output)
                sys.stdout.flush()

        except SystemExit:
            pass
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def cmd_list(self, args: List[str]):
        """List recent pentests (both autonomous and guided)."""
        page = 1
        page_size = 5

        for i, arg in enumerate(args):
            if arg == "--page" and i + 1 < len(args):
                try:
                    page = int(args[i + 1])
                except ValueError:
                    self.console.print("[red]Invalid page number[/red]")
                    return
            elif arg == "--page-size" and i + 1 < len(args):
                try:
                    page_size = int(args[i + 1])
                except ValueError:
                    self.console.print("[red]Invalid page size[/red]")
                    return
            elif arg == "--all":
                page_size = 100

        creds = load_credentials()
        if not creds:
            self.console.print("[red]Not configured. Run: configure[/red]")
            return

        try:
            from twpt_cli.sdk import HTTPClient
            client = HTTPClient(get_api_endpoint(), creds)
            response = client.list_pentests(page=page, page_size=page_size)

            self.console.print()
            self.console.print("[bold cyan]Recent Pentests[/bold cyan]")
            self.console.print("─" * 100)

            if not response.pentests:
                self.console.print("[dim]No pentests found[/dim]")
                return

            # Table with Mode column
            table = Table(show_header=True, header_style="bold cyan", box=None, padding=(0, 1))
            table.add_column("ID", style="white", no_wrap=True)
            table.add_column("Mode", style="white", width=8)
            table.add_column("Status", style="white")
            table.add_column("Target", style="white")
            table.add_column("Findings", justify="center")
            table.add_column("Severity", justify="center")

            status_colors = {"PENDING": "yellow", "IN_PROGRESS": "blue", "COMPLETED": "green", "FAILED": "red"}
            severity_colors = {"CRITICAL": "red bold", "HIGH": "red", "MEDIUM": "yellow", "LOW": "blue", "NONE": "dim"}
            mode_colors = {"AUTONOMOUS": "dim", "GUIDED": "magenta"}

            for pentest in response.pentests:
                status_style = status_colors.get(pentest.status, "white")
                severity_style = severity_colors.get(pentest.severity, "white")

                # Get mode - default to AUTONOMOUS for older pentests
                mode = getattr(pentest, 'mode', None) or "AUTO"
                if mode == "AUTONOMOUS":
                    mode_display = "[dim]AUTO[/dim]"
                elif mode == "GUIDED":
                    mode_display = "[magenta]GUIDED[/magenta]"
                else:
                    mode_display = "[dim]AUTO[/dim]"

                if pentest.targets and len(pentest.targets) > 0:
                    target_names = [t.target for t in pentest.targets]
                    target = target_names[0][:20] if len(target_names) == 1 else f"{len(target_names)}x"
                else:
                    target = "-"

                table.add_row(
                    pentest.id,
                    mode_display,
                    f"[{status_style}]{pentest.status}[/{status_style}]",
                    target,
                    str(pentest.findings),
                    f"[{severity_style}]{pentest.severity}[/{severity_style}]",
                )

            self.console.print(table)

            if response.total_pages > 1:
                self.console.print(f"\n[dim]Page {response.page}/{response.total_pages} • Total: {response.total}[/dim]")

            self.console.print("\n[dim]get <id>[/dim] details  •  [dim]watch <id>[/dim] monitor  •  [dim]download <id>[/dim] evidence")
            self.console.print()

        except Exception as e:
            self.console.print(f"[red]Failed to list pentests: {e}[/red]")

    def _get_latest_pentest_id(self) -> str:
        """Get the latest pentest ID (in-progress first, then completed)."""
        try:
            from twpt_cli.config import load_credentials, get_api_endpoint
            from twpt_cli.sdk import HTTPClient

            creds = load_credentials()
            if not creds:
                return None

            client = HTTPClient(get_api_endpoint(), creds)
            response = client.list_pentests(page=1, page_size=10)

            if not response.pentests:
                return None

            # Prefer in-progress pentests
            for p in response.pentests:
                if p.status == "IN_PROGRESS":
                    return p.id

            # Fall back to most recent
            return response.pentests[0].id

        except Exception:
            return None

    def cmd_watch(self, args: List[str]):
        """Watch a running pentest stream."""
        if not args:
            # Try to auto-detect the latest pentest
            pentest_id = self._get_latest_pentest_id()
            if pentest_id:
                self.console.print(f"[dim]Auto-selected: {pentest_id}[/dim]")
            elif self.last_pentest_id:
                pentest_id = self.last_pentest_id
                self.console.print(f"[dim]Using last pentest: {pentest_id}[/dim]")
            else:
                self.console.print("[red]Error: No pentest found. Provide an ID.[/red]")
                return
        else:
            pentest_id = args[0]
        self.last_pentest_id = pentest_id

        cli_args = []
        if "--no-history" in args:
            cli_args.append("--no-history")
        if "--quiet" in args or "-q" in args:
            cli_args.append("--quiet")

        self.console.print(f"\n[cyan]Starting watch for pentest {pentest_id}...[/cyan]")
        self.console.print("[dim]Type hints to guide the AI agent. Use 'stop' or 'quit' to exit.[/dim]")
        self.console.print("[dim]Prefix with ! for HIGH priority, !! for IMMEDIATE.[/dim]\n")

        self.watch_manager.start_watch(pentest_id, cli_args)

    def cmd_stop(self, args: List[str]):
        """Stop watching current pentest."""
        if self.watch_manager.is_watching():
            self.watch_manager.stop_watch()
        else:
            self.console.print("[dim]No active watch[/dim]")

    def cmd_hint(self, args: List[str]):
        """Inject a hint/context into the running pentest.

        This sends a context injection request to the pt-agent, which will
        incorporate the hint into the AI agent's reasoning at the next step.
        """
        # Check if we have a pentest to target
        pentest_id = None
        if self.watch_manager.is_watching():
            pentest_id = self.watch_manager.watching_pentest_id
        elif self.last_pentest_id:
            pentest_id = self.last_pentest_id
        else:
            self.console.print("[red]Error: No active pentest. Use 'watch <id>' first or run a pentest.[/red]")
            return

        if not args:
            self.console.print("[red]Error: Hint text required[/red]")
            self.console.print("[dim]Usage: hint [--high|--immediate] <hint text>[/dim]")
            return

        # Parse priority flags
        priority = "NORMAL"
        hint_parts = []
        for arg in args:
            if arg == "--high":
                priority = "HIGH"
            elif arg == "--immediate":
                priority = "IMMEDIATE"
            else:
                hint_parts.append(arg)

        hint_text = " ".join(hint_parts)
        if not hint_text:
            self.console.print("[red]Error: Hint text required[/red]")
            return

        # Send the hint via gRPC
        try:
            import asyncio
            from twpt_cli.config import load_credentials, get_grpc_endpoint
            from twpt_cli.sdk import GRPCClient

            creds = load_credentials()
            if not creds:
                self.console.print("[red]Not configured. Please run: configure[/red]")
                return

            async def send_hint():
                client = GRPCClient(get_grpc_endpoint(), creds)
                try:
                    await client.connect()

                    # Create inject context request
                    inject_request = client.create_inject_context_request(
                        pentest_id=pentest_id,
                        context=hint_text,
                        priority=priority
                    )

                    # Use the interactive stream to send the request and get response
                    request_queue, response_stream, cleanup = await client.subscribe_pentest_stream_interactive(
                        pentest_id, include_history=False
                    )

                    # Send the inject request
                    await request_queue.put(inject_request)

                    # Wait for acknowledgement (with timeout)
                    try:
                        async for response in response_stream:
                            if response.get('type') == 'context_ack':
                                if response.get('accepted'):
                                    self.console.print(
                                        f"[green]✓ Hint accepted ({priority}): {response.get('message', '')}[/green]"
                                    )
                                else:
                                    self.console.print(
                                        f"[yellow]✗ Hint rejected: {response.get('message', '')}[/yellow]"
                                    )
                                break
                            elif response.get('type') == 'error':
                                self.console.print(f"[red]Error: {response.get('error', '')}[/red]")
                                break
                            # Skip other responses (subscribe_response, etc.)
                            if response.get('type') == 'subscribe_response':
                                continue
                    except asyncio.TimeoutError:
                        self.console.print("[yellow]Hint sent (no acknowledgement received)[/yellow]")

                    await cleanup()

                finally:
                    await client.close()

            asyncio.run(send_hint())

        except Exception as e:
            self.console.print(f"[red]Failed to send hint: {e}[/red]")

    def cmd_chat(self, args: List[str]):
        """Chat with AI about a pentest."""
        if not args:
            if self.last_pentest_id:
                pentest_id = self.last_pentest_id
                self.console.print(f"[dim]Using last pentest: {pentest_id}[/dim]")
            else:
                self.console.print("[red]Error: Pentest ID required[/red]")
                return
        else:
            pentest_id = args[0]
            self.last_pentest_id = pentest_id

        interactive = "-i" in args or "--interactive" in args

        question_parts = [arg for arg in args[1:] if arg not in ["-i", "--interactive"]]
        question = " ".join(question_parts) if question_parts else None

        cli_args = [pentest_id]
        if interactive:
            cli_args.append("--interactive")
        elif question:
            cli_args.append(question)
        else:
            cli_args.append("--interactive")

        cmd = [sys.executable, "-m", "twpt_cli.main", "chat"] + cli_args

        try:
            subprocess.run(cmd, check=False)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Chat ended[/yellow]")

    def cmd_init(self, args: List[str]):
        """Initialize remote endpoint configuration."""
        try:
            from click.testing import CliRunner
            runner = CliRunner()

            if "--local" in args:
                result = runner.invoke(init.init, ["--local"], catch_exceptions=False)
            elif len(args) >= 2:
                cli_args = []
                non_flags = [a for a in args if not a.startswith("--")]

                if len(non_flags) >= 1:
                    cli_args.extend(["--host", non_flags[0]])
                if len(non_flags) >= 2:
                    cli_args.extend(["--api-port", non_flags[1]])
                if len(non_flags) >= 3:
                    cli_args.extend(["--grpc-port", non_flags[2]])
                if "--skip-test" in args:
                    cli_args.append("--skip-test")

                result = runner.invoke(init.init, cli_args, catch_exceptions=False, input="\n\n")
            else:
                self.console.print("[red]Error: Invalid arguments[/red]")
                self.console.print("[dim]Usage: init <host> <port> | init --local[/dim]")
                return

            if result.output:
                sys.stdout.write(result.output)
                sys.stdout.flush()

        except SystemExit:
            pass
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def cmd_configure(self, args: List[str]):
        """Configure API credentials."""
        from prompt_toolkit import prompt as pt_prompt

        self.console.print()
        api_key = pt_prompt(FormattedText([('class:prompt', 'API Key: ')]), style=PROMPT_STYLE)
        api_secret = pt_prompt(FormattedText([('class:prompt', 'API Secret: ')]), is_password=True, style=PROMPT_STYLE)

        try:
            from click.testing import CliRunner
            runner = CliRunner()

            cli_args = ["--api-key", api_key, "--api-secret", api_secret]
            if "--skip-docker" in args:
                cli_args.append("--skip-docker")

            result = runner.invoke(configure.configure, cli_args, catch_exceptions=False)

            if result.output:
                sys.stdout.write(result.output)
                sys.stdout.flush()

        except SystemExit:
            pass
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def cmd_status(self, args: List[str]):
        """Show current configuration status."""
        from twpt_cli.config import IS_KALI_LINUX

        self.console.print()
        self.console.print("[bold cyan]Configuration Status[/bold cyan]")
        self.console.print("─" * 45)

        creds = load_credentials()
        endpoint_config = load_endpoint_config()

        # Credentials
        if creds:
            self.console.print("  [green]●[/green] API Credentials: [green]Configured[/green]")
        else:
            self.console.print("  [red]●[/red] API Credentials: [red]Not configured[/red]")

        # Endpoint
        if endpoint_config and endpoint_config.get("use_remote"):
            endpoint = f"{endpoint_config['api_host']}:{endpoint_config['api_port']}"
            self.console.print(f"  [green]●[/green] Server: [green]Remote[/green] ({endpoint})")
        else:
            mode_label = "Local Agent" if IS_KALI_LINUX else "Not configured"
            color = "yellow" if IS_KALI_LINUX else "red"
            self.console.print(f"  [{color}]●[/{color}] Server: [{color}]{mode_label}[/{color}]")

        self.console.print(f"  [dim]   API:  {get_api_endpoint()}[/dim]")
        self.console.print(f"  [dim]   gRPC: {get_grpc_endpoint()}[/dim]")

        if self.watch_manager.is_watching():
            self.console.print(f"  [cyan]●[/cyan] Watching: [cyan]{self.watch_manager.watching_pentest_id}[/cyan]")

        self.console.print()

    def cmd_update(self, args: List[str]):
        """Update the pentest toolkit."""
        try:
            from click.testing import CliRunner
            runner = CliRunner()

            cli_args = ["--force"] if "--force" in args else []
            result = runner.invoke(update.update_latest, cli_args, catch_exceptions=False)

            if result.output:
                sys.stdout.write(result.output)
                sys.stdout.flush()

        except SystemExit:
            pass
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def cmd_uninstall(self, args: List[str]):
        """Uninstall the pentest toolkit."""
        from prompt_toolkit import prompt as pt_prompt

        confirm = pt_prompt(
            FormattedText([('class:prompt.status.warning', 'Uninstall? (y/N): ')]),
            style=PROMPT_STYLE
        )

        if confirm.lower() == 'y':
            try:
                from click.testing import CliRunner
                runner = CliRunner()

                cli_args = ["--yes"]
                if "--remove-data" in args:
                    cli_args.append("--remove-data")

                result = runner.invoke(uninstall.uninstall, cli_args, catch_exceptions=False)

                if result.output:
                    sys.stdout.write(result.output)
                    sys.stdout.flush()

            except SystemExit:
                pass
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
        else:
            self.console.print("[dim]Cancelled[/dim]")

    def cmd_version(self, args: List[str]):
        """Show version information."""
        try:
            from click.testing import CliRunner
            runner = CliRunner()

            cli_args = ["--detailed"] if ("--detailed" in args or "-d" in args) else []
            result = runner.invoke(version_cmd.version, cli_args, catch_exceptions=False)

            if result.output:
                sys.stdout.write(result.output)
                sys.stdout.flush()

        except SystemExit:
            pass
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def cmd_webui(self, args: List[str]):
        """Launch the web-based interface in background."""
        host = "0.0.0.0"
        port = 8080
        debug = "--debug" in args or "-d" in args

        for i, arg in enumerate(args):
            if arg == "--host" and i + 1 < len(args):
                host = args[i + 1]
            elif arg == "--port" and i + 1 < len(args):
                try:
                    port = int(args[i + 1])
                except ValueError:
                    self.console.print("[red]Invalid port number[/red]")
                    return

        cli_args = ["--host", host, "--port", str(port)]
        if debug:
            cli_args.append("--debug")

        cmd = [sys.executable, "-m", "twpt_cli.main", "webui"] + cli_args

        try:
            # Start webui in background (detached from shell)
            self.webui_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            self.console.print()
            self.console.print("[green]Web UI started in background[/green]")
            self.console.print(f"  Advanced UI:   [cyan]http://{host}:{port}/[/cyan]")
            self.console.print(f"  Simplified UI: [cyan]http://{host}:{port}/simple[/cyan]")
            self.console.print()
            self.console.print("[dim]Use 'stopweb' to stop the server[/dim]")
            self.console.print()
        except Exception as e:
            self.console.print(f"[red]Failed to start Web UI: {e}[/red]")

    def cmd_stopweb(self, args: List[str]):
        """Stop the background web UI server."""
        if self.webui_process is None or self.webui_process.poll() is not None:
            self.console.print("[dim]No web UI server running[/dim]")
            return

        try:
            self.webui_process.terminate()
            self.webui_process.wait(timeout=5)
            self.console.print("[green]Web UI server stopped[/green]")
        except subprocess.TimeoutExpired:
            self.webui_process.kill()
            self.console.print("[yellow]Web UI server killed[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Failed to stop Web UI: {e}[/red]")
        finally:
            self.webui_process = None

    def cmd_help(self, args: List[str]):
        """Show help information."""
        if args:
            cmd_name = args[0].lower()
            if cmd_name in COMMANDS:
                info = COMMANDS[cmd_name]
                self.console.print()
                self.console.print(f"[bold cyan]{cmd_name}[/bold cyan] - {info['help']}")

                # Usage
                usage_parts = [cmd_name] + info.get('args', [])
                if info.get('options'):
                    usage_parts.append('[options]')
                self.console.print(f"[dim]Usage: {' '.join(usage_parts)}[/dim]")

                # Options
                if info.get('options'):
                    self.console.print("\n[yellow]Options:[/yellow]")
                    for opt, desc in info['options'].items():
                        self.console.print(f"  [cyan]{opt:18}[/cyan] {desc}")

                # Examples
                if info.get('examples'):
                    self.console.print("\n[yellow]Examples:[/yellow]")
                    for example in info['examples']:
                        self.console.print(f"  [dim]{example}[/dim]")

                self.console.print()
            else:
                self.console.print(f"[red]Unknown command: {cmd_name}[/red]")
        else:
            self.console.print()
            self.console.print("[bold cyan]ThreatWinds Pentest CLI - Commands[/bold cyan]")
            self.console.print("─" * 60)

            categories = {
                "Pentest": ["run", "get", "download", "list"],
                "Playbooks": ["plan"],
                "Memory": ["memory"],
                "Custom Tasks": ["task"],
                "Monitor": ["watch", "stop", "hint", "chat"],
                "Config": ["init", "configure", "status"],
                "System": ["update", "uninstall", "version", "webui", "stopweb"],
                "Shell": ["help", "clear", "exit"],
            }

            for cat, cmds in categories.items():
                self.console.print(f"\n[yellow]{cat}[/yellow]")
                for cmd in cmds:
                    if cmd in COMMANDS:
                        info = COMMANDS[cmd]
                        self.console.print(f"  [bold white]{cmd:12}[/bold white] {info['help']}")

            # Quick tips section
            self.console.print()
            self.console.print("[cyan]─" * 60 + "[/cyan]")
            self.console.print("[bold cyan]Quick Tips[/bold cyan]")
            self.console.print()
            self.console.print("  [yellow]Playbooks:[/yellow] Custom pentest plans in [white]playbooks/[/white] folder")
            self.console.print("    [dim]plan edit web-audit[/dim]  •  [dim]run target --plan web-audit[/dim]")
            self.console.print()
            self.console.print("  [yellow]Memory:[/yellow] Context notes in [white]memory/[/white] folder")
            self.console.print("    [dim]memory edit default[/dim]  •  [dim]run target -m @name[/dim]  •  [dim]run target -m \"text\"[/dim]")
            self.console.print("    [white]@name[/white] = load file  •  [white]\"text\"[/white] = inline  •  [white]default.md[/white] = auto-included")
            self.console.print()
            self.console.print("[dim]help <command>[/dim] for details  •  [dim]Tab[/dim] for autocomplete")
            self.console.print()

    def cmd_clear(self, args: List[str]):
        """Clear the screen."""
        os.system('clear' if os.name == 'posix' else 'cls')

    def cmd_done(self, args: List[str]):
        """No-op command - handles 'done' typed at main prompt after guided mode ends."""
        pass

    def cmd_exit(self, args: List[str]):
        """Exit the shell."""
        if self.watch_manager.is_watching():
            self.watch_manager.stop_watch(silent=True)

        # Stop webui if running
        if self.webui_process is not None and self.webui_process.poll() is None:
            try:
                self.webui_process.terminate()
                self.webui_process.wait(timeout=2)
            except Exception:
                try:
                    self.webui_process.kill()
                except Exception:
                    pass
            self.console.print("[dim]Web UI server stopped[/dim]")

        self.console.print("[cyan]Goodbye![/cyan]")
        self.running = False

    def cmd_task(self, args: List[str]):
        """Run a custom pentesting task."""
        # Handle --list
        if "--list" in args:
            cmd = [sys.executable, "-m", "twpt_cli.main", "task", "--list"]
            try:
                subprocess.run(cmd, check=False)
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Interrupted[/yellow]")
            return

        # Handle --close
        if "--close" in args:
            idx = args.index("--close")
            if idx + 1 < len(args):
                task_id = args[idx + 1]
                cmd = [sys.executable, "-m", "twpt_cli.main", "task", "--close", task_id]
                try:
                    subprocess.run(cmd, check=False)
                except KeyboardInterrupt:
                    self.console.print("\n[yellow]Interrupted[/yellow]")
            else:
                self.console.print("[red]Error: Task ID required for --close[/red]")
            return

        # Extract target
        target = None
        session = None
        description_parts = []

        i = 0
        while i < len(args):
            if args[i] in ["--target", "-t"] and i + 1 < len(args):
                target = args[i + 1]
                i += 2
            elif args[i] in ["--session", "-s"] and i + 1 < len(args):
                session = args[i + 1]
                i += 2
            else:
                description_parts.append(args[i])
                i += 1

        description = " ".join(description_parts)

        if not description:
            self.console.print("[red]Error: Task description required[/red]")
            self.console.print("[dim]Usage: task \"port scan\" --target 192.168.1.1[/dim]")
            return

        if not target:
            # Try to extract target from description
            target = extract_target_from_text(description)
            if not target:
                self.console.print("[red]Error: Target required[/red]")
                self.console.print("[dim]Usage: task \"port scan\" --target 192.168.1.1[/dim]")
                return

        # Build command
        cmd = [sys.executable, "-m", "twpt_cli.main", "task", description, "--target", target]
        if session:
            cmd.extend(["--session", session])

        try:
            subprocess.run(cmd, check=False)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Task interrupted[/yellow]")

    def cmd_plan(self, args: List[str]):
        """Manage custom pentest plans.

        Usage:
            plan <file> --name <name>  Save a plan (shorthand)
            plan save <file> --name <name>  Save a plan from markdown file
            plan list [--tag <tag>]    List saved plans
            plan show <name>           Show plan details
            plan delete <name>         Delete a saved plan
            plan preview <file>        Preview a plan before saving

        Using plans with pentests:
            run <target> --plan <file>          Execute plan from file
            run <target> --plan saved:<name>    Execute saved plan

        Example workflow:
            1. plan ./my-plan.md --name "Web Audit" --tags web,audit
            2. plan list
            3. run example.com --plan saved:web-audit --watch
        """
        if not args:
            # Show plan help
            self._show_plan_help()
            return

        # Route to subcommand
        subcmd = args[0].lower()

        if subcmd == "save":
            self._plan_save(args[1:])
        elif subcmd == "list":
            self._plan_list(args[1:])
        elif subcmd == "show":
            self._plan_show(args[1:])
        elif subcmd == "delete":
            self._plan_delete(args[1:])
        elif subcmd == "preview":
            self._plan_preview(args[1:])
        elif subcmd.endswith('.md') or '/' in subcmd or subcmd.startswith('.'):
            # Looks like a file path - treat as shorthand for save
            self._plan_save(args)
        else:
            self.console.print(f"[red]Unknown plan subcommand: {subcmd}[/red]")
            self._show_plan_help()

    def _show_plan_help(self):
        """Show help for plan command."""
        self.console.print()
        self.console.print("[bold cyan]Custom Pentest Plans[/bold cyan]")
        self.console.print("─" * 40)
        self.console.print()
        self.console.print("[yellow]Manage:[/yellow]")
        self.console.print("  plan save <file> <name>    Save a plan")
        self.console.print("  plan list                  List saved plans")
        self.console.print("  plan show <name>           Show plan details")
        self.console.print("  plan delete <name>         Delete a plan")
        self.console.print()
        self.console.print("[yellow]Run:[/yellow]")
        self.console.print("  run <target> --plan <name>           Saved plan")
        self.console.print("  run <target> --plan file:<path>      From file")
        self.console.print()

    def _plan_save(self, args: List[str]):
        """Save a plan from a markdown file."""
        cmd = [sys.executable, "-m", "twpt_cli.main", "plan", "save"] + args
        try:
            subprocess.run(cmd, check=False)
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def _plan_list(self, args: List[str]):
        """List saved plans."""
        cmd = [sys.executable, "-m", "twpt_cli.main", "plan", "list"] + args
        try:
            subprocess.run(cmd, check=False)
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def _plan_show(self, args: List[str]):
        """Show plan details."""
        if not args:
            self.console.print("[red]Error: Plan name required[/red]")
            self.console.print("[dim]Usage: plan show <name> [--content][/dim]")
            return
        cmd = [sys.executable, "-m", "twpt_cli.main", "plan", "show"] + args
        try:
            subprocess.run(cmd, check=False)
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def _plan_delete(self, args: List[str]):
        """Delete a saved plan."""
        if not args:
            self.console.print("[red]Error: Plan name required[/red]")
            self.console.print("[dim]Usage: plan delete <name> [--force][/dim]")
            return
        cmd = [sys.executable, "-m", "twpt_cli.main", "plan", "delete"] + args
        try:
            subprocess.run(cmd, check=False)
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def _plan_preview(self, args: List[str]):
        """Preview a plan file."""
        if not args:
            self.console.print("[red]Error: File path required[/red]")
            self.console.print("[dim]Usage: plan preview <file>[/dim]")
            return
        cmd = [sys.executable, "-m", "twpt_cli.main", "plan", "preview"] + args
        try:
            subprocess.run(cmd, check=False)
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def cmd_memory(self, args: List[str]):
        """Manage pentest memory/context notes.

        Usage:
            memory init                  Initialize memory/ folder
            memory save <name> <content> Save a memory item
            memory list                  List saved memory items
            memory show <name>           Show memory item content
            memory delete <name>         Delete a memory item
            memory edit <name>           Open in editor
            memory path                  Show memory folder path

        Special:
            memory/default.md is auto-included in standard pentests.
        """
        if not args:
            self._show_memory_help()
            return

        subcmd = args[0].lower()

        if subcmd == "init":
            self._memory_init(args[1:])
        elif subcmd == "save":
            self._memory_save(args[1:])
        elif subcmd == "list":
            self._memory_list(args[1:])
        elif subcmd == "show":
            self._memory_show(args[1:])
        elif subcmd == "delete":
            self._memory_delete(args[1:])
        elif subcmd == "edit":
            self._memory_edit(args[1:])
        elif subcmd == "path":
            self._memory_path(args[1:])
        else:
            self.console.print(f"[red]Unknown memory subcommand: {subcmd}[/red]")
            self._show_memory_help()

    def _show_memory_help(self):
        """Show help for memory command."""
        self.console.print()
        self.console.print("[bold cyan]Pentest Memory/Context[/bold cyan]")
        self.console.print("─" * 50)
        self.console.print()
        self.console.print("[yellow]Commands:[/yellow]")
        self.console.print("  memory list                  List saved items")
        self.console.print("  memory edit <name>           Edit in $EDITOR")
        self.console.print("  memory show <name>           Show item content")
        self.console.print("  memory save <name> <text>    Save from command line")
        self.console.print("  memory delete <name>         Delete an item")
        self.console.print()
        self.console.print("[yellow]Default Memory:[/yellow]")
        self.console.print("  memory/default.md is AUTO-INCLUDED in standard pentests")
        self.console.print("  Edit it with: [white]memory edit default[/white]")
        self.console.print()
        self.console.print("[yellow]Using Memory with run:[/yellow]")
        self.console.print("  [white]@name[/white]  = Load saved file     [dim]run target -m @brute-force[/dim]")
        self.console.print("  [white]\"text\"[/white] = Inline context      [dim]run target -m \"Focus on SQLi\"[/dim]")
        self.console.print("  [dim]Combine: run target -m @creds -m \"Also check /admin\"[/dim]")
        self.console.print()

    def _memory_init(self, args: List[str]):
        """Initialize memory folder."""
        cmd = [sys.executable, "-m", "twpt_cli.main", "memory", "init"]
        try:
            subprocess.run(cmd, check=False)
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def _memory_save(self, args: List[str]):
        """Save a memory item."""
        if len(args) < 2:
            self.console.print("[red]Error: Name and content required[/red]")
            self.console.print("[dim]Usage: memory save <name> <content>[/dim]")
            return
        cmd = [sys.executable, "-m", "twpt_cli.main", "memory", "save"] + args
        try:
            subprocess.run(cmd, check=False)
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def _memory_list(self, args: List[str]):
        """List saved memory items."""
        cmd = [sys.executable, "-m", "twpt_cli.main", "memory", "list"]
        try:
            subprocess.run(cmd, check=False)
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def _memory_show(self, args: List[str]):
        """Show memory item content."""
        if not args:
            self.console.print("[red]Error: Memory name required[/red]")
            self.console.print("[dim]Usage: memory show <name>[/dim]")
            return
        cmd = [sys.executable, "-m", "twpt_cli.main", "memory", "show"] + args
        try:
            subprocess.run(cmd, check=False)
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def _memory_delete(self, args: List[str]):
        """Delete a memory item."""
        if not args:
            self.console.print("[red]Error: Memory name required[/red]")
            self.console.print("[dim]Usage: memory delete <name> [--force][/dim]")
            return
        cmd = [sys.executable, "-m", "twpt_cli.main", "memory", "delete"] + args
        try:
            subprocess.run(cmd, check=False)
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def _memory_edit(self, args: List[str]):
        """Edit a memory item in default editor."""
        if not args:
            self.console.print("[red]Error: Memory name required[/red]")
            self.console.print("[dim]Usage: memory edit <name>[/dim]")
            return
        cmd = [sys.executable, "-m", "twpt_cli.main", "memory", "edit"] + args
        try:
            subprocess.run(cmd, check=False)
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def _memory_path(self, args: List[str]):
        """Show memory folder path."""
        cmd = [sys.executable, "-m", "twpt_cli.main", "memory", "path"]
        try:
            subprocess.run(cmd, check=False)
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def _handle_freeform_input(self, line: str):
        """Handle freeform input by interpreting user intent.

        This implements intelligent command mapping:
        1. AI interprets the request
        2. If it maps to a built-in command → show and execute that command
        3. If it's a custom task → proceed with guided pentest flow
        """
        from prompt_toolkit import prompt as pt_prompt
        from rich.panel import Panel
        from rich.spinner import Spinner
        from rich.live import Live

        # Show thinking indicator
        self.console.print()
        with Live(Spinner("dots", text="Understanding your request..."), refresh_per_second=10, console=self.console):
            interpreted = interpret_request(line)

        if not interpreted:
            self.console.print("[red]Failed to interpret request. Please try again.[/red]")
            return

        # Check if this maps to a built-in command
        if interpreted.is_builtin_command and interpreted.maps_to_command:
            self._execute_mapped_command(interpreted)
            return

        # Otherwise, proceed with guided pentest flow for custom tasks
        self._handle_custom_task(interpreted)

    def _execute_mapped_command(self, interpreted):
        """Execute a built-in command that was mapped from natural language."""
        from prompt_toolkit import prompt as pt_prompt
        from rich.panel import Panel

        cmd = interpreted.maps_to_command
        args = interpreted.command_args or []
        flags = interpreted.command_flags or []

        # Build the command string for display
        cmd_display = cmd
        if args:
            cmd_display += " " + " ".join(args)
        if flags:
            cmd_display += " " + " ".join(flags)

        # Display what we understood
        self.console.print()
        self.console.print(Panel(
            f"[bold cyan]{interpreted.understood_request}[/bold cyan]",
            title="[yellow]Mapped to command[/yellow]",
            border_style="green"
        ))
        self.console.print(f"  [dim]Command:[/dim] [green]{cmd_display}[/green]")
        self.console.print(f"  [dim]Confidence:[/dim] [white]{interpreted.confidence}[/white]")
        self.console.print()

        # Ask for confirmation
        confirm = pt_prompt(
            FormattedText([('class:prompt', 'Execute? (Y/n): ')]),
            style=PROMPT_STYLE
        )

        if confirm.lower().strip() == 'n':
            self.console.print("[dim]Cancelled[/dim]")
            return

        # Execute the command
        handler = self.command_handlers.get(cmd)
        if handler:
            # Build args list with flags
            full_args = list(args) + list(flags)
            handler(full_args)
        else:
            self.console.print(f"[red]Error: Unknown command '{cmd}'[/red]")

    def _handle_custom_task(self, interpreted):
        """Handle a custom task that doesn't map to a built-in command.

        Custom tasks always run in watch mode (real-time progress streaming).
        """
        from prompt_toolkit import prompt as pt_prompt
        from rich.panel import Panel

        # Display AI's understanding
        self.console.print()
        self.console.print(Panel(
            f"[bold cyan]{interpreted.understood_request}[/bold cyan]",
            title="[yellow]Guided Pentest[/yellow]",
            border_style="cyan"
        ))

        # Show details
        if interpreted.target:
            self.console.print(f"  [dim]Target:[/dim] [white]{interpreted.target}[/white]")
        else:
            self.console.print(f"  [dim]Target:[/dim] [yellow]Not specified[/yellow]")

        if interpreted.tools_suggested:
            self.console.print(f"  [dim]Suggested tools:[/dim] [white]{', '.join(interpreted.tools_suggested)}[/white]")

        if interpreted.parameters:
            self.console.print(f"  [dim]Parameters:[/dim] [white]{', '.join(interpreted.parameters)}[/white]")

        self.console.print(f"  [dim]Confidence:[/dim] [white]{interpreted.confidence}[/white]")
        self.console.print(f"  [dim]Mode:[/dim] [magenta]Real-time streaming[/magenta]")
        self.console.print()

        # Ask for target if needed (required like regular pentests)
        target = interpreted.target
        if interpreted.needs_target or not target:
            target = pt_prompt(
                FormattedText([('class:prompt', 'Target (IP/domain/URL): ')]),
                style=PROMPT_STYLE
            )
            if not target.strip():
                self.console.print("[yellow]Cancelled - target is required[/yellow]")
                return
            target = target.strip()

        # Ask for confirmation (guided mode always uses watch/streaming)
        confirm = pt_prompt(
            FormattedText([('class:prompt', 'Execute? (Y/n): ')]),
            style=PROMPT_STYLE
        )

        if confirm.lower().strip() == 'n':
            self.console.print("[dim]Cancelled[/dim]")
            return

        # Run the guided pentest with continuation loop (always in watch mode)
        self._run_guided_pentest(
            description=interpreted.task_description,
            target=target,
            parameters=interpreted.parameters,
            pentest_id=None  # New pentest
        )

    def _run_guided_pentest(
        self,
        description: str,
        target: str,
        parameters: List[str],
        pentest_id: Optional[str] = None
    ):
        """Run a guided pentest with real-time streaming and continuation prompts.

        Guided pentests always run in watch mode (real-time progress streaming).
        After each task completion, asks if there's more to do.
        Continues until user says no or exits.
        """
        from prompt_toolkit import prompt as pt_prompt
        import re

        creds = load_credentials()
        if not creds:
            self.console.print("[red]Not configured. Run: configure[/red]")
            return

        current_pentest_id = pentest_id
        current_description = description

        while True:
            # Build and run command - always with --watch for real-time streaming
            cmd = [
                sys.executable, "-m", "twpt_cli.main", "task",
                current_description,
                "--target", target,
                "--watch"  # Always watch mode for guided pentests
            ]

            # Continue existing session if we have a pentest ID
            if current_pentest_id:
                cmd.extend(["--session", current_pentest_id])

            for param in parameters:
                cmd.extend(["--param", param])

            self.console.print()
            try:
                # Run the task with real-time output (watch mode)
                subprocess.run(cmd, check=False)

            except KeyboardInterrupt:
                self.console.print("\n[yellow]Task interrupted[/yellow]")
                break

            # After task completion, ask if there's anything else to do
            self.console.print()
            self.console.print("[cyan]─" * 50 + "[/cyan]")
            self.console.print()

            try:
                next_action = pt_prompt(
                    FormattedText([
                        ('class:prompt.status', '◆ '),
                        ('class:prompt', 'Anything else to do on '),
                        ('class:prompt.status', target),
                        ('class:prompt', '? (describe or '),
                        ('class:prompt.status.warning', 'done'),
                        ('class:prompt', ' to finish): '),
                    ]),
                    style=PROMPT_STYLE
                )
            except (KeyboardInterrupt, EOFError):
                self.console.print("\n[yellow]Session ended[/yellow]")
                break

            next_action = next_action.strip()

            if not next_action or next_action.lower() in ['done', 'no', 'n', 'exit', 'quit', 'q', 'finish', 'complete']:
                # User is done - finalize the pentest
                self.console.print()
                self.console.print("[green]✓ Guided pentest session completed[/green]")
                if current_pentest_id:
                    self.console.print(f"  [dim]Pentest ID:[/dim] [cyan]{current_pentest_id}[/cyan]")
                    self.console.print(f"  [dim]Use[/dim] get {current_pentest_id} [dim]to view details[/dim]")
                    self.console.print(f"  [dim]Use[/dim] download {current_pentest_id} [dim]to get evidence[/dim]")
                    # Store as last pentest ID for convenience
                    self.last_pentest_id = current_pentest_id
                self.console.print()
                break
            else:
                # User wants to do more - interpret the new request
                from rich.spinner import Spinner
                from rich.live import Live

                with Live(Spinner("dots", text="Understanding..."), refresh_per_second=10, console=self.console):
                    new_interpreted = interpret_request(f"{next_action} on {target}")

                if new_interpreted:
                    current_description = new_interpreted.task_description
                    parameters = new_interpreted.parameters
                else:
                    # Use raw input as description
                    current_description = next_action
                    parameters = []

                # Continue the loop with the new task
                is_first_task = False


def main():
    """Main entry point for interactive shell."""
    shell = InteractiveShell()
    shell.run()


if __name__ == "__main__":
    main()
