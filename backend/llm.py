from functools import lru_cache
from google import genai

from backend.config import GEMINI_API_KEY, MODEL_NAME


@lru_cache(maxsize=1)
def get_gemini_client():
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Please add GEMINI_API_KEY or GOOGLE_API_KEY to your .env file."
        )
    return genai.Client(api_key=GEMINI_API_KEY)


class GeminiLLM:

    def __init__(self):
        self.client = get_gemini_client()

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini Error: {e}") from e