"""HTTP client for ThreatWinds Pentest API."""

import json
import os
import re
from typing import Optional, Dict, Any
from pathlib import Path
import zipfile

import requests
from requests.exceptions import RequestException

from .models import (
    Credentials,
    HTTPPentestData,
    HTTPPentestListResponse,
    HTTPSchedulePentestRequest,
)


def _sanitize_id_for_path(pentest_id: str) -> str:
    """
    Sanitize a pentest ID for safe use in filesystem paths.

    Removes any characters that could be problematic:
    - Path traversal (..)
    - Directory separators (/, \\)
    - Special filesystem characters

    Args:
        pentest_id: The pentest ID to sanitize

    Returns:
        Sanitized ID safe for use in paths
    """
    if not pentest_id:
        return "unknown"

    # Remove path traversal and directory separators
    sanitized = re.sub(r'[/\\]', '-', pentest_id)
    sanitized = re.sub(r'\.\.+', '.', sanitized)

    # Keep only alphanumeric, hyphens, underscores, and dots
    sanitized = re.sub(r'[^a-zA-Z0-9\-_.]', '', sanitized)

    # Ensure it doesn't start with a dot or hyphen
    sanitized = sanitized.lstrip('.-')

    return sanitized or "unknown"


class HTTPClient:
    """HTTP client for ThreatWinds Pentest API operations."""

    def __init__(self, base_url: str, credentials: Credentials):
        """Initialize HTTP client.

        Args:
            base_url: Base URL for the API
            credentials: API credentials for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.credentials = credentials
        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'application/json',
            'api-key': credentials.api_key,
            'api-secret': credentials.api_secret,
        })

    def _make_request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
    ) -> requests.Response:
        """Make an HTTP request.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            json_data: JSON data for request body
            headers: Additional headers to include
            timeout: Request timeout in seconds

        Returns:
            Response object

        Raises:
            RequestException: If request fails
        """
        url = f"{self.base_url}{endpoint}"

        # Merge additional headers if provided
        req_headers = self.session.headers.copy()
        if headers:
            req_headers.update(headers)

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json_data,
                headers=req_headers,
                timeout=timeout,
            )
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            # Extract error message from response if available
            try:
                error_data = e.response.json()
                error_msg = error_data.get('message', error_data.get('error', str(e)))
                # Include more details for debugging
                if 'details' in error_data:
                    error_msg += f" - {error_data['details']}"
            except:
                error_msg = f"{e.response.status_code}: {e.response.text if hasattr(e.response, 'text') else str(e)}"
            raise RequestException(f"HTTP error: {error_msg}") from e
        except RequestException as e:
            raise RequestException(f"Request failed: {str(e)}") from e

    def list_pentests(self, page: int = 1, page_size: int = 10) -> HTTPPentestListResponse:
        """Retrieve a paginated list of pentests.

        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            HTTPPentestListResponse with paginated results

        Raises:
            RequestException: If request fails
        """
        endpoint = f"/api/v1/pentests?page={page}&page_size={page_size}"
        response = self._make_request("GET", endpoint)
        return HTTPPentestListResponse(**response.json())

    def get_pentest(self, pentest_id: str) -> HTTPPentestData:
        """Retrieve a single pentest by ID.

        Args:
            pentest_id: Unique identifier of the pentest

        Returns:
            HTTPPentestData object with pentest details

        Raises:
            RequestException: If request fails or pentest not found
        """
        endpoint = f"/api/v1/pentests/{pentest_id}"
        try:
            response = self._make_request("GET", endpoint)
            return HTTPPentestData(**response.json())
        except RequestException as e:
            if "404" in str(e):
                raise RequestException(f"Pentest {pentest_id} not found") from e
            raise

    def schedule_pentest(self, request: HTTPSchedulePentestRequest) -> str:
        """Schedule a new pentest.

        Args:
            request: HTTPSchedulePentestRequest with pentest configuration

        Returns:
            String with the pentest ID

        Raises:
            RequestException: If request fails
        """
        endpoint = "/api/v1/pentests/schedule"
        headers = {'content-type': 'application/json'}

        # Convert request to dict with proper field names
        request_data = request.model_dump()

        response = self._make_request("POST", endpoint, json_data=request_data, headers=headers)
        result = response.json()

        # Handle different response formats
        if isinstance(result, dict):
            return result.get('PentestID', result.get('pentest_id', ''))
        return str(result)

    def download_evidence(
        self,
        pentest_id: str,
        output_path: str,
        extract: bool = True,
        timeout: int = 300
    ) -> str:
        """Download and optionally extract pentest evidence.

        Args:
            pentest_id: Unique identifier of the pentest
            output_path: Directory to save the evidence
            extract: Whether to extract the ZIP file
            timeout: Download timeout in seconds

        Returns:
            Path to the downloaded/extracted evidence

        Raises:
            RequestException: If download fails
        """
        endpoint = f"/api/v1/pentests/{pentest_id}/download"

        # Ensure output directory exists
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Set up download headers
        headers = {
            'accept': 'application/zip',
        }

        # Download the file
        response = self._make_request("GET", endpoint, headers=headers, timeout=timeout)

        # Sanitize pentest_id for filesystem safety
        safe_id = _sanitize_id_for_path(pentest_id)

        # Save the ZIP file
        zip_filename = f"pentest_{safe_id}_evidence.zip"
        zip_path = output_dir / zip_filename

        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        # Extract if requested
        if extract:
            extract_dir = output_dir / f"pentest_{safe_id}_evidence"
            extract_dir.mkdir(exist_ok=True)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            # Optionally remove the ZIP file after extraction
            zip_path.unlink()

            return str(extract_dir)

        return str(zip_path)

    def get_current_version(self) -> str:
        """Get the current version of the pentest agent.

        Returns:
            Version string

        Raises:
            RequestException: If request fails
        """
        endpoint = "/api/v1/version"
        response = self._make_request("GET", endpoint)
        result = response.json()

        # Handle different response formats
        if isinstance(result, dict):
            return result.get('version', '')
        return str(result)

    def chat_with_pentest(self, pentest_id: str, question: str, timeout: int = 120) -> Dict[str, Any]:
        """Ask a question about a pentest's results.

        The AI will analyze the evidence files and provide explanations.

        Args:
            pentest_id: Unique identifier of the pentest
            question: Question about the pentest results
            timeout: Request timeout in seconds (AI responses can take time)

        Returns:
            Dict with success, answer, pentest_id, and error fields

        Raises:
            RequestException: If request fails
        """
        endpoint = f"/api/v1/pentests/{pentest_id}/chat"
        headers = {'content-type': 'application/json'}

        request_data = {'question': question}

        response = self._make_request(
            "POST",
            endpoint,
            json_data=request_data,
            headers=headers,
            timeout=timeout
        )
        return response.json()

    def close(self):
        """Close the HTTP session."""
        self.session.close()