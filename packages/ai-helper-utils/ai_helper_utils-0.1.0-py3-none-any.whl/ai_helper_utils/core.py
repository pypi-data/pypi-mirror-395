import random

def get_response(prompt, api_key=None):
    """
    Simulates sending a prompt to an AI tool and returning a response.
    If api_key is provided, it would ideally make a real API call.
    For this demo, we'll use a mock response or a simple echo if no key is present.
    """
    if not prompt:
        return "Please provide a prompt."

    # Mock responses for demonstration
    mock_responses = [
        f"That's an interesting question about '{prompt}'. Here is a generated answer.",
        f"I can certainly help with '{prompt}'. The solution involves...",
        f"Thinking about '{prompt}'... It seems complex but manageable.",
        f"AI says: '{prompt}' is a great topic!",
    ]
    
    # In a real scenario, you would use requests to call an API like OpenAI
    # if api_key:
    #     headers = {"Authorization": f"Bearer {api_key}"}
    #     response = requests.post("https://api.openai.com/v1/...", json={"prompt": prompt}, headers=headers)
    #     return response.json().get("choices")[0].get("text")

    return random.choice(mock_responses)

def summarize_text(text):
    """
    Simulates summarizing a long text.
    """
    if not text:
        return ""
    
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
