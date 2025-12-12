"""
Semantik Python SDK

A Python client library for the Semantik Client API.

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
    >>> result = client.candidates.submit_application({
    ...     "candidate": {
    ...         "firstName": "John",
    ...         "lastName": "Doe",
    ...         "email": "john@example.com"
    ...     },
    ...     "programId": 123,
    ...     "stepId": "step-1",
    ...     "documents": [{
    ...         "fieldName": "CV",
    ...         "content": base64_content,
    ...         "fileName": "cv.pdf"
    ...     }]
    ... })
"""

from semantik.client import Semantik
from semantik.http.base_client import ApiError, SemantikConfig

__version__ = "0.1.0"
__all__ = [
    "Semantik",
    "ApiError",
    "SemantikConfig",
]

