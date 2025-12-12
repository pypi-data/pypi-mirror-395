import requests
import os

def get_response(prompt):
    api = os.getenv("AI_API_KEY")
    headers = {"Authorization": f"Bearer {api}", "Content-Type": "application/json"}
    data = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]}
    r = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
    return r.json()["choices"][0]["message"]["content"]
