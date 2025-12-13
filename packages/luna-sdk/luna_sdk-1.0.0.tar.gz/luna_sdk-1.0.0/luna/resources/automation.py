from __future__ import annotations

from typing import Any, Dict

from luna.http import HttpClient
from luna.types import WorkflowList, WorkflowRun


class WorkflowsResource:
    """Manages automation workflows."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client
        self._base_path = "/v1/automation/workflows"

    async def list(self) -> WorkflowList:
        """List all workflows."""
        resp = await self._client.request(
            method="GET",
            path=self._base_path,
        )
        return WorkflowList.model_validate(resp.data)

    async def trigger(self, id: str, params: Dict[str, Any] | None = None) -> WorkflowRun:
        """Trigger a workflow."""
        resp = await self._client.request(
            method="POST",
            path=f"{self._base_path}/{id}/trigger",
            body=params or {},
        )
        return WorkflowRun.model_validate(resp.data)


class AutomationResource:
    """Automation Service resources."""

    def __init__(self, client: HttpClient) -> None:
        self.workflows = WorkflowsResource(client)
