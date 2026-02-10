from fastapi import APIRouter

from app.schemas.assistant import AssistantRequest, AssistantResponse
from app.services.assistant import assistant_service

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/{project_id}/{node_name}", response_model=AssistantResponse)
async def ask_assistant(project_id: str, node_name: str, request: AssistantRequest):
    metadata = await assistant_service.fetch_metadata(project_id)
    node_data = assistant_service.get_node_data(metadata, node_name)
    response = await assistant_service.generate_response(
        node_data, request.content, node_name
    )

    return AssistantResponse(response=response)
