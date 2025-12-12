import requests

def get_response(prompt, api_key):
    """Send a prompt to an AI API and return the response text."""
    url = "https://api.openai.com/v1/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": prompt,
        "max_tokens": 200
    }

    r = requests.post(url, json=data, headers=headers)
    return r.json()["choices"][0]["text"]


def summarize_text(text):
    """Return a short summary."""
    return text[:100] + "..."


def format_response(text):
    """Clean whitespace and formatting."""
    return text.strip()
