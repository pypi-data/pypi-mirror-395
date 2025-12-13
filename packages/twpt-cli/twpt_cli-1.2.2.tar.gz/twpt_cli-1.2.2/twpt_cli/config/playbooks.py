"""Playbook (plan) management for custom pentest plans.

File-based playbook storage in a local `playbooks/` folder within the project directory.
Playbooks are stored as markdown (.md) files that define multi-step pentest plans.

Playbooks can be:
1. Saved in the playbooks/ folder for reuse
2. Referenced by filename (with or without .md extension)
3. Loaded from any file path with file: prefix

When a pentest runs with --plan, the playbook content is sent to the agent
which executes each phase/step systematically.
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any


# Playbooks folder name (created in current working directory)
PLAYBOOKS_FOLDER_NAME = "playbooks"


def get_playbooks_dir() -> Path:
    """Get the playbooks directory path (in current working directory).

    Returns:
        Path to the playbooks/ folder
    """
    return Path.cwd() / PLAYBOOKS_FOLDER_NAME


def ensure_playbooks_dir() -> Path:
    """Ensure the playbooks directory exists with README.

    Creates the playbooks/ folder and a README if they don't exist.

    Returns:
        Path to the playbooks/ folder
    """
    playbooks_dir = get_playbooks_dir()
    playbooks_dir.mkdir(parents=True, exist_ok=True)

    # Create README if it doesn't exist
    readme_path = playbooks_dir / "README.md"
    if not readme_path.exists():
        readme_content = '''# Playbooks - Custom Pentest Plans

This folder contains playbooks (custom pentest plans) that define multi-step
penetration testing workflows for the AI agent to execute.

## What are Playbooks?

Playbooks are markdown documents that describe a structured pentest methodology.
Unlike memory items (which provide context), playbooks define the actual steps
and phases the AI agent should follow during the pentest.

## How to Use

### Creating a Playbook

Create a `.md` file in this folder with your pentest plan:

```bash
# Create a playbook
twpt-cli plan save web-audit playbooks/web-audit.md

# Or just create the file directly
nano playbooks/web-audit.md
```

### Running a Playbook

Use the `--plan` option to run a pentest with a specific playbook:

```bash
# Run with a saved playbook
twpt-cli run example.com --plan web-audit

# Run with a file path
twpt-cli run example.com --plan file:./my-custom-plan.md
```

## Playbook Format

Playbooks use markdown with sections for each phase. Example structure:

```markdown
# Web Application Security Audit

## Overview
A comprehensive web application security assessment.

## Phase 1: Reconnaissance
- [ ] Identify all subdomains
- [ ] Map the application structure
- [ ] Enumerate technologies used

## Phase 2: Authentication Testing
- [ ] Test login forms for SQLi
- [ ] Check for default credentials
- [ ] Test password reset functionality

## Phase 3: Authorization Testing
- [ ] Test for IDOR vulnerabilities
- [ ] Check role-based access controls
- [ ] Test API authorization

## Phase 4: Input Validation
- [ ] Test all forms for XSS
- [ ] Check for command injection
- [ ] Test file upload functionality

## Deliverables
- Summary of findings
- Risk ratings for each issue
- Remediation recommendations
```

## Example Playbooks

### Quick Web Scan (quick-web.md)
```markdown
# Quick Web Security Scan

## Scope
Fast assessment of web application security posture.

## Phase 1: Surface Analysis (10 min)
- Run quick port scan
- Identify web technologies
- Check SSL/TLS configuration

## Phase 2: Common Vulnerabilities (15 min)
- Test for SQLi on login forms
- Check for obvious XSS
- Test for directory traversal

## Output
Brief summary of critical findings only.
```

### Network Pentest (network-pentest.md)
```markdown
# Network Penetration Test

## Phase 1: Discovery
- Full port scan
- Service enumeration
- OS fingerprinting

## Phase 2: Vulnerability Assessment
- Check for known CVEs
- Test default credentials
- Identify misconfigurations

## Phase 3: Exploitation
- Attempt to exploit high-risk findings
- Document proof of concept
- Assess impact

## Phase 4: Reporting
- Create detailed findings report
- Prioritize by risk level
```

## Tips

1. Be specific about what you want tested
2. Include time estimates if relevant
3. Define clear deliverables
4. Break complex tests into phases
5. Include any special instructions or constraints
'''
        with open(readme_path, 'w') as f:
            f.write(readme_content)

    return playbooks_dir


def _normalize_name(name: str) -> str:
    """Normalize a playbook name (strip .md extension if present).

    Args:
        name: The playbook name or filename

    Returns:
        Normalized name without .md extension
    """
    if name.lower().endswith('.md'):
        return name[:-3]
    return name


def get_playbook_file_path(name: str) -> Path:
    """Get the file path for a playbook by name.

    Args:
        name: The playbook name (with or without .md extension)

    Returns:
        Path to the playbook file
    """
    normalized = _normalize_name(name)
    return get_playbooks_dir() / f"{normalized}.md"


def playbook_exists(name: str) -> bool:
    """Check if a playbook exists.

    Args:
        name: The playbook name (with or without .md extension)

    Returns:
        True if the playbook file exists
    """
    return get_playbook_file_path(name).exists()


def save_playbook(name: str, content: str) -> Dict[str, Any]:
    """Save a playbook to the playbooks folder.

    Args:
        name: Playbook name (used for filename, .md will be appended)
        content: The playbook content

    Returns:
        Dict with success status and file path

    Raises:
        ValueError: If name or content is empty
    """
    if not name or not name.strip():
        raise ValueError("Playbook name cannot be empty")
    if not content or not content.strip():
        raise ValueError("Playbook content cannot be empty")

    ensure_playbooks_dir()

    normalized = _normalize_name(name.strip())
    file_path = get_playbooks_dir() / f"{normalized}.md"

    is_update = file_path.exists()

    with open(file_path, 'w') as f:
        f.write(content)

    return {
        "success": True,
        "action": "updated" if is_update else "created",
        "name": normalized,
        "file_path": str(file_path),
    }


def save_playbook_from_file(source_path: str, name: str) -> Dict[str, Any]:
    """Save a playbook from an existing file.

    Args:
        source_path: Path to the source markdown file
        name: Name for the playbook

    Returns:
        Dict with success status and file path

    Raises:
        FileNotFoundError: If source file doesn't exist
        ValueError: If name is empty
    """
    source = Path(source_path)
    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    content = source.read_text()
    return save_playbook(name, content)


def get_playbook(name: str) -> Optional[Dict[str, Any]]:
    """Get a playbook by name.

    Args:
        name: Playbook name (with or without .md extension)

    Returns:
        Dict with name and content, or None if not found
    """
    file_path = get_playbook_file_path(name)

    if not file_path.exists():
        return None

    with open(file_path, 'r') as f:
        content = f.read()

    return {
        "name": _normalize_name(name),
        "content": content,
        "file_path": str(file_path),
    }


def list_playbooks() -> List[Dict[str, Any]]:
    """List all playbooks in the playbooks folder.

    Returns:
        List of playbook dicts with name, file_path, and size
    """
    playbooks_dir = get_playbooks_dir()

    if not playbooks_dir.exists():
        return []

    items = []
    for file_path in sorted(playbooks_dir.glob("*.md")):
        # Skip README
        if file_path.name.lower() == "readme.md":
            continue

        stat = file_path.stat()
        items.append({
            "name": file_path.stem,  # filename without extension
            "file_path": str(file_path),
            "size": stat.st_size,
            "modified": stat.st_mtime,
        })

    # Sort alphabetically
    items.sort(key=lambda x: x["name"].lower())

    return items


def delete_playbook(name: str) -> bool:
    """Delete a playbook by name.

    Args:
        name: Playbook name (with or without .md extension)

    Returns:
        True if deleted, False if not found
    """
    file_path = get_playbook_file_path(name)

    if not file_path.exists():
        return False

    file_path.unlink()
    return True


def resolve_playbook_reference(reference: str) -> str:
    """Resolve a playbook reference to its content.

    Supports:
    - Simple name: "web-audit" -> looks in playbooks/web-audit.md
    - File path: "file:./my-plan.md" -> loads from the specified path

    Args:
        reference: Playbook name or file: reference

    Returns:
        Playbook content

    Raises:
        FileNotFoundError: If playbook not found
        ValueError: If reference is empty
    """
    if not reference or not reference.strip():
        raise ValueError("Playbook reference cannot be empty")

    reference = reference.strip()

    # Check for file: prefix
    if reference.startswith("file:"):
        file_path = Path(reference[5:])
        if not file_path.exists():
            raise FileNotFoundError(f"Playbook file not found: {file_path}")
        return file_path.read_text()

    # Look up by name in playbooks folder
    playbook = get_playbook(reference)
    if playbook:
        return playbook["content"]

    raise FileNotFoundError(
        f"Playbook not found: {reference}\n"
        f"Looked in: {get_playbooks_dir()}"
    )


def get_playbook_metadata(reference: str) -> Dict[str, Any]:
    """Get metadata for a playbook reference.

    Args:
        reference: Playbook name or file: reference

    Returns:
        Dict with name, version, and description
    """
    reference = reference.strip()

    if reference.startswith("file:"):
        file_path = Path(reference[5:])
        return {
            "name": file_path.stem,
            "version": "1.0",
            "description": f"Loaded from {file_path}",
            "source": "file",
        }

    return {
        "name": _normalize_name(reference),
        "version": "1.0",
        "description": f"Playbook from playbooks/{reference}.md",
        "source": "playbooks",
    }


__all__ = [
    "PLAYBOOKS_FOLDER_NAME",
    "get_playbooks_dir",
    "ensure_playbooks_dir",
    "get_playbook_file_path",
    "playbook_exists",
    "save_playbook",
    "save_playbook_from_file",
    "get_playbook",
    "list_playbooks",
    "delete_playbook",
    "resolve_playbook_reference",
    "get_playbook_metadata",
]
