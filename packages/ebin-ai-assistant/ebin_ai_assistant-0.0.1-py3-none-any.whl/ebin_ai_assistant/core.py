import re
import google.generativeai as genai

_api_configured = False

def configure_api(api_key: str):
    """
    Configures the Gemini API with the provided API key.
    
    Args:
        api_key (str): The Google Gemini API key.
    """
    global _api_configured
    genai.configure(api_key=api_key)
    _api_configured = True

def get_response(prompt: str, model_name: str = 'gemini-pro') -> str:
    """
    Sends a prompt to the Gemini API and returns the response.
    
    Args:
        prompt (str): The input prompt.
        model_name (str): The model to use (default: 'gemini-pro').
        
    Returns:
        str: The text response from the AI.
        
    Raises:
        RuntimeError: If the API has not been configured.
    """
    if not _api_configured:
        raise RuntimeError("API not configured. Call configure_api(api_key) first.")
        
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

def summarize_text(text: str) -> str:
    """
    Summarizes a long text using the Gemini API.
    
    Args:
        text (str): The text to summarize.
        
    Returns:
        str: A summary of the text.
    """
    prompt = f"Please summarize the following text:\n\n{text}"
    return get_response(prompt)

def format_response(text: str) -> str:
    """
    Cleans or processes AI output before displaying.
    
    Args:
        text (str): The raw AI output.
        
    Returns:
        str: The formatted output.
    """

    prompt = f"Please format the following text to be clean, professional, and well-structured:\n\n{text}"
    return get_response(prompt)
