from pydantic import BaseModel


class AssistantRequest(BaseModel):
    content: str


class AssistantResponse(BaseModel):
    response: str
