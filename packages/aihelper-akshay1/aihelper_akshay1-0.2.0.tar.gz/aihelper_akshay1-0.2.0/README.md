# aihelper_akshay1

A simple Python library that uses **Google Gemini API** for:
- Text generation
- Summarization
- Output formatting

## Installation


## Usage
```python
from aihelper_akshay1 import GeminiClient, format_response

client = GeminiClient(api_key="YOUR_API_KEY")

response = client.get_response("Explain AI in 2 lines.")
print(format_response(response))
