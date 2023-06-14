import requests

def get_api_key():
    return open("src/apikey.txt", "r").read()

def fetch_response(api_key: str, model: str, chat_history:list):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model,
            "messages": chat_history,
            "temperature": 0.8,
            "max_tokens": 200,
        },
        timeout=10,
    ).json()
    return response["choices"][0]["message"]["content"].strip()
