import openai
import os

def get_response(prompt, api_key=None, model="gpt-3.5-turbo"):
    """
    Sends a prompt to an AI tool (OpenAI) and returns the response.

    Args:
        prompt (str): The input text to send to the AI.
        api_key (str, optional): OpenAI API key. If not provided, looks for OPENAI_API_KEY env var.
        model (str, optional): The model to use. Defaults to "gpt-3.5-turbo".

    Returns:
        str: The AI's response text.
    """
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return "Error: API key not provided and OPENAI_API_KEY environment variable not set."

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error communicating with AI: {str(e)}"

def summarize_text(text, api_key=None):
    """
    Summarizes a long text using AI.

    Args:
        text (str): The text to summarize.
        api_key (str, optional): OpenAI API key.

    Returns:
        str: The summary of the text.
    """
    prompt = f"Please summarize the following text:\n\n{text}"
    return get_response(prompt, api_key=api_key)

def format_response(text):
    """
    Cleans or processes AI output before displaying.
    
    - Removes leading/trailing whitespace.
    - Standardizes line breaks.

    Args:
        text (str): The raw text from AI.

    Returns:
        str: Cleaned text.
    """
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    cleaned = text.strip()
    
    # Replace multiple newlines with a single one (optional simplification)
    # cleaned = "\n".join([line.strip() for line in cleaned.splitlines() if line.strip()])
    
    return cleaned
