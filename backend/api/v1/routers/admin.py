from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator

from backend.api.v1.deps import get_ai_engine_client, get_current_user_id
from backend.infrastructure.clients.ai_engine_protocol import AiEngineClientProtocol

router = APIRouter(prefix="/admin", tags=["admin"])


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
# Routes
# ---------------------------------------------------------------------------


@router.post(
    "/config/dashscope-api-key",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update the DashScope API key at runtime",
    description=(
        "Proxies the new key to the AI engine service, which applies it "
        "in-process immediately and persists it to a volume-mounted file so "
        "it survives a container restart.  Requires a valid Bearer JWT."
    ),
)
async def update_dashscope_api_key(
    body: UpdateDashscopeApiKeyRequest,
    _user_id: str = Depends(get_current_user_id),
    ai_engine: AiEngineClientProtocol = Depends(get_ai_engine_client),
) -> None:
    try:
        await ai_engine.update_dashscope_key(body.api_key)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to update API key in ai_engine: {exc}",
        ) from exc
