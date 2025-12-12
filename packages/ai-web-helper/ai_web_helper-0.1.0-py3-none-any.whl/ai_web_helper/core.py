import google.generativeai as genai
import markdown

def get_response(prompt: str, api_key: str) -> str:
    """
    Sends a prompt to the AI tool (Google Gemini) and returns the response.

    Args:
        prompt (str): The user's input query.
        api_key (str): The API key for Google Gemini.

    Returns:
        str: The generated response from the AI.
    """
    if not api_key:
        return "Error: API Key is missing."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def summarize_text(text: str, api_key: str) -> str:
    """
    Summarizes a long text using AI.

    Args:
        text (str): The text to summarize.
        api_key (str): The API key for Google Gemini.

    Returns:
        str: The summary of the text.
    """
    prompt = f"Please summarize the following text:\n\n{text}"
    return get_response(prompt, api_key)

def format_response(text: str) -> str:
    """
    Cleans or processes AI output before displaying.
    Converts Markdown to HTML for better display in the web app.

    Args:
        text (str): The raw text response from the AI.

    Returns:
        str: The formatted HTML string.
    """
    try:
        # Convert markdown to HTML
        html_content = markdown.markdown(text)
        return html_content
    except Exception as e:
        return f"Error formatting response: {str(e)}"
