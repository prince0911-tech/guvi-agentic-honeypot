from pydantic import BaseModel
from typing import Optional, Dict, Any

class Message(BaseModel):
    sender: str
    text: str
    timestamp: Optional[str] = None

class HoneypotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[Any] = None
    metadata: Optional[Dict[str, Any]] = None
