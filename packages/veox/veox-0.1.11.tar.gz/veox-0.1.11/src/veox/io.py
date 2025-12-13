"""Persistence helpers for Veox models."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class VeoxIOError(RuntimeError):
    """Raised when persistence operations fail."""


def write_json(path: str | Path, payload: Dict[str, Any]) -> Path:
    """Write JSON payload to disk with UTF-8 encoding."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        data = json.dumps(payload, indent=2, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise VeoxIOError(f"Unable to serialize payload to JSON: {exc}") from exc

    tmp_path = target.with_suffix(target.suffix + ".tmp")
    tmp_path.write_text(data, encoding="utf-8")
    tmp_path.replace(target)
    return target


def read_json(path: str | Path) -> Dict[str, Any]:
    """Load JSON payload from disk."""
    target = Path(path)
    try:
        text = target.read_text(encoding="utf-8")
    except OSError as exc:
        raise VeoxIOError(f"Unable to read JSON file {target}: {exc}") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise VeoxIOError(f"Invalid JSON in {target}: {exc}") from exc

