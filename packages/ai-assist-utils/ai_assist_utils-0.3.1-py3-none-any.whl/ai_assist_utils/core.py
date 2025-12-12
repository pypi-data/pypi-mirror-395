import os
import google.generativeai as genai


def get_response(prompt, api_key=None, model="gemini-2.0-flash"):
    """Send a prompt to Google Gemini and return the response."""
    
    # Prefer parameter → fallback to environment variable
    api_key = api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: No API key provided."

    try:
        genai.configure(api_key=api_key)
        model_obj = genai.GenerativeModel(model)
        response = model_obj.generate_content(prompt)
        return response.text or "AI returned no text."
    except Exception as e:
        return f"Error communicating with AI: {e}"


def summarize_text(text, api_key=None):
    """Return a summarized version of the given text."""
    prompt = f"Summarize the following text:\n\n{text}"
    return get_response(prompt, api_key)


def format_response(text):
    """Remove unnecessary whitespace from AI output."""
    return text.strip() if text else ""
