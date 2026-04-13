from pathlib import Path

# Minimum file size (bytes) considered to contain real audio content.
_MIN_AUDIO_SIZE_BYTES = 1_024  # 1 KB


class VADError(Exception):
    """Raised when a file fails the voice-activity check."""


class VoiceActivityDetector:
    """Lightweight, dependency-free VAD based on file-size heuristics.

    Good enough for MVP: rejects empty uploads or stub files before they
    hit the (paid) Qwen API.  Can be swapped for a proper webrtcvad or
    silero-vad implementation later without touching callers.
    """

    def __init__(self, min_size_bytes: int = _MIN_AUDIO_SIZE_BYTES) -> None:
        self._min_size = min_size_bytes

    def check(self, audio_path: Path) -> None:
        """Verify that *audio_path* likely contains real audio content.

        Raises:
            VADError: if the file is missing, empty, or too small.
        """
        if not audio_path.exists():
            raise VADError(f"Audio file not found: {audio_path}")

        size = audio_path.stat().st_size
        if size < self._min_size:
            raise VADError(
                f"Audio file is too small ({size} bytes, minimum {self._min_size} bytes). "
                "The file appears to be empty or corrupted."
            )
