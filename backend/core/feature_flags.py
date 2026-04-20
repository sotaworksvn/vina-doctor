from __future__ import annotations

from backend.core.config import get_settings


def is_auth_disabled() -> bool:
    """Return True when DISABLE_AUTH=true, bypassing all login/logout checks."""
    return get_settings().disable_auth
