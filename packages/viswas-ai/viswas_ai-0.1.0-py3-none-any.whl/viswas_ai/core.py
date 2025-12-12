import requests

def get_response(prompt):
    """
    Send a prompt to an AI API and return the response text.
    Replace <YOUR_API_KEY> and <API_URL> with your service details.
    """
    api_url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer <YOUR_API_KEY>"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(api_url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]


def summarize_text(text):
    """
    Summarize long text using AI.
    """
    return get_response(f"Summarize this:\n{text}")


def format_response(text):
    """
    Format AI text before displaying.
    Removes extra whitespace.
    """
    return text.strip()
