import google.generativeai as genai
import markdown
import os

def configure_api(api_key):
    """
    Configures the Google Gemini API key.
    
    Args:
        api_key (str): The API key for Google Gemini.
    """
    if not api_key:
        raise ValueError("API Key must be provided.")
    genai.configure(api_key=api_key)

def get_response(prompt, api_key=None, model_name="gemini-2.5-flash-lite"):
    """
    Sends a prompt to the AI tool and returns the response.
    
    Args:
        prompt (str): The user's input query.
        api_key (str, optional): API key if not already configured globally.
        model_name (str): The model to use. Defaults to "gemini-pro".
        
    Returns:
        str: The generated text response from the AI.
    """
    if api_key:
        configure_api(api_key)
        
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def summarize_text(text, api_key=None):
    """
    Summarizes a long text using AI.
    
    Args:
        text (str): The text to summarize.
        api_key (str, optional): API key if not already configured globally.
        
    Returns:
        str: The summary of the text.
    """
    prompt = f"Please summarize the following text:\n\n{text}"
    return get_response(prompt, api_key)

def format_response(text):
    """
    Cleans or processes AI output before displaying.
    Converts Markdown to HTML for web display.
    
    Args:
        text (str): The raw text from the AI (likely Markdown).
        
    Returns:
        str: HTML formatted text.
    """
    if not text:
        return ""
    
    # Convert markdown to HTML
    html_content = markdown.markdown(text)
    return html_content
