from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path


class FileConfigRepository:
    """Infrastructure implementation of ConfigRepositoryProtocol.

    Persists runtime configuration as a JSON file on disk.
    Reads and writes are atomic — a write to a temporary file followed by
    ``os.replace`` ensures the reader never sees a partial write.

    The directory is created on first write if it does not yet exist.
    """

    _KEY_DASHSCOPE = "dashscope_api_key"

    def __init__(self, path: str | Path = "/app/config/runtime.json") -> None:
        self._path = Path(path)

    # ------------------------------------------------------------------
    # ConfigRepositoryProtocol implementation
    # ------------------------------------------------------------------

    def get_dashscope_key(self) -> str | None:
        """Return the persisted DashScope API key, or *None* if not found."""
        data = self._read()
        value = data.get(self._KEY_DASHSCOPE)
        return value if isinstance(value, str) and value else None

    def set_dashscope_key(self, key: str) -> None:
        """Atomically persist *key* to the config file."""
        if not key or not key.strip():
            raise ValueError("DashScope API key must not be empty.")
        data = self._read()
        data[self._KEY_DASHSCOPE] = key.strip()
        self._write(data)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _read(self) -> dict:
        """Return the config dict, or an empty dict if the file does not exist."""
        try:
            return json.loads(self._path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            # Corrupted file — treat as empty rather than crashing the app.
            return {}

    def _write(self, data: dict) -> None:
        """Write *data* to disk atomically via a temp file + os.replace."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(
            dir=self._path.parent, prefix=".tmp_runtime_", suffix=".json"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(tmp_path, self._path)
        except Exception:
            # Clean up the temp file on any error before re-raising.
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise
