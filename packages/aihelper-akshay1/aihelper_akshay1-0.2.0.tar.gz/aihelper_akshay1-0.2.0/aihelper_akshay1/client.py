import google.generativeai as genai

class GeminiClient:
    """
    A simple client wrapper for Google Gemini API.
    API key must be passed securely from outside.
    """

    def __init__(self, api_key: str):
        # Configure Gemini API
        genai.configure(api_key=api_key)

        # FREE model
        self.model_name = "gemini-2.0-flash"
        self.model = genai.GenerativeModel(self.model_name)

    def get_response(self, prompt: str) -> str:
        """Generate text using Gemini."""
        if not prompt.strip():
            return "Error: Empty prompt."

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

    def summarize_text(self, text: str) -> str:
        """Summarize a long text using Gemini."""
        prompt = f"Summarize the following text:\n\n{text}"

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
