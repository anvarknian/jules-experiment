from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# --- Base Models ---
class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    content: str
    sender_type: str # 'user' or 'ai'

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    chat_id: int
    created_at: datetime
    token_usage: Optional[int] = None

    class Config:
        orm_mode = True

class ChatBase(BaseModel):
    title: Optional[str] = None

class ChatCreate(ChatBase):
    user_id: int # User ID must be provided when creating a chat

class Chat(ChatBase):
    id: int
    user_id: int
    created_at: datetime
    messages: List[Message] = []

    class Config:
        orm_mode = True

# --- API Specific Schemas ---
class ChatCompletionRequest(BaseModel):
    message: str = Field(..., example="Hello, how are you?")
    user_id: int = Field(1, description="ID of the user sending the message. For now, defaults to 1.")
    chat_id: Optional[int] = Field(None, description="ID of the existing chat session. If None, a new chat will be created.")

class ChatCompletionResponse(BaseModel):
    reply: Optional[str] = None
    chat_id: int
    user_message_id: int
    ai_message_id: Optional[int] = None
    error: Optional[str] = None

class UsageBase(BaseModel):
    tokens_used: int

class UsageCreate(UsageBase):
    user_id: int

class Usage(UsageBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class LogBase(BaseModel):
    level: str
    message: str

class LogCreate(LogBase):
    pass

class Log(LogBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
