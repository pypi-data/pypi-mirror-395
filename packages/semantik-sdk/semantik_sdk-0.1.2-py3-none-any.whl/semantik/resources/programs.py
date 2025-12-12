"""Programs resource for Semantik API."""

from typing import Dict, Any, Optional, List
from semantik.http.base_client import BaseClient


class ProgramsResource:
    """Resource for managing programs."""

    def __init__(self, client: BaseClient):
        """Initialize the programs resource."""
        self.client = client

    def list(self) -> Dict[str, Any]:
        """
        List all programs available to the organization.

        Returns:
            Dictionary with 'programs' key containing list of programs
        """
        return self.client.request("/api/v2/programs")

    def get(self, program_id: int) -> Dict[str, Any]:
        """
        Get a specific program by ID.

        Args:
            program_id: The program ID

        Returns:
            Program dictionary
        """
        return self.client.request(f"/api/v2/programs/{program_id}")

    def list_candidates(
        self,
        program_id: int,
        step_id: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        include: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List candidates in a program, optionally filtered by step.

        Args:
            program_id: The program ID
            step_id: Optional step ID to filter by
            status: Optional status filter ('active', 'refused', 'admitted')
            search: Optional search query (name or email)
            include: Optional comma-separated list ('applications', 'scores', 'documents', 'all')
            limit: Optional number of results per page
            cursor: Optional pagination cursor

        Returns:
            Dictionary with 'candidates' and 'pagination' keys
        """
        params: Dict[str, str] = {}
        if step_id:
            params["stepId"] = step_id
        if status:
            params["status"] = status
        if search:
            params["search"] = search
        if include:
            params["include"] = include
        if limit:
            params["limit"] = str(limit)
        if cursor:
            params["cursor"] = cursor

        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        path = f"/api/v2/programs/{program_id}/candidates"
        if query_string:
            path += f"?{query_string}"

        return self.client.request(path)

    def move_candidate(
        self,
        program_id: int,
        candidate_id: str,
        from_step_id: Optional[str] = None,
        to_step_id: Optional[str] = None,
        direction: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Move a candidate to the next or previous step, or to a specific step.

        Args:
            program_id: The program ID
            candidate_id: The candidate ID
            from_step_id: Optional current step ID (will be inferred if not provided)
            to_step_id: Optional target step ID (required if direction is not provided)
            direction: Optional direction ('next' or 'previous') (required if to_step_id is not provided)

        Returns:
            Movement response dictionary
        """
        body: Dict[str, Any] = {"candidateId": candidate_id}
        if from_step_id:
            body["fromStepId"] = from_step_id
        if to_step_id:
            body["toStepId"] = to_step_id
        if direction:
            body["direction"] = direction

        return self.client.request(
            f"/api/v2/programs/{program_id}/move-candidate",
            method="POST",
            body=body,
        )

