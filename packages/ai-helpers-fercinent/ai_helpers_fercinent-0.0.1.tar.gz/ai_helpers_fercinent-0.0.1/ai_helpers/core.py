import requests

def get_response(prompt, api_key):
    """
    Send a prompt to an AI text generation API and return the reply.
    
    Args:
        prompt (str): The user's text input.
        api_key (str): Your AI service API key.
    
    Returns:
        str: AI-generated response.
    """
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        return f"Error: {response.text}"

    return response.json()["choices"][0]["message"]["content"]
