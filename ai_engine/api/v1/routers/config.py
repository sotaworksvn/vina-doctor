from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator

from ai_engine.application.use_cases.update_api_key_use_case import UpdateApiKeyUseCase

router = APIRouter(prefix="/v1/config", tags=["config"])


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------


class UpdateDashscopeApiKeyRequest(BaseModel):
    api_key: str

    @field_validator("api_key")
    @classmethod
    def must_not_be_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("api_key must not be blank.")
        return v.strip()


# ---------------------------------------------------------------------------
# Dependency injection (deferred import to avoid circular imports)
# ---------------------------------------------------------------------------


def _get_use_case() -> UpdateApiKeyUseCase:
    from ai_engine.main import get_update_api_key_use_case  # noqa: PLC0415

    return get_update_api_key_use_case()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.patch(
    "/dashscope-api-key",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update the DashScope API key at runtime",
    description=(
        "Replaces the active DashScope API key in-process **and** persists it "
        "to a config file on the mounted volume so that the new key survives "
        "a container restart.  No restart required."
    ),
)
def update_dashscope_api_key(
    body: UpdateDashscopeApiKeyRequest,
    use_case: UpdateApiKeyUseCase = Depends(_get_use_case),
) -> None:
    try:
        use_case.execute(body.api_key)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
