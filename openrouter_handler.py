import requests
import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_openrouter(prompt: str) -> str:
    headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://oab-fastapi-backend.onrender.com",
    "X-Title": "OAB-Tracker"
    }


    data = {
        "model": "openai/gpt-3.5-turbo",  # or another free/added model
        "messages": [
            {
                "role": "system",
                "content": "You're a health assistant trained to provide advice for Overactive Bladder (OAB) based on patterns in daily logs. Suggest simple lifestyle techniques like bladder training, timed voiding, and breathing or pelvic exercises."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        print("Response JSON:", response.json())
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error:", e)
        return "Error generating response from AI. Please try again later."

