from pydantic import BaseModel


class AssistantRequest(BaseModel):
    project_id: str
    node_name: str
    content: str


class AssistantResponse(BaseModel):
    response: str
