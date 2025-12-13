# redix_client/client.py
"""
Redix Universal Healthcare Conversion API - Python Client
Thin client approach - works with any API endpoint without SDK updates.
"""
import os
import httpx
from typing import Optional, Dict, Any, Union, BinaryIO
from pathlib import Path

from .exceptions import RedixAPIError


class RedixClient:
    """
    Thin client for Redix Universal Healthcare Conversion API.

    Supports all current and future API endpoints without requiring SDK updates.

    Example:
        client = RedixClient(
            base_url="https://demo.redix.com",
            api_key="your-api-key"
        )

        # Health check
        response = client.get("/")

        # Any v1 endpoint
        response = client.get("/api/v1/staging-files")

        # Any v2 endpoint
        response = client.post("/api/v2/convert/hl7-to-fhir", files={"file": open("test.hl7", "rb")})

        # File upload with form data
        response = client.post("/api/v1/staging/upload", files={"file": open("data.txt", "rb")})
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 120,
        verify_ssl: bool = True
    ):
        """
        Initialize the Redix API client.

        Args:
            base_url: Base URL for API (e.g., "https://demo.redix.com").
                     Falls back to REDIX_API_URL environment variable.
            api_key: API key for authentication.
                    Falls back to REDIX_API_KEY environment variable.
            timeout: Request timeout in seconds (default: 120).
            verify_ssl: Verify SSL certificates (default: True).
                       Set to False for self-signed certs in development.
        """
        self.base_url = (base_url or os.getenv("REDIX_API_URL", "")).rstrip("/")
        self.api_key = api_key or os.getenv("REDIX_API_KEY", "")
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.base_url:
            raise ValueError("base_url is required (or set REDIX_API_URL environment variable)")

    def _get_headers(self, extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Build request headers."""
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response and raise errors if needed."""
        if response.status_code >= 400:
            try:
                error_detail = response.json()
                message = error_detail.get("detail") or error_detail.get("message") or response.text
            except Exception:
                message = response.text
            raise RedixAPIError(response.status_code, message)

        # Return JSON if possible, otherwise return text
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()
        return {"content": response.text, "status_code": response.status_code}

    def _prepare_files(
        self,
        files: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Prepare files for upload.

        Accepts:
            - File path as string: {"file": "/path/to/file.txt"}
            - File object: {"file": open("file.txt", "rb")}
            - Tuple (filename, file_obj): {"file": ("custom_name.txt", open("file.txt", "rb"))}
        """
        if not files:
            return None

        prepared = {}
        for key, value in files.items():
            if isinstance(value, str):
                # File path - open it
                path = Path(value)
                if not path.exists():
                    raise RedixAPIError(404, f"File not found: {value}")
                prepared[key] = (path.name, open(value, "rb"))
            elif isinstance(value, tuple):
                # Already a tuple (filename, file_obj)
                prepared[key] = value
            elif hasattr(value, "read"):
                # File-like object
                name = getattr(value, "name", "file")
                if isinstance(name, str):
                    name = Path(name).name
                prepared[key] = (name, value)
            else:
                prepared[key] = value

        return prepared

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH).
            endpoint: API endpoint (e.g., "/api/v1/staging-files").
            params: Query parameters.
            data: Form data (for multipart/form-data requests).
            json: JSON body data.
            files: Files to upload. Accepts:
                   - File paths: {"file": "/path/to/file.txt"}
                   - File objects: {"file": open("file.txt", "rb")}
                   - Tuples: {"file": ("filename.txt", file_obj)}
            headers: Additional headers.
            timeout: Request timeout (overrides default).

        Returns:
            Dict containing the API response.

        Raises:
            RedixAPIError: If the API returns an error status code.
        """
        url = f"{self.base_url}{endpoint}"
        request_headers = self._get_headers(headers)
        request_timeout = timeout or self.timeout

        prepared_files = self._prepare_files(files)

        try:
            response = httpx.request(
                method=method.upper(),
                url=url,
                params=params,
                data=data,
                json=json,
                files=prepared_files,
                headers=request_headers,
                timeout=request_timeout,
                verify=self.verify_ssl
            )
            return self._handle_response(response)
        finally:
            # Close any file handles we opened
            if prepared_files:
                for key, value in prepared_files.items():
                    if isinstance(value, tuple) and len(value) >= 2:
                        file_obj = value[1]
                        if hasattr(file_obj, "close"):
                            try:
                                file_obj.close()
                            except Exception:
                                pass

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Make a GET request.

        Args:
            endpoint: API endpoint (e.g., "/api/v1/files").
            params: Query parameters.
            headers: Additional headers.
            timeout: Request timeout.

        Returns:
            Dict containing the API response.
        """
        return self.request("GET", endpoint, params=params, headers=headers, timeout=timeout)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Make a POST request.

        Args:
            endpoint: API endpoint.
            data: Form data.
            json: JSON body.
            files: Files to upload.
            params: Query parameters.
            headers: Additional headers.
            timeout: Request timeout.

        Returns:
            Dict containing the API response.
        """
        return self.request(
            "POST", endpoint,
            params=params, data=data, json=json, files=files,
            headers=headers, timeout=timeout
        )

    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Make a PUT request.

        Args:
            endpoint: API endpoint.
            data: Form data.
            json: JSON body.
            files: Files to upload.
            params: Query parameters.
            headers: Additional headers.
            timeout: Request timeout.

        Returns:
            Dict containing the API response.
        """
        return self.request(
            "PUT", endpoint,
            params=params, data=data, json=json, files=files,
            headers=headers, timeout=timeout
        )

    def patch(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Make a PATCH request.

        Args:
            endpoint: API endpoint.
            data: Form data.
            json: JSON body.
            params: Query parameters.
            headers: Additional headers.
            timeout: Request timeout.

        Returns:
            Dict containing the API response.
        """
        return self.request(
            "PATCH", endpoint,
            params=params, data=data, json=json,
            headers=headers, timeout=timeout
        )

    def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Make a DELETE request.

        Args:
            endpoint: API endpoint.
            params: Query parameters.
            headers: Additional headers.
            timeout: Request timeout.

        Returns:
            Dict containing the API response.
        """
        return self.request("DELETE", endpoint, params=params, headers=headers, timeout=timeout)

    def download(
        self,
        endpoint: str,
        dest_path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> str:
        """
        Download a file from the API.

        Args:
            endpoint: API endpoint (e.g., "/api/v1/download-file/output/file.txt").
            dest_path: Local path to save the file.
            params: Query parameters.
            headers: Additional headers.
            timeout: Request timeout.

        Returns:
            Path where file was saved.

        Raises:
            RedixAPIError: If download fails.
        """
        url = f"{self.base_url}{endpoint}"
        request_headers = self._get_headers(headers)
        request_timeout = timeout or self.timeout

        with httpx.stream(
            "GET", url,
            params=params,
            headers=request_headers,
            timeout=request_timeout,
            verify=self.verify_ssl
        ) as response:
            if response.status_code >= 400:
                raise RedixAPIError(response.status_code, response.text)

            dest = Path(dest_path)
            if dest.is_dir():
                # Extract filename from Content-Disposition or endpoint
                filename = endpoint.split("/")[-1]
                dest = dest / filename

            with open(dest, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)

        return str(dest)
