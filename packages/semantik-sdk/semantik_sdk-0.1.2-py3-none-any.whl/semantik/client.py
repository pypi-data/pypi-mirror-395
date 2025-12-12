"""Main Semantik SDK client."""

from typing import Optional
from semantik.http.base_client import BaseClient, SemantikConfig
from semantik.resources.programs import ProgramsResource
from semantik.resources.candidates import CandidatesResource


class Semantik:
    """
    Main Semantik SDK client.

    Example:
        >>> from semantik import Semantik
        >>>
        >>> # Automatically reads from SEMANTIK_API_KEY environment variable
        >>> client = Semantik()
        >>>
        >>> # Or override with explicit API key
        >>> client = Semantik(api_key="sk_...")
        >>>
        >>> # List programs
        >>> programs = client.programs.list()
        >>>
        >>> # Submit an application
        >>> result = client.candidates.submit_application(
        ...     candidate={
        ...         "firstName": "John",
        ...         "lastName": "Doe",
        ...         "email": "john@example.com"
        ...     },
        ...     program_id=123,
        ...     step_id="step-1",
        ...     documents=[{
        ...         "fieldName": "CV",
        ...         "content": base64_content,
        ...         "fileName": "cv.pdf"
        ...     }]
        ... )
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        """
        Initialize the Semantik client.

        Args:
            api_key: Optional API key. If not provided, reads from SEMANTIK_API_KEY environment variable.
            base_url: Optional base URL. If not provided, uses default or SEMANTIK_BASE_URL environment variable.

        Raises:
            ValueError: If API key is not provided and SEMANTIK_API_KEY is not set.
        """
        config = SemantikConfig(api_key=api_key, base_url=base_url)
        self._client = BaseClient(config)
        self.programs = ProgramsResource(self._client)
        self.candidates = CandidatesResource(self._client)

