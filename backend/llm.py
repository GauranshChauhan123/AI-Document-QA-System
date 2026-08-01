from google import genai

from backend.config import GEMINI_API_KEY, MODEL_NAME

client = genai.Client(api_key=GEMINI_API_KEY)


class GeminiLLM:

    def generate(self,prompt):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            return response.text

        except Exception as e:

            raise RuntimeError(
                f"Gemini Error : {e}"
            )