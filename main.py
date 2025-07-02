from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LogData(BaseModel):
    logs: list

@app.post("/analyze")
def analyze(logs: LogData):
    return {"message": "Received logs", "count": len(logs.logs)}
