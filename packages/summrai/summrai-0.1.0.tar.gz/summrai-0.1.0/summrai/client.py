import requests

class AIClient:
    """
    AI Client using Google Gemini (FREE).
    API key must be passed manually for security.
    """

    def __init__(self, api_key, model="gemini-2.0-flash"):
        if not api_key:
            raise ValueError("API key required. Pass api_key='YOUR_KEY'.")
        
        self.api_key = api_key
        self.model = model

        # OpenAI-compatible Gemini endpoint (free)
        self.url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"

    def get_response(self, prompt, max_tokens=300):
        """
        Sends a prompt to the AI model and returns its output.
        """

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }

        response = requests.post(self.url, json=body, headers=headers)
        
        data = response.json()

        return data["choices"][0]["message"]["content"].strip()
