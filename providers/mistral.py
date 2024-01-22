import requests
import os
def ask_mistral(prompt, max_tokens, temperature=1):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + os.getenv("MISTRAL_API_KEY"),
    }
    json_data = {
        'model': 'mistral-small',
        'max_tokens': max_tokens,
        'temperature': 1,
        'messages': [{
                'role': 'user',
                'content': prompt
            }
        ],
    }

    r = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=json_data)
    text = r.json()["choices"][0]["message"]["content"]
    return text

