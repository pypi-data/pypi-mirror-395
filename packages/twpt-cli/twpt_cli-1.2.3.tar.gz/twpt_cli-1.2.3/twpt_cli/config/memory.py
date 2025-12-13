"""Memory management for pentest context/notes.

File-based memory storage in a local `memory/` folder within the project directory.
Memory items are stored as markdown (.md) files that can be edited directly.

Memory items can be:
1. Saved in the memory/ folder for reuse across pentests
2. Passed inline via --memory flag (transient)
3. Referenced by filename (with or without .md extension)

Special files:
- memory/default.md: Auto-included in all standard pentests (not custom plans)

When a pentest runs, memory items are sent to the agent and made available
to the AI throughout all phases of the pentest execution.
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any


# Memory folder name (created in current working directory)
MEMORY_FOLDER_NAME = "memory"
DEFAULT_MEMORY_FILE = "default.md"


def get_memory_dir() -> Path:
    """Get the memory directory path (in current working directory).

    Returns:
        Path to the memory/ folder
    """
    return Path.cwd() / MEMORY_FOLDER_NAME


def ensure_memory_dir() -> Path:
    """Ensure the memory directory exists with README.

    Creates the memory/ folder and a README if they don't exist.

    Returns:
        Path to the memory/ folder
    """
    memory_dir = get_memory_dir()
    memory_dir.mkdir(parents=True, exist_ok=True)

    # Create README if it doesn't exist
    readme_path = memory_dir / "README.md"
    if not readme_path.exists():
        readme_content = '''# Memory - Pentest Context Notes

This folder contains memory items that provide context to the AI agent during pentests.

## What is Memory?

Memory items are notes, instructions, or context that you want the AI agent to keep in mind
throughout all phases of a penetration test. They persist across the entire pentest and help
guide the agent's behavior.

## How to Use

### Default Memory (default.md)

Create a file named `default.md` in this folder. Its contents will be automatically included
in every standard pentest you run (autonomous mode, not custom plans).

Example `default.md`:
```markdown
# Default Testing Guidelines

- Always try default credentials on discovered services
- Focus on SQL injection for web applications
- Check for directory traversal vulnerabilities
- Document all findings with screenshots
```

### Named Memory Items

Create any `.md` file in this folder to save reusable context:

```bash
# Create a memory item
echo "Focus on brute force attacks" > memory/brute-force.md

# Use it in a pentest
twpt-cli run example.com --memory brute-force
```

### Inline Memory

Pass context directly on the command line:
```bash
twpt-cli run example.com --memory "Try SQL injection on login forms"
```

### Multiple Memory Items

Combine multiple memory sources:
```bash
twpt-cli run example.com --memory brute-force --memory sqli-focus --memory "Also check for XSS"
```

## File Format

Memory files are plain markdown. The filename (without .md) becomes the memory item name.

Example `sqli-focus.md`:
```markdown
# SQL Injection Focus

Pay special attention to SQL injection vulnerabilities:
- Test all input fields with SQLi payloads
- Use sqlmap for automated testing
- Check for blind SQL injection
- Try time-based attacks if error-based fails
```

## Tips

1. Keep memory items focused and concise
2. Use descriptive filenames
3. The default.md file is great for your standard testing methodology
4. Create specialized memory items for specific target types (web, network, etc.)
'''
        with open(readme_path, 'w') as f:
            f.write(readme_content)

    return memory_dir


def _normalize_name(name: str) -> str:
    """Normalize a memory item name (strip .md extension if present).

    Args:
        name: The memory item name or filename

    Returns:
        Normalized name without .md extension
    """
    if name.lower().endswith('.md'):
        return name[:-3]
    return name


def get_memory_file_path(name: str) -> Path:
    """Get the file path for a memory item by name.

    Args:
        name: The memory item name (with or without .md extension)

    Returns:
        Path to the memory file
    """
    normalized = _normalize_name(name)
    return get_memory_dir() / f"{normalized}.md"


def memory_exists(name: str) -> bool:
    """Check if a memory item exists.

    Args:
        name: The memory item name (with or without .md extension)

    Returns:
        True if the memory file exists
    """
    return get_memory_file_path(name).exists()


def save_memory(name: str, content: str) -> Dict[str, Any]:
    """Save a memory item to the memory folder.

    Args:
        name: Memory item name (used for filename, .md will be appended)
        content: The memory content

    Returns:
        Dict with success status and file path

    Raises:
        ValueError: If name or content is empty
    """
    if not name or not name.strip():
        raise ValueError("Memory name cannot be empty")
    if not content or not content.strip():
        raise ValueError("Memory content cannot be empty")

    ensure_memory_dir()

    normalized = _normalize_name(name.strip())
    file_path = get_memory_dir() / f"{normalized}.md"

    is_update = file_path.exists()

    with open(file_path, 'w') as f:
        f.write(content)

    return {
        "success": True,
        "action": "updated" if is_update else "created",
        "name": normalized,
        "file_path": str(file_path),
    }


def get_memory(name: str) -> Optional[Dict[str, Any]]:
    """Get a memory item by name.

    Args:
        name: Memory item name (with or without .md extension)

    Returns:
        Dict with name and content, or None if not found
    """
    file_path = get_memory_file_path(name)

    if not file_path.exists():
        return None

    with open(file_path, 'r') as f:
        content = f.read()

    return {
        "name": _normalize_name(name),
        "content": content,
        "file_path": str(file_path),
    }


def list_memory() -> List[Dict[str, Any]]:
    """List all memory items in the memory folder.

    Returns:
        List of memory item dicts with name, file_path, and size
    """
    memory_dir = get_memory_dir()

    if not memory_dir.exists():
        return []

    items = []
    for file_path in sorted(memory_dir.glob("*.md")):
        # Skip README
        if file_path.name.lower() == "readme.md":
            continue

        stat = file_path.stat()
        items.append({
            "name": file_path.stem,  # filename without extension
            "file_path": str(file_path),
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "is_default": file_path.name.lower() == DEFAULT_MEMORY_FILE.lower(),
        })

    # Sort: default first, then alphabetically
    items.sort(key=lambda x: (not x["is_default"], x["name"].lower()))

    return items


def delete_memory(name: str) -> bool:
    """Delete a memory item by name.

    Args:
        name: Memory item name (with or without .md extension)

    Returns:
        True if deleted, False if not found
    """
    file_path = get_memory_file_path(name)

    if not file_path.exists():
        return False

    file_path.unlink()
    return True


def get_default_memory() -> Optional[Dict[str, str]]:
    """Get the default memory item (default.md) if it exists.

    Returns:
        Dict with name and content, or None if no default.md
    """
    return get_memory("default")


def get_memory_for_pentest(
    memory_names: Optional[List[str]] = None,
    inline_memory: Optional[List[str]] = None,
    include_default: bool = True,
) -> List[Dict[str, str]]:
    """Get all memory items to include in a pentest.

    This combines:
    1. default.md (if include_default=True and no specific memory requested)
    2. Specifically requested memory items by name
    3. Inline memory strings passed via --memory flag

    Args:
        memory_names: List of specific memory item names to include
        inline_memory: List of inline memory strings to include
        include_default: Whether to include default.md (when no specific memory)

    Returns:
        List of dicts with 'name' and 'content' keys
    """
    result = []
    seen_names = set()

    # If no specific memory requested, include default.md
    if include_default and not memory_names and not inline_memory:
        default_mem = get_default_memory()
        if default_mem:
            result.append({
                "name": "default",
                "content": default_mem["content"],
            })
            seen_names.add("default")

    # Add specifically requested memory items
    if memory_names:
        for name in memory_names:
            normalized = _normalize_name(name)
            if normalized not in seen_names:
                memory_data = get_memory(name)
                if memory_data:
                    result.append({
                        "name": memory_data["name"],
                        "content": memory_data["content"],
                    })
                    seen_names.add(normalized)

    # Add inline memory items
    if inline_memory:
        for idx, content in enumerate(inline_memory):
            name = f"inline-{idx + 1}"
            result.append({
                "name": name,
                "content": content,
            })

    return result


def format_memory_for_prompt(memory_items: List[Dict[str, str]]) -> str:
    """Format memory items into a string for inclusion in AI prompts.

    Args:
        memory_items: List of memory items with 'name' and 'content' keys

    Returns:
        Formatted string for AI prompt inclusion
    """
    if not memory_items:
        return ""

    lines = ["## User-Provided Context/Notes\n"]
    lines.append("The following context has been provided by the user for this pentest:\n")

    for item in memory_items:
        lines.append(f"### {item['name']}")
        lines.append(item['content'])
        lines.append("")

    lines.append("Please keep these notes in mind throughout all phases of the pentest.\n")

    return "\n".join(lines)


__all__ = [
    "MEMORY_FOLDER_NAME",
    "DEFAULT_MEMORY_FILE",
    "get_memory_dir",
    "ensure_memory_dir",
    "get_memory_file_path",
    "memory_exists",
    "save_memory",
    "get_memory",
    "list_memory",
    "delete_memory",
    "get_default_memory",
    "get_memory_for_pentest",
    "format_memory_for_prompt",
]
