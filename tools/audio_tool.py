from utils.groq_client import transcribe_audio as _transcribe


def process_audio(audio_bytes: bytes, filename: str = "audio.wav") -> dict:
    """
    Transcribe audio using Groq Whisper.
    Returns dict with 'text', 'language', 'needs_hitl'.
    """
    try:
        text, language = _transcribe(audio_bytes, filename)

        if not text or len(text.strip()) < 5:
            return {
                "text": text or "",
                "language": language,
                "needs_hitl": True,
                "error": "Transcription too short or empty"
            }

        # Heuristic: if transcript looks garbled (too many non-alpha chars), flag HITL
        alpha_ratio = sum(c.isalpha() or c.isspace() or c.isdigit() for c in text) / max(len(text), 1)
        needs_hitl = alpha_ratio < 0.7

        return {
            "text": text.strip(),
            "language": language,
            "needs_hitl": needs_hitl,
            "error": None
        }
    except Exception as e:
        return {
            "text": "",
            "language": "unknown",
            "needs_hitl": True,
            "error": str(e)
        }
