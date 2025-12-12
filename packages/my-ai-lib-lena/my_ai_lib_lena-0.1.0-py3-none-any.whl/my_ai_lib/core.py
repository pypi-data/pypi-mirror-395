import requests
import os

def get_response(prompt):
    """
    Send a prompt to an AI model and return the generated response.

    Parameters:
        prompt (str): The text prompt to send.

    Returns:
        str: The AI-generated response text.
    """

    API_KEY = os.getenv("AI_API_KEY")
    if not API_KEY:
        return "Error: API Key not found. Set AI_API_KEY as an environment variable."

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"


def summarize_text(text):
    """
    Generate a simple summary of the text.
    (This is a placeholder for optional AI-based summarization.)

    Parameters:
        text (str): The long text to summarize.

    Returns:
        str: Summary text.
    """

    if len(text) < 50:
        return "Text too short to summarize."

    return text[:120] + "..."


def format_response(text):
    """
    Clean the AI output before sending to UI.
    """

    if not isinstance(text, str):
        return ""

    # remove extra spaces and fix capitalization
    return text.strip().capitalize()
