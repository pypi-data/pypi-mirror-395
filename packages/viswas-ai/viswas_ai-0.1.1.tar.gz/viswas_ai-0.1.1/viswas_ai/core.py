import requests

class ViswasAI:
    """
    Main class for interacting with an AI service.
    Usage:
        bot = ViswasAI(api_key="YOUR_API_KEY")
        response = bot.get_response("Hello AI")
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def get_response(self, prompt):
        """
        Send a prompt to the AI and return the response text.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(self.api_url, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]

    def summarize_text(self, text):
        """
        Summarize a long text using AI.
        """
        return self.get_response(f"Summarize this:\n{text}")

    def format_response(self, text):
        """
        Clean or format AI response.
        """
        return text.strip()
