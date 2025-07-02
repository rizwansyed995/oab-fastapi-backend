from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from openrouter_handler import ask_openrouter

app = FastAPI()

class LogEntry(BaseModel):
    timestamp: str
    duration: str
    urgency: str
    flow: str

@app.get("/")
def home():
    return {"message": "OAB Tracker backend is running"}

@app.post("/analyze")
def analyze_logs(logs: List[LogEntry]):
    prompt = "Here are my recent washroom logs:\n"
    for log in logs:
        prompt += f"- Timestamp: {log.timestamp}, Duration: {log.duration}, Urgency: {log.urgency}, Flow: {log.flow}\n"
    prompt += "\nBased on this data, assess my OAB severity and give suggestions using breathing techniques, pelvic exercises, or routine adjustments. Avoid suggesting to consult a doctor."

    result = ask_openrouter(prompt)
    return {
        "diagnosis": result,
        "log_count": len(logs)
    }
