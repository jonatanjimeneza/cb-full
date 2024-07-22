from pydantic import BaseModel, Field

class OpenAINode(BaseModel):
    api_key: str
    model: str = 'gpt-3.5-turbo'
    temperature: float = Field(default=0.7, ge=0, le=1)
