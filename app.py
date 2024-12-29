from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
from datetime import datetime

app = FastAPI()

# In-memory storage
health_data: Dict = {}

class HealthData(BaseModel):
    data: Dict[str, Dict[str, str]]

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

def analyze_health_data(message: str) -> str:
    """
    Analyze health data based on the user's message and return a relevant response.
    This is a simple implementation - you can enhance it based on your needs.
    """
    message = message.lower()
    
    if not health_data:
        return "No health data available to analyze. Please upload data first."
    
    # Get the dates sorted in descending order
    dates = sorted(health_data.keys(), reverse=True)
    
    if "steps" in message or "walking" in message:
        response = "Here's your step count data:\n"
        for date in dates:
            if "Step Count" in health_data[date]:
                response += f"{date}: {health_data[date]['Step Count']}\n"
        return response
    
    elif "sleep" in message:
        response = "Here's your sleep data:\n"
        for date in dates:
            if "Sleep" in health_data[date]:
                response += f"{date}: {health_data[date]['Sleep']}\n"
        return response
    
    elif "heart" in message or "heart rate" in message:
        response = "Here's your heart rate data:\n"
        for date in dates:
            if "Heart Rate" in health_data[date]:
                response += f"{date}: {health_data[date]['Heart Rate']}\n"
        return response
    
    elif "energy" in message or "calories" in message:
        response = "Here's your active energy data:\n"
        for date in dates:
            if "Active Energy" in health_data[date]:
                response += f"{date}: {health_data[date]['Active Energy']}\n"
        return response
    
    elif "summary" in message or "overview" in message:
        response = "Here's your latest health data summary:\n"
        if dates:
            latest_date = dates[0]
            response += f"Date: {latest_date}\n"
            for metric, value in health_data[latest_date].items():
                response += f"{metric}: {value}\n"
        return response
    
    return "I understand you're asking about your health data. Could you please be more specific? You can ask about steps, sleep, heart rate, or energy expenditure."

@app.post("/upload")
async def upload_health_data(data: HealthData):
    """
    Upload health data and replace existing data in memory.
    """
    global health_data
    health_data = data.data
    return {"message": "Data uploaded successfully", "data_points": len(health_data)}

@app.post("/chat")
async def chat(message: ChatMessage):
    """
    Process a chat message and return a response based on the health data.
    """
    if not message.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    response = analyze_health_data(message.message)
    return ChatResponse(response=response)

@app.get("/")
async def root():
    """
    Root endpoint to check if the API is running.
    """
    return {"status": "Health Data Chat API is running", "data_available": bool(health_data)}