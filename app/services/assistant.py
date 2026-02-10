import httpx
from openai import AsyncOpenAI

from app.core.config import settings
from app.core.exceptions import BadRequestException, NotFoundException


class AssistantService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.cdn_base_url = settings.r2_public_url

    async def fetch_metadata(self, project_id: str) -> dict:
        url = f"{self.cdn_base_url}/projects/{project_id}/meta_data.json"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            if response.status_code == 404:
                raise NotFoundException(
                    f"Metadata not found for project_id: {project_id}"
                )

            if response.status_code != 200:
                raise BadRequestException(f"Failed to fetch metadata: {response.text}")

            return response.json()

    def get_node_data(self, metadata: dict, node_name: str) -> dict:
        if node_name not in metadata:
            raise NotFoundException(f"Node '{node_name}' not found in metadata")

        return metadata[node_name]

    async def generate_response(
        self, node_data: dict, user_question: str, node_name: str
    ) -> str:
        system_prompt = f"""You are an expert assistant for 3D engineering CAD models and mechanical parts.
You help users understand specific components and answer their questions based on the component's metadata.

You are currently analyzing the component: {node_name}

Component metadata:
{node_data}

Provide clear, technical, and accurate answers in Korean based on this metadata. If the metadata doesn't contain enough information to answer the question, acknowledge this limitation in Korean."""

        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question},
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content


assistant_service = AssistantService()
