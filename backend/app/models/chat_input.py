from typing import Optional
from pydantic import BaseModel

class ChatInput(BaseModel):
    sender: Optional[str] = "User"
    sender_name: Optional[str] = "User"
    input_value: Optional[str] = None
    session_id: Optional[str] = None

    def build(self) -> str:
        return self.input_value or ""