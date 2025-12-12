import google.generativeai as genai

def configure(api_key):
    """
    Configure the Gemini client with your API key.
    """
    genai.configure(api_key=api_key)


def get_response(prompt):
    """
    Sends a prompt to Gemini and returns the generated text.
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text


def summarize_text(text):
    """
    Summarizes long text using Gemini.
    """
    prompt = f"Summarize the following text:\n\n{text}"
    return get_response(prompt)


def format_response(text):
    """
    Cleans the AI output.
    """
    return text.strip().replace("\n", "<br>")
