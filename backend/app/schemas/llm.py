from pydantic import BaseModel


class LLMRequest(BaseModel):
    system_prompt: str
    user_prompt: str


class LLMResponse(BaseModel):
    response: str