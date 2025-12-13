"""
Persistence helpers for meta-learning artefacts.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional


@dataclass
class MetaStorageConfig:
    root: Path = Path("artifacts/meta")
    prior_name: str = "global_prior.json"
    domain_vectors_name: str = "domain_vectors.json"
    retention: int = 10


class MetaStorageManager:
    def __init__(self, config: Optional[MetaStorageConfig] = None):
        self.config = config or MetaStorageConfig()
        self.config.root.mkdir(parents=True, exist_ok=True)
        (self.config.root / "backups").mkdir(exist_ok=True)

    def save_prior(self, prior: Dict[str, float]) -> Path:
        path = self.config.root / self.config.prior_name
        with path.open("w", encoding="utf-8") as fh:
            json.dump(prior, fh, indent=2, sort_keys=True)
        self._backup(path)
        return path

    def load_prior(self) -> Dict[str, float]:
        path = self.config.root / self.config.prior_name
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    def save_domain_vectors(self, vectors: Dict[str, Dict[str, float]]) -> Path:
        path = self.config.root / self.config.domain_vectors_name
        with path.open("w", encoding="utf-8") as fh:
            json.dump(vectors, fh, indent=2, sort_keys=True)
        return path

    def load_domain_vectors(self) -> Dict[str, Dict[str, float]]:
        path = self.config.root / self.config.domain_vectors_name
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    def _backup(self, path: Path) -> None:
        backup_dir = self.config.root / "backups"
        timestamp = path.stat().st_mtime
        backup_path = backup_dir / f"{path.stem}_{int(timestamp)}{path.suffix}"
        backup_path.write_bytes(path.read_bytes())
        backups = sorted(backup_dir.glob(f"{path.stem}_*{path.suffix}"), key=lambda p: p.stat().st_mtime, reverse=True)
        for old in backups[self.config.retention :]:
            old.unlink(missing_ok=True)

