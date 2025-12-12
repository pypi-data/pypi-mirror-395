import requests

class ViswasAI:
    """
    AI helper class using Google Gemini API.
    """

    def __init__(self, api_key, model_name="gemini-2.0-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"

    def get_response(self, prompt):
        """
        Send a prompt to Gemini and return the response text.
        Handles errors gracefully and prints debug info.
        """
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }

        data = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        try:
            resp = requests.post(self.api_url, headers=headers, json=data)
            resp_json = resp.json()

            # Debug: print full response
            print("DEBUG: Full API response:", resp_json)

            # Handle API error
            if resp.status_code != 200 or "error" in resp_json:
                return f"API Error: {resp_json.get('error', {}).get('message', resp_json)}"

            # Extract the first candidate text
            candidates = resp_json.get("candidates")
            if not candidates:
                return "No candidates in response"
            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            if not parts:
                return "No content parts in response"
            text = parts[0].get("text", "")
            return text

        except Exception as e:
            return f"Exception occurred: {str(e)}"

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
