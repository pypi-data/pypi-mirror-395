"""Plan management for custom pentest plans.

Local plan storage at ~/.twpt/plans/ for managing custom pentest plans.
Plans are stored as markdown files with metadata in an index.json file.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any

from .constants import USER_CONFIG_PATH


# Plans storage directory
PLANS_DIR = USER_CONFIG_PATH / "plans"
PLANS_INDEX_FILE = PLANS_DIR / "index.json"


def _ensure_plans_dir() -> Path:
    """Ensure the plans directory exists."""
    PLANS_DIR.mkdir(parents=True, exist_ok=True)
    return PLANS_DIR


def _load_index() -> Dict[str, Any]:
    """Load the plans index file."""
    if not PLANS_INDEX_FILE.exists():
        return {"plans": {}}

    try:
        with open(PLANS_INDEX_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"plans": {}}


def _save_index(index: Dict[str, Any]) -> None:
    """Save the plans index file."""
    _ensure_plans_dir()
    with open(PLANS_INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=2, default=str)


def _sanitize_plan_name(name: str) -> str:
    """Sanitize a plan name for use as a filename.

    Args:
        name: The plan name to sanitize

    Returns:
        A filesystem-safe version of the name
    """
    # Replace problematic characters
    safe_name = name.lower()
    for char in [' ', '/', '\\', ':', '*', '?', '"', '<', '>', '|']:
        safe_name = safe_name.replace(char, '-')

    # Remove multiple consecutive dashes
    while '--' in safe_name:
        safe_name = safe_name.replace('--', '-')

    # Strip leading/trailing dashes
    safe_name = safe_name.strip('-')

    # Truncate if too long
    if len(safe_name) > 100:
        safe_name = safe_name[:100].rstrip('-')

    return safe_name or "unnamed-plan"


def get_plan_file_path(name: str) -> Path:
    """Get the file path for a plan by name.

    Args:
        name: The plan name

    Returns:
        Path to the plan file
    """
    safe_name = _sanitize_plan_name(name)
    return PLANS_DIR / f"{safe_name}.md"


def save_plan(
    name: str,
    content: str,
    description: Optional[str] = None,
    version: str = "1.0",
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Save a plan to local storage.

    Args:
        name: Plan name (used for identification and filename)
        content: The markdown content of the plan
        description: Optional short description of the plan
        version: Version string (default: "1.0")
        tags: Optional list of tags for categorization

    Returns:
        Dict with plan metadata

    Raises:
        ValueError: If name is empty or content is empty
    """
    if not name or not name.strip():
        raise ValueError("Plan name cannot be empty")
    if not content or not content.strip():
        raise ValueError("Plan content cannot be empty")

    _ensure_plans_dir()

    safe_name = _sanitize_plan_name(name)
    plan_path = PLANS_DIR / f"{safe_name}.md"

    # Write the plan content
    with open(plan_path, 'w') as f:
        f.write(content)

    # Update the index
    index = _load_index()
    now = datetime.now(timezone.utc).isoformat()

    # Check if plan already exists (update vs create)
    is_update = safe_name in index["plans"]

    index["plans"][safe_name] = {
        "name": name,
        "safe_name": safe_name,
        "description": description or "",
        "version": version,
        "tags": tags or [],
        "created_at": index["plans"].get(safe_name, {}).get("created_at", now),
        "updated_at": now,
        "file_path": str(plan_path),
    }

    _save_index(index)

    return {
        "success": True,
        "action": "updated" if is_update else "created",
        "plan": index["plans"][safe_name],
    }


def get_plan(name: str) -> Optional[Dict[str, Any]]:
    """Get a plan by name.

    Args:
        name: Plan name (original or safe name)

    Returns:
        Dict with plan metadata and content, or None if not found
    """
    safe_name = _sanitize_plan_name(name)
    index = _load_index()

    if safe_name not in index["plans"]:
        return None

    plan_meta = index["plans"][safe_name]
    plan_path = Path(plan_meta["file_path"])

    if not plan_path.exists():
        return None

    with open(plan_path, 'r') as f:
        content = f.read()

    return {
        **plan_meta,
        "content": content,
    }


def list_plans(tag: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all saved plans.

    Args:
        tag: Optional tag to filter plans by

    Returns:
        List of plan metadata dicts (without content)
    """
    index = _load_index()
    plans = list(index["plans"].values())

    # Filter by tag if specified
    if tag:
        plans = [p for p in plans if tag.lower() in [t.lower() for t in p.get("tags", [])]]

    # Sort by updated_at (most recent first)
    plans.sort(key=lambda p: p.get("updated_at", ""), reverse=True)

    return plans


def delete_plan(name: str) -> bool:
    """Delete a plan by name.

    Args:
        name: Plan name (original or safe name)

    Returns:
        True if deleted, False if not found
    """
    safe_name = _sanitize_plan_name(name)
    index = _load_index()

    if safe_name not in index["plans"]:
        return False

    plan_meta = index["plans"][safe_name]
    plan_path = Path(plan_meta["file_path"])

    # Delete the file
    if plan_path.exists():
        plan_path.unlink()

    # Remove from index
    del index["plans"][safe_name]
    _save_index(index)

    return True


def load_plan_from_file(file_path: str) -> str:
    """Load plan content from a file path.

    Args:
        file_path: Path to the markdown file

    Returns:
        The content of the file

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is not readable or is empty
    """
    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"Plan file not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Not a file: {file_path}")

    content = path.read_text()

    if not content.strip():
        raise ValueError(f"Plan file is empty: {file_path}")

    return content


def resolve_plan_reference(reference: str) -> str:
    """Resolve a plan reference to its content.

    Supports two formats:
    - "file:<path>" - Load from file
    - "<plan-name>" - Load from saved plans (default)

    Args:
        reference: Plan reference string

    Returns:
        The plan content

    Raises:
        ValueError: If plan not found
    """
    if reference.startswith("file:"):
        # Load from file path
        file_path = reference[5:]  # Remove "file:" prefix
        if not file_path:
            raise ValueError("File path cannot be empty in 'file:<path>' format")
        return load_plan_from_file(file_path)
    else:
        # Load from saved plans (default)
        plan = get_plan(reference)
        if not plan:
            raise ValueError(f"Plan not found: {reference}. Use 'plan list' to see saved plans.")

        return plan["content"]


def get_plan_metadata(reference: str) -> Dict[str, Any]:
    """Get metadata for a plan reference.

    Args:
        reference: Plan reference string ("file:<path>" or plan name)

    Returns:
        Dict with name, version, and description
    """
    if reference.startswith("file:"):
        # For file paths, extract name from filename
        file_path = reference[5:]
        path = Path(file_path)
        name = path.stem  # Filename without extension
        return {"name": name, "version": "1.0", "description": f"Loaded from {path.name}"}
    else:
        # Load from saved plans
        plan = get_plan(reference)
        if plan:
            return {
                "name": plan.get("name", reference),
                "version": plan.get("version", "1.0"),
                "description": plan.get("description", ""),
            }
        return {"name": reference, "version": "1.0", "description": ""}
