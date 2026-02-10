from fastapi import APIRouter

from app.schemas.assistant import AssistantRequest, AssistantResponse
from app.services.assistant import assistant_service

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("", response_model=AssistantResponse)
async def ask_assistant(request: AssistantRequest):
    metadata = await assistant_service.fetch_metadata(request.project_id)
    node_data = assistant_service.get_node_data(metadata, request.node_name)
    response = await assistant_service.generate_response(
        node_data, request.content, request.node_name
    )

    return AssistantResponse(response=response)
