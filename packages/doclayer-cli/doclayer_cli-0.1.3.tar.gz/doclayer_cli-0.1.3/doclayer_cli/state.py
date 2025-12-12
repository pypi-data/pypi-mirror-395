from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .ingest import UploadResult


class UploadStateStore:
    """
    Persist upload progress so large batches can resume after interruption.

    The store writes a JSON file where each key is the resolved path to the
    uploaded document and the value captures metadata (status, job_id, etc.).
    """

    def __init__(self, path: Optional[Path], resume: bool) -> None:
        self._enabled = path is not None
        self.path = Path(path) if path else None
        self.resume = resume
        self._lock = threading.Lock()
        self._state: Dict[str, Dict[str, Any]] = {}

        if not self._enabled:
            return

        if self.path is None:
            return

        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            try:
                self._state = json.loads(self.path.read_text())
            except json.JSONDecodeError:
                # Corrupt or empty file – start fresh but keep backup
                backup = self.path.with_suffix(".bak")
                backup.write_text(self.path.read_text())
                self._state = {}

    def should_skip(self, path: Path) -> bool:
        if not (self._enabled and self.resume and self.path):
            return False
        entry = self._state.get(str(path))
        return bool(entry and entry.get("status") == "success")

    def record(self, result: "UploadResult") -> None:
        if not (self._enabled and self.path):
            return

        payload = {
            "status": "error" if result.error else "success",
            "job_id": result.job_id,
            "document_id": result.document_id,
            "duration_ms": result.duration_ms,
            "size_bytes": result.size_bytes,
            "error": result.error,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        with self._lock:
            self._state[str(result.path)] = payload
            tmp_path = self.path.with_suffix(".tmp")
            tmp_path.write_text(json.dumps(self._state, indent=2, sort_keys=True))
            tmp_path.replace(self.path)
