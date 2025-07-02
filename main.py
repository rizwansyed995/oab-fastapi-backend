import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

app = FastAPI()

class WashroomLog(BaseModel):
    timestamp: str
    duration: str
    urgency: str
    flow: str

class LogsRequest(BaseModel):
    logs: List[WashroomLog]

@app.post("/analyze")
async def analyze_logs(data: LogsRequest):
    logs = data.logs

    prompt = f"""You are a health assistant for Overactive Bladder (OAB). Based on the following washroom log data:
    
{[log.dict() for log in logs]}

Analyze the severity of the user's OAB and suggest lifestyle-based techniques like breathing exercises, timed voiding, and pelvic floor routines. Avoid suggesting a doctor unless absolutely necessary. Output only the advice clearly.
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",  # You can change to another OpenRouter model if you want
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        advice = response.json()["choices"][0]["message"]["content"]
        return {"advice": advice}
    except Exception as e:
        return {"error heheh": str(e)}
