"""Cost monitoring client for Mogu SDK"""

import logging
from datetime import datetime, timezone
from typing import Optional

from mogu_sdk.auth import BaseClient
from mogu_sdk.models import (
    ConsumptionFinalizeRequest,
    ConsumptionFinalizeResponse,
)

logger = logging.getLogger(__name__)


class CostClient:
    """Client for cost monitoring operations"""

    def __init__(self, client: BaseClient) -> None:
        """
        Initialize cost client.

        Args:
            client: Base HTTP client for making requests
        """
        self._client = client

    async def finalize_consumption(
        self,
        workspace_id: str,
        flow_run_id: str,
        workflow_id: Optional[str] = None,
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
    ) -> ConsumptionFinalizeResponse:
        """
        Finalize consumption for a completed flow run.

        This should be called when a flow run completes to:
        1. Read consumption from Prefect artifacts
        2. Save aggregated consumption to database for fast querying

        Args:
            workspace_id: Workspace identifier
            flow_run_id: Prefect flow run ID
            workflow_id: Optional workflow ID
            started_at: Flow run start time
            completed_at: Flow run completion time (defaults to now)

        Returns:
            Response with record ID and total cost

        Raises:
            PermissionDeniedError: If user lacks access
            MoguAPIError: On other API errors
        """
        if completed_at is None:
            completed_at = datetime.now(timezone.utc)

        request_data = ConsumptionFinalizeRequest(
            workspace_id=workspace_id,
            flow_run_id=flow_run_id,
            workflow_id=workflow_id,
            started_at=started_at.isoformat() if started_at else None,
            completed_at=completed_at.isoformat(),
        )

        response = await self._client.post(
            f"/api/v1/workspaces/{workspace_id}/costs/consumption/finalize",
            json=request_data.model_dump(exclude_none=True),
        )

        data = response.json()
        return ConsumptionFinalizeResponse(**data)
