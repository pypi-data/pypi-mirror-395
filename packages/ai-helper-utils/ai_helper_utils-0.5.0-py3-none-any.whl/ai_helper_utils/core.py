import random

import google.generativeai as genai

def get_response(prompt, api_key=None):
    """
    Sends a prompt to the Gemini 2.5 Flash model and returns the response.
    Requires a valid API key.
    """
    if not prompt:
        return "Please provide a prompt."

    if not api_key:
        return "Error: API Key is missing. Please provide a valid Gemini API Key."

    try:
        genai.configure(api_key=api_key)
        # Using the requested model version.
        model = genai.GenerativeModel('gemini-2.5-flash') 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini: {str(e)}"

def summarize_text(text, api_key=None):
    """
    Summarizes the text using Gemini if api_key is provided, otherwise uses simple truncation.
    """
    if not text:
        return ""
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(f"Summarize this text: {text}")
            return response.text
        except Exception as e:
            return f"Error summarizing with Gemini: {str(e)}"

    words = text.split()
    if len(words) <= 10:
        return text # Too short to summarize
        
    summary = " ".join(words[:10]) + "..."
    return f"Summary: {summary}"

def format_response(text):
    """
    Cleans or processes AI output before displaying.
    For example, converting newlines to HTML breaks or stripping whitespace.
    """
    if not text:
        return ""
    
    formatted = text.strip()
    # Simple formatting: capitalize first letter
    if formatted:
        formatted = formatted[0].upper() + formatted[1:]
        
    return formatted
