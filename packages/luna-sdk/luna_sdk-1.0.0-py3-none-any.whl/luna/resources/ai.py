from __future__ import annotations

from luna.http import HttpClient
from luna.types import CompletionRequest, CompletionResponse


class AiResource:
    """AI Service resources."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client
        self._base_path = "/v1/ai"

    async def chat_completions(self, params: CompletionRequest) -> CompletionResponse:
        """Generate chat completions."""
        resp = await self._client.request(
            method="POST",
            path=f"{self._base_path}/chat/completions",
            body=params.model_dump(exclude_none=True),
        )
        return CompletionResponse.model_validate(resp.data)
