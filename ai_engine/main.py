from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import dashscope
from fastapi import FastAPI
from dotenv import load_dotenv

from ai_engine.agents.extractor import MedicalExtractor
from ai_engine.agents.reporter import MedicalReporter
from ai_engine.application.use_cases.process_audio_use_case import ProcessAudioUseCase
from ai_engine.api.v1.routers.consultations import router as consultations_router
from ai_engine.infrastructure.clients.qwen_audio_client import QwenAudioClient
from ai_engine.infrastructure.vad.voice_activity_detector import VoiceActivityDetector

# ---------------------------------------------------------------------------
# DI container (module-level singletons assembled at startup)
# ---------------------------------------------------------------------------
_use_case: ProcessAudioUseCase | None = None


def get_process_audio_use_case() -> ProcessAudioUseCase:
    """Return the singleton ProcessAudioUseCase; raises if not yet initialised."""
    if _use_case is None:
        raise RuntimeError("Application has not been initialised. Call create_app() first.")
    return _use_case


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Wire dependencies on startup; nothing to tear down for MVP."""
    global _use_case  # noqa: PLW0603

    load_dotenv()

    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "DASHSCOPE_API_KEY environment variable is not set. "
            "Copy .env.example to .env and fill in your key."
        )
    dashscope.api_key = api_key

    client = QwenAudioClient()
    _use_case = ProcessAudioUseCase(
        vad=VoiceActivityDetector(),
        extractor=MedicalExtractor(client),
        reporter=MedicalReporter(),
    )

    yield
    # Nothing to clean up for MVP.


def create_app() -> FastAPI:
    app = FastAPI(
        title="Vina Doctor — AI Engine",
        description=(
            "Medical consultation audio processing service. "
            "Accepts audio uploads and returns multilingual SOAP reports via Qwen2-Audio."
        ),
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(consultations_router)

    return app


app = create_app()

