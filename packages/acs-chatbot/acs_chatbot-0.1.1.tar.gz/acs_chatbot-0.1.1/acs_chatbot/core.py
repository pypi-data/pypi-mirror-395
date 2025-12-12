import os
import google.generativeai as genai

def configure_api_key(api_key: str = None):
    """
    Configure the Gemini API key.
    
    Args:
        api_key (str, optional): The API key. If None, tries to read from GEMINI_API_KEY env var.
    """
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("API key must be provided or set in GEMINI_API_KEY environment variable.")
        
    genai.configure(api_key=api_key)

def get_response(prompt: str, model_name: str = "gemini-1.5-flash") -> str:
    """
    Send a prompt to the Gemini AI and return the response.
    
    Args:
        prompt (str): The input prompt for the AI.
        model_name (str): The model to use. Defaults to "gemini-pro".
        
    Returns:
        str: The AI's response.
    """
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def summarize_text(text: str) -> str:
    """
    Summarize a long text using Gemini AI.
    
    Args:
        text (str): The text to summarize.
        
    Returns:
        str: A summary of the text.
    """
    prompt = f"Please summarize the following text:\n\n{text}"
    return get_response(prompt)

def format_response(text: str) -> str:
    """
    Clean or process AI output before displaying.
    
    Args:
        text (str): The raw AI output.
        
    Returns:
        str: The formatted text.
    """
    if not text:
        return ""
    return text.strip()
