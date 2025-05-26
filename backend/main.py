import os
import requests
from fastapi import FastAPI, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func # for server_default=func.now() in models if not already there
from dotenv import load_dotenv
from typing import List, Optional
from datetime import datetime

# Alembic imports for running migrations on startup
from alembic.config import Config as AlembicConfig
from alembic import command as alembic_command

from . import models, schemas
from .database import SessionLocal, engine, get_db, DATABASE_URL

# Ensure models create tables if they don't exist (though Alembic handles this)
# models.Base.metadata.create_all(bind=engine) # This is generally handled by Alembic migrations now

# Load environment variables from .env file
load_dotenv()

# --- Environment and API Configuration ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions") # Default if not set
DEFAULT_MODEL =  os.getenv("DEFAULT_MODEL", "gryphe/mythomax-l2-13b") # Default if not set


# --- FastAPI ---
app = FastAPI(title="Chat API with PostgreSQL", version="1.0")

# --- Alembic Configuration for Startup Migrations ---
# This is for development convenience. In production, you might run migrations manually or differently.
@app.on_event("startup")
def run_migrations():
    if DATABASE_URL is None: # Should have been caught by database.py but double check
        print("DATABASE_URL is not set. Skipping migrations.")
        return
    
    alembic_cfg_path = os.path.join(os.path.dirname(__file__), "..", "alembic.ini") # Assuming alembic.ini is in project root
    # If alembic.ini is in backend/ adjust path to "alembic.ini"
    # For this project, alembic.ini will be in backend/ so use "alembic.ini"
    alembic_cfg_path_backend = "alembic.ini" # alembic init alembic was run in backend/
    
    # Check if alembic.ini exists in backend/
    if not os.path.exists(alembic_cfg_path_backend):
        print(f"Alembic config not found at {alembic_cfg_path_backend}. Skipping migrations.")
        # Attempt to find it in the root, just in case structure changes
        if os.path.exists(alembic_cfg_path):
             alembic_cfg_path_backend = alembic_cfg_path
             print(f"Found alembic.ini at {alembic_cfg_path_backend}")
        else:
            print(f"Also not found at {alembic_cfg_path}. Skipping migrations.")
            return

    print(f"Running Alembic migrations from config: {alembic_cfg_path_backend}")
    alembic_cfg = AlembicConfig(alembic_cfg_path_backend)
    
    # Make sure Alembic can find your models, typically by setting script_location
    # and ensuring env.py points to your Base.metadata
    # If alembic commands are run from backend/, script_location might not be needed in alembic.ini
    # or it should be relative to backend/ (e.g. script_location = alembic)

    try:
        alembic_command.upgrade(alembic_cfg, "head")
        print("Migrations applied successfully.")
    except Exception as e:
        print(f"Error applying migrations: {e}")
        # Depending on the error, you might want to prevent app startup
        # For example, if it's a sqlalchemy.exc.OperationalError, the DB might not be reachable


# --- Helper for Logging ---
def create_log_entry(db: Session, level: str, message: str):
    log_entry = models.Log(level=level, message=message, timestamp=datetime.utcnow())
    db.add(log_entry)
    db.commit()


# --- Root Endpoint ---
@app.get("/")
async def root():
    return {"message": "Chat API is running. POST to /api/v1/chat with a message."}

# --- API Endpoints ---
API_V1_PREFIX = "/api/v1"

@app.post(f"{API_V1_PREFIX}/chat", response_model=schemas.ChatCompletionResponse)
async def chat_endpoint(
    request_data: schemas.ChatCompletionRequest, 
    db: Session = Depends(get_db)
):
    if not OPENROUTER_API_KEY:
        create_log_entry(db, "ERROR", "OpenRouter API key not configured.")
        raise HTTPException(status_code=500, detail="OpenRouter API key not configured.")

    # 1. User Handling
    user = db.query(models.User).filter(models.User.id == request_data.user_id).first()
    if not user:
        # For now, create a user if not found. In a real app, this would be part of user management.
        user = models.User(id=request_data.user_id, username=f"user_{request_data.user_id}")
        db.add(user)
        # db.commit() # Commit separately or together with other changes
        # db.refresh(user) # Refresh to get defaults like created_at
        create_log_entry(db, "INFO", f"User with ID {request_data.user_id} not found, created new user.")
        # Not committing here, will commit along with message and chat

    # 2. Chat Session Handling
    chat_session: Optional[models.Chat] = None
    if request_data.chat_id:
        chat_session = db.query(models.Chat).filter(models.Chat.id == request_data.chat_id, models.Chat.user_id == user.id).first()
        if not chat_session:
            create_log_entry(db, "ERROR", f"Chat session {request_data.chat_id} not found for user {user.id}.")
            raise HTTPException(status_code=404, detail=f"Chat session not found.")
    else:
        chat_session = models.Chat(user_id=user.id, title=f"Chat on {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}")
        db.add(chat_session)
        # db.flush() # Flush to get chat_session.id before using it for messages
        # create_log_entry(db, "INFO", f"New chat session created for user {user.id} with ID {chat_session.id}.")
        # Not committing here, will commit along with message

    try:
        # Ensure chat_session is not None (for type checkers)
        if chat_session is None : # Should not happen due to logic above
            create_log_entry(db, "ERROR", "Chat session is unexpectedly None.")
            raise HTTPException(status_code=500, detail="Internal error: Chat session not initialized.")
        
        db.flush() # Ensure user and chat are in session and have IDs if new

        # 3. Store User Message
        user_message = models.Message(
            chat_id=chat_session.id,
            content=request_data.message,
            sender_type="user"
        )
        db.add(user_message)
        db.flush() # Get user_message.id
        create_log_entry(db, "INFO", f"Stored user message for chat {chat_session.id}, user {user.id}.")

        # 4. Prepare messages for OpenRouter API (include history)
        history_messages = db.query(models.Message).filter(models.Message.chat_id == chat_session.id).order_by(models.Message.created_at.asc()).all()
        
        api_messages = []
        for msg in history_messages:
            api_messages.append({"role": msg.sender_type, "content": msg.content})
        # The current user message is already added to history_messages if committed before query
        # If not, ensure it's part of api_messages. The current logic adds it before querying.

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost"), # Optional, but good practice
            "X-Title": os.getenv("OPENROUTER_APP_TITLE", "FastAPI Chat App") # Optional
        }
        data = {
            "model": DEFAULT_MODEL,
            "messages": api_messages
        }

        # 5. Call OpenRouter API
        ai_message_text = None
        tokens_used = 0
        try:
            response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            response_data = response.json()

            if response_data.get("choices") and len(response_data["choices"]) > 0:
                ai_message_text = response_data["choices"][0].get("message", {}).get("content")
                if response_data.get("usage"):
                    tokens_used = response_data["usage"].get("total_tokens", 0)
            
            if not ai_message_text:
                create_log_entry(db, "ERROR", f"No valid AI reply in OpenRouter response for chat {chat_session.id}. Response: {response_data}")
                raise HTTPException(status_code=500, detail="Could not parse assistant's reply.")

        except requests.exceptions.Timeout:
            create_log_entry(db, "ERROR", f"Timeout calling OpenRouter for chat {chat_session.id}.")
            raise HTTPException(status_code=504, detail="Request to OpenRouter API timed out.")
        except requests.exceptions.RequestException as e:
            status_code = e.response.status_code if hasattr(e, 'response') and e.response is not None else 500
            error_detail = f"Error communicating with OpenRouter API: {e}"
            if hasattr(e, 'response') and e.response is not None and e.response.text:
                 error_detail = f"Error from OpenRouter API ({e.response.status_code}): {e.response.text}"
            create_log_entry(db, "ERROR", f"OpenRouter API error for chat {chat_session.id}: {error_detail}")
            if status_code == 401:
                raise HTTPException(status_code=401, detail="Authentication error with OpenRouter. Check API key.")
            raise HTTPException(status_code=status_code, detail=error_detail)

        # 6. Store AI Message and Usage
        ai_message_record = None
        if ai_message_text:
            ai_message_record = models.Message(
                chat_id=chat_session.id,
                content=ai_message_text,
                sender_type="ai",
                token_usage=tokens_used 
            )
            db.add(ai_message_record)
            create_log_entry(db, "INFO", f"Stored AI message for chat {chat_session.id}, user {user.id}.")

            if tokens_used > 0:
                usage_record = models.Usage(
                    user_id=user.id,
                    tokens_used=tokens_used
                )
                db.add(usage_record)
                create_log_entry(db, "INFO", f"Recorded {tokens_used} tokens for user {user.id}.")
            
            db.commit() # Commit all changes: user (if new), chat (if new), user_msg, ai_msg, usage
            db.refresh(user_message)
            if ai_message_record: db.refresh(ai_message_record)
            if chat_session and request_data.chat_id is None: db.refresh(chat_session) # if it's a new chat

            return schemas.ChatCompletionResponse(
                reply=ai_message_text,
                chat_id=chat_session.id,
                user_message_id=user_message.id,
                ai_message_id=ai_message_record.id if ai_message_record else None
            )
        else: # Should have been caught earlier
            db.rollback() # Rollback user message if AI failed critically post-API call
            create_log_entry(db, "ERROR", f"AI message text was empty after API call for chat {chat_session.id}, rolling back user message.")
            raise HTTPException(status_code=500, detail="AI response was empty.")

    except HTTPException as e:
        db.rollback()
        # Log is already created in most cases or not applicable for db operational errors
        raise e # Re-raise FastAPI's HTTP exceptions
    except Exception as e:
        db.rollback()
        error_msg = f"An unexpected error occurred in chat endpoint for user {request_data.user_id}, chat {request_data.chat_id}: {str(e)}"
        print(error_msg) # Print for server logs
        create_log_entry(db, "CRITICAL", error_msg)
        raise HTTPException(status_code=500, detail=f"An unexpected server error occurred.")

# Placeholder for other potential CRUD endpoints for users, chats, etc.
# For example:
# @app.post(f"{API_V1_PREFIX}/users/", response_model=schemas.User, status_code=201)
# def create_user_endpoint(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(models.User.username == user_data.username).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     new_user = models.User(username=user_data.username)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     create_log_entry(db, "INFO", f"User {new_user.username} created with ID {new_user.id}.")
#     return new_user

# @app.get(f"{API_V1_PREFIX}/chats/{{user_id}}", response_model=List[schemas.Chat])
# def get_user_chats(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user.chats

# @app.get(f"{API_V1_PREFIX}/chats/{{chat_id}}/messages", response_model=List[schemas.Message])
# def get_chat_messages(chat_id: int, db: Session = Depends(get_db)):
#     chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
#     if not chat:
#         raise HTTPException(status_code=404, detail="Chat not found")
#     return chat.messages
