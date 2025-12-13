"""Simple model registry management."""

from __future__ import annotations

from pathlib import Path
from typing import List

_registry_root: Path | None = None


def init_registry(path: Path) -> None:
    """Initialise the registry root directory."""

    global _registry_root  # noqa: PLW0603
    _registry_root = path
    _registry_root.mkdir(parents=True, exist_ok=True)


def _ensure_root() -> Path:
    if _registry_root is None:
        raise RuntimeError("Model registry not initialised.")
    return _registry_root


def list_models() -> List[dict[str, object]]:
    """Return a listing of stored model artefacts."""

    root = _ensure_root()
    entries = []
    for item in sorted(root.glob("*.json")):
        entries.append(
            {
                "rev": item.stem,
                "path": str(item),
                "size": item.stat().st_size,
            }
        )
    return entries


def save_model(revision: str, content: bytes) -> str:
    """Persist a model revision to disk."""

    root = _ensure_root()
    path = root / f"{revision}.json"
    path.write_bytes(content)
    return str(path)


def get_model_path(revision: str) -> Path:
    """Return path to a stored model revision."""

    root = _ensure_root()
    path = root / f"{revision}.json"
    if not path.exists():
        raise FileNotFoundError(f"Model revision {revision} not found.")
    return path



