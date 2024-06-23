import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class GeminiAdapter:
    def __init__(self):
        if os.environ.get("GOOGLE_API_KEY") is None:
            raise ValueError("GOOGLE_API_KEY is not set")
        genai.configure(
            api_key=os.environ.get("GOOGLE_API_KEY"),
        )
        self.gemini = genai.GenerativeModel("gemini-1.5-pro")

    def generate(self, prompt: str, max_new_tokens: int = 100) -> str:
        response = self.gemini.generate_content(
            f"{prompt}",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_new_tokens,
            ),
        )
        return response.text


if __name__ == "__main__":
    adapter = GeminiAdapter()
    print(adapter.generate("こんにちは"))
