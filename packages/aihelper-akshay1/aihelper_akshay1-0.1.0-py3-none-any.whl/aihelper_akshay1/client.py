from google import genai

class GeminiClient:
    """
    A simple client wrapper for Google Gemini API.
    API key must be passed securely from outside.
    """

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash-exp"   # FREE MODEL

    def get_response(self, prompt: str) -> str:
        """Generate text using Gemini."""
        if not prompt.strip():
            return "Error: Empty prompt."

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text

    def summarize_text(self, text: str) -> str:
        """Summarize a long text using Gemini."""
        prompt = f"Summarize this text in simple terms:\n\n{text}"
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text
