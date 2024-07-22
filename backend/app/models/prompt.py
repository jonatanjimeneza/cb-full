# app/models.py

from pydantic import BaseModel

class PromptNodeData(BaseModel):
    promptTemplate: str
