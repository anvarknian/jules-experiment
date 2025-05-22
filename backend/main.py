import os
import requests
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Environment and API Configuration ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL")
DEFAULT_MODEL =  os.getenv("DEFAULT_MODEL")

# --- Pydantic Models ---
class ChatMessage(BaseModel):
    message: str = Field(..., example="Hello, how are you?")

class ChatResponse(BaseModel):
    reply: str | None = None
    error: str | None = None

# --- FastAPI ---
app = FastAPI()

# --- Root Endpoint ---
@app.get("/")
async def root():
    return {"message": "Chat API is running. POST to /chat with a message."}

# --- Chat Endpoint ---
@app.post("/chat", response_model=ChatResponse)
async def chat_with_openrouter(chat_message: ChatMessage):
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="OpenRouter API key not configured.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "user", "content": chat_message.message}
        ]
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        
        response_data = response.json()
        
        if response_data.get("choices") and len(response_data["choices"]) > 0:
            assistant_reply = response_data["choices"][0].get("message", {}).get("content")
            if assistant_reply:
                return ChatResponse(reply=assistant_reply)
            else:
                # Log unexpected response structure
                print(f"Unexpected response structure: {response_data}")
                raise HTTPException(status_code=500, detail="Could not parse assistant's reply from API response.")
        else:
            # Log unexpected response structure
            print(f"No choices found in API response: {response_data}")
            raise HTTPException(status_code=500, detail="No choices found in API response.")

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Request to OpenRouter API timed out.")
    except requests.exceptions.RequestException as e:
        # Log the error from requests
        print(f"Error calling OpenRouter API: {e}")
        # Check for specific status codes if available in the exception (e.g. e.response.status_code)
        status_code = e.response.status_code if hasattr(e, 'response') and e.response is not None else 500
        error_detail = f"Error communicating with OpenRouter API: {e}"
        if hasattr(e, 'response') and e.response is not None and e.response.text:
            error_detail = f"Error from OpenRouter API ({e.response.status_code}): {e.response.text}"
        
        # If it's an auth error from OpenRouter, it often returns 401
        if status_code == 401:
             raise HTTPException(status_code=401, detail="Authentication error with OpenRouter API. Check your API key.")

        raise HTTPException(status_code=status_code, detail=error_detail)
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
