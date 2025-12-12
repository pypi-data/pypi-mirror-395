import os
import openai

def get_response(prompt):
    """
    Sends a prompt to an AI tool and returns the response.

    Usage:
    >>> get_response("Hello AI")
    'Hello! How can I help you today?'
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "API key not found! Please set OPENAI_API_KEY in your environment."
    
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def summarize_text(text):
    """
    Summarizes a long text using AI.

    Usage:
    >>> summarize_text("Long text here...")
    'Summary of the text.'
    """
    prompt = f"Summarize the following text:\n{text}"
    return get_response(prompt)


def format_response(text):
    """
    Cleans AI output for display.

    Usage:
    >>> format_response('Hello\\nWorld')
    'Hello World'
    """
    return text.replace("\n", " ").strip()

