from __future__ import annotations

from typing import Callable

from ai_engine.domain.config_repository import ConfigRepositoryProtocol


class UpdateApiKeyUseCase:
    """Application use case — update the DashScope API key at runtime.

    Responsibilities (SRP):
      1. Validate the new key is non-empty.
      2. Apply it in-process via the injected *apply_key* callable.
      3. Persist it via the injected *config_repo* (ConfigRepositoryProtocol).

    Dependency Inversion: this class never imports ``dashscope`` or any file-
    system module.  The ``apply_key`` callable (injected in ``main.py`` as
    ``lambda k: setattr(dashscope, "api_key", k)``) bridges the gap, keeping
    this use case free of infrastructure concerns.
    """

    def __init__(
        self,
        config_repo: ConfigRepositoryProtocol,
        apply_key: Callable[[str], None],
    ) -> None:
        self._config_repo = config_repo
        self._apply_key = apply_key

    def execute(self, new_key: str) -> None:
        """Validate, apply in-process, and persist *new_key*.

        Args:
            new_key: The new DashScope API key to activate.

        Raises:
            ValueError: if *new_key* is blank.
        """
        key = new_key.strip() if new_key else ""
        if not key:
            raise ValueError("API key must not be empty.")

        # Apply in-process first so the current request benefits immediately.
        self._apply_key(key)
        # Then persist so the key survives a container restart.
        self._config_repo.set_dashscope_key(key)
