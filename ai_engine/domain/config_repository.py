from __future__ import annotations

from typing import Protocol


class ConfigRepositoryProtocol(Protocol):
    """Domain port — persists and retrieves runtime configuration.

    Implementations live in the infrastructure layer.
    The application layer depends only on this abstraction.
    """

    def get_dashscope_key(self) -> str | None:
        """Return the persisted DashScope API key, or *None* if not set."""
        ...

    def set_dashscope_key(self, key: str) -> None:
        """Persist *key* as the new DashScope API key."""
        ...
