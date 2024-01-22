import requests
import os
def ask_chat(prompt, temperature=1):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + os.getenv("OPENAI_API_KEY"),
    }
    json_data = {
        'model': 'gpt-3.5-turbo',
        'temperature': temperature,
        'messages': [{
                'role': 'user',
                'content': prompt
            }
        ],
    }

    r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json_data)
    if (r.status_code != 200):
        return "⛔ Error from OpenAI API: \n"+r.text
    text = r.json()["choices"][0]["message"]["content"]
    return text

