import os
from groq import Groq

_client = None

def get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"]
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment")
        _client = Groq(api_key=api_key)
    return _client


def chat(messages: list, model: str = "llama-3.3-70b-versatile", temperature: float = 0.2, max_tokens: int = 2048) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def transcribe_audio(audio_bytes: bytes, filename: str = "audio.wav") -> str:
    client = get_client()
    transcription = client.audio.transcriptions.create(
        file=(filename, audio_bytes, "audio/wav"),
        model="whisper-large-v3",
        response_format="verbose_json",
    )
    return transcription.text, getattr(transcription, "language", "en")
