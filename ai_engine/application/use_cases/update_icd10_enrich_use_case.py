"""Application use case — toggle ICD-10 context enrichment at runtime.

Persists the enabled/disabled flag to ``runtime.json`` via the config
repository.  The change is picked up by ``ProcessConsultationUseCase`` on
the *next* request without a restart because the use case reads the flag
from the config repo on each invocation.
"""

from __future__ import annotations

from ai_engine.domain.config_repository import ConfigRepositoryProtocol


class UpdateICD10EnrichUseCase:
    """Enable or disable ICD-10 enrichment at runtime (no restart required).

    The flag is persisted to the config file so it survives container restarts.
    """

    def __init__(self, config_repo: ConfigRepositoryProtocol) -> None:
        self._config_repo = config_repo

    def execute(self, *, enabled: bool) -> None:
        """Persist the ICD-10 enrichment toggle.

        Args:
            enabled: ``True`` to enable enrichment, ``False`` to disable.
        """
        self._config_repo.set_icd10_enrich_enabled(enabled)

    def is_enabled(self) -> bool:
        """Return the current persisted state of the toggle."""
        return self._config_repo.get_icd10_enrich_enabled()
