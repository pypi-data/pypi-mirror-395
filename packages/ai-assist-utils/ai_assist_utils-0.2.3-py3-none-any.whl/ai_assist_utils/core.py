import google.generativeai as genai
import os

def get_response(prompt, api_key=None, model="gemini-2.5-flash"):
    """
    Sends a prompt to Google Gemini and returns the response.

    Args:
        prompt (str): The input text to send to the AI.
        api_key (str, optional): Gemini API key. If not provided, looks for GEMINI_API_KEY env var.
        model (str, optional): The model to use. Defaults to "gemini-pro".

    Returns:
        str: The AI's response text.
    """
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return "Error: API key not provided and GEMINI_API_KEY environment variable not set."

    try:
        genai.configure(api_key=api_key)
        model_instance = genai.GenerativeModel(model)
        response = model_instance.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with AI: {str(e)}"

def summarize_text(text, api_key=None):
    """
    Summarizes a long text using AI.

    Args:
        text (str): The text to summarize.
        api_key (str, optional): Gemini API key.

    Returns:
        str: The summary of the text.
    """
    prompt = f"Please summarize the following text:\n\n{text}"
    return get_response(prompt, api_key=api_key)

def format_response(text):
    """
    Cleans or processes AI output before displaying.
    
    - Removes leading/trailing whitespace.

    Args:
        text (str): The raw text from AI.

    Returns:
        str: Cleaned text.
    """
    if not text:
        return ""
    
    return text.strip()
