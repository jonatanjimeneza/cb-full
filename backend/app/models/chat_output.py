from pydantic import BaseModel

class ChatOutput(BaseModel):
    message: str
    sender_name: str = "AI"