"""Candidates resource for Semantik API."""

from typing import Dict, Any, Optional, List
from semantik.http.base_client import BaseClient


class CandidatesResource:
    """Resource for managing candidates."""

    def __init__(self, client: BaseClient):
        """Initialize the candidates resource."""
        self.client = client

    def submit_application(
        self,
        candidate: Dict[str, str],
        program_id: int,
        step_id: str,
        client_data: Optional[Dict[str, Any]] = None,
        documents: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Submit a candidate application with documents.

        Args:
            candidate: Dictionary with 'firstName', 'lastName', 'email'
            program_id: Program ID
            step_id: Step ID to submit to
            client_data: Optional custom metadata
            documents: Optional list of document dictionaries with:
                - fieldName: Field name for the document
                - content: Base64-encoded or UTF-8 content
                - fileName: Optional file name
                - mimeType: Optional MIME type
                - encoding: Optional encoding ('base64' or 'utf-8')
                - fieldType: Optional field type

        Returns:
            Application submission response dictionary
        """
        body: Dict[str, Any] = {
            "candidate": candidate,
            "programId": program_id,
            "stepId": step_id,
        }
        if client_data:
            body["clientData"] = client_data
        if documents:
            body["documents"] = documents

        return self.client.request(
            "/api/v2/candidates/applications",
            method="POST",
            body=body,
        )

    def get_status(
        self, candidate_id: str, include: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get candidate status across all programs.

        Args:
            candidate_id: The candidate ID
            include: Optional comma-separated list ('applications', 'scores', 'documents', 'all')

        Returns:
            Candidate status dictionary
        """
        params = {}
        if include:
            params["include"] = include

        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        path = f"/api/v2/candidates/{candidate_id}"
        if query_string:
            path += f"?{query_string}"

        return self.client.request(path)

    def get_applications(
        self, candidate_id: str, include: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get all applications for a candidate.

        Args:
            candidate_id: The candidate ID
            include: Optional comma-separated list ('documents', 'scores', 'all')

        Returns:
            Dictionary with 'applications' key
        """
        params = {}
        if include:
            params["include"] = include

        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        path = f"/api/v2/candidates/{candidate_id}/applications"
        if query_string:
            path += f"?{query_string}"

        return self.client.request(path)

    def get_scores(
        self, candidate_id: str, include: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get scores for a candidate across all programs.

        Args:
            candidate_id: The candidate ID
            include: Optional comma-separated list ('applications', 'documents', 'all')

        Returns:
            Dictionary with 'programs' key containing score information
        """
        params = {}
        if include:
            params["include"] = include

        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        path = f"/api/v2/candidates/{candidate_id}/scores"
        if query_string:
            path += f"?{query_string}"

        return self.client.request(path)

    def enroll(
        self,
        candidate_id: str,
        program_id: int,
        step_id: Optional[str] = None,
        send_email: Optional[bool] = None,
        email_template: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Enroll a candidate in a program.

        Args:
            candidate_id: The candidate ID
            program_id: Program ID
            step_id: Optional step ID (defaults to first step)
            send_email: Optional flag to send enrollment email
            email_template: Optional custom email template

        Returns:
            Enrollment response dictionary
        """
        body: Dict[str, Any] = {"programId": program_id}
        if step_id:
            body["stepId"] = step_id
        if send_email is not None:
            body["sendEmail"] = send_email
        if email_template:
            body["emailTemplate"] = email_template

        return self.client.request(
            f"/api/v2/candidates/{candidate_id}/enroll",
            method="POST",
            body=body,
        )

    def update_attachments(
        self,
        candidate_id: str,
        attachments: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Add or update attachments for a candidate.

        Args:
            candidate_id: The candidate ID
            attachments: List of attachment dictionaries with:
                - fieldName: Field name for the attachment
                - content: Base64-encoded or UTF-8 content
                - fileName: Optional file name
                - mimeType: Optional MIME type
                - encoding: Optional encoding ('base64' or 'utf-8')

        Returns:
            Response dictionary with success status and message
        """
        body = {"attachments": attachments}

        return self.client.request(
            f"/api/v2/candidates/{candidate_id}/attachments",
            method="PUT",
            body=body,
        )

