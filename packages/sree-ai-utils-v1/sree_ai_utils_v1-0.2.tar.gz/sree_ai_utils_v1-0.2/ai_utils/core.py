import google.generativeai as genai

def get_response(prompt, api_key):
    """
    Sends a prompt to Google Gemini and returns the text response.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def summarize_text(text, api_key):
    """
    Summarizes a long text using AI.
    """
    try:
        prompt = f"Please summarize the following text efficiently:\n\n{text}"
        return get_response(prompt, api_key)
    except Exception as e:
        return f"Error summarizing: {str(e)}"

def format_response(text):
    """
    Clean or process AI output before displaying.
    """
    if text:
        # Removes asterisks often used by AI for bolding to keep text clean
        clean_text = text.replace("**", "").replace("##", "")
        return clean_text.strip()
    return "No response generated."