"""HTTP client for VirtualDojo API."""

import time
from typing import Any, Optional

import httpx

from .config import (
    Credentials,
    Profile,
    config_manager,
    get_current_credentials,
    get_current_profile,
)
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    NotLoggedInError,
    TokenExpiredError,
)


class VirtualDojoClient:
    """Async HTTP client with automatic auth and tenant handling."""

    def __init__(
        self,
        profile: Optional[str] = None,
        *,
        timeout: float = 30.0,
    ):
        """Initialize the client.

        Args:
            profile: Profile name to use. If None, uses default profile.
            timeout: Request timeout in seconds.
        """
        self._profile_name = profile
        self._profile: Optional[Profile] = None
        self._credentials: Optional[Credentials] = None
        self._client: Optional[httpx.AsyncClient] = None
        self._timeout = timeout

    @property
    def profile(self) -> Profile:
        """Get the current profile."""
        if self._profile is None:
            self._profile = get_current_profile(self._profile_name)
        return self._profile

    @property
    def credentials(self) -> Credentials:
        """Get the current credentials."""
        if self._credentials is None:
            creds = get_current_credentials(self.profile.name)
            if creds is None or creds.token is None:
                raise NotLoggedInError()
            self._credentials = creds
        return self._credentials

    def _is_token_expired(self) -> bool:
        """Check if the current token is expired."""
        if self.credentials.expires_at is None:
            return False
        # Add 30 second buffer
        return time.time() > (self.credentials.expires_at - 30)

    async def _refresh_token(self) -> bool:
        """Attempt to refresh the JWT token.

        Returns:
            True if refresh was successful, False otherwise.
        """
        if self.credentials.token_type != "jwt" or not self.credentials.refresh_token:
            return False

        try:
            async with httpx.AsyncClient(
                base_url=self.profile.server,
                timeout=self._timeout,
            ) as client:
                response = await client.post(
                    "/api/v1/auth/refresh-token",
                    json={"refresh_token": self.credentials.refresh_token},
                )

                if response.status_code == 200:
                    data = response.json()
                    self._credentials.token = data["access_token"]
                    self._credentials.expires_at = time.time() + data.get(
                        "expires_in", 1800
                    )
                    if "refresh_token" in data:
                        self._credentials.refresh_token = data["refresh_token"]
                    config_manager.save_credentials(self._credentials)
                    return True
        except Exception:
            pass

        return False

    def _get_headers(self) -> dict[str, str]:
        """Get headers for API requests."""
        return {
            "Authorization": f"Bearer {self.credentials.token}",
            "X-Tenant-ID": self.profile.tenant,
            "Content-Type": "application/json",
        }

    async def __aenter__(self) -> "VirtualDojoClient":
        """Enter async context."""
        # Check token expiration
        if self._is_token_expired():
            if not await self._refresh_token():
                raise TokenExpiredError()

        self._client = httpx.AsyncClient(
            base_url=self.profile.server,
            headers=self._get_headers(),
            timeout=self._timeout,
        )
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Exit async context."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def _handle_response(self, response: httpx.Response) -> None:
        """Handle API response and raise appropriate exceptions."""
        if response.status_code == 401:
            # Try token refresh
            if await self._refresh_token():
                # Update client headers with new token
                if self._client:
                    self._client.headers["Authorization"] = (
                        f"Bearer {self.credentials.token}"
                    )
                # Caller should retry the request
                raise TokenExpiredError()
            raise AuthenticationError(
                message="Authentication failed.",
                hint="Run 'vdojo login' to authenticate again.",
            )

        if response.status_code >= 400:
            try:
                detail = response.json().get("detail", "Unknown error")
            except Exception:
                detail = response.text or "Unknown error"
            raise APIError(response.status_code, detail)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
        retry_count: int = 1,
    ) -> dict[str, Any]:
        """Make an HTTP request with automatic retry on token refresh.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API path
            params: Query parameters
            json: JSON body data
            retry_count: Number of retries remaining

        Returns:
            Response JSON data
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use 'async with' context.")

        try:
            response = await self._client.request(
                method, path, params=params, json=json
            )
            await self._handle_response(response)
            return response.json() if response.content else {}
        except TokenExpiredError:
            if retry_count > 0:
                # Update headers and retry
                self._client.headers["Authorization"] = (
                    f"Bearer {self.credentials.token}"
                )
                return await self._request(
                    method, path, params=params, json=json, retry_count=retry_count - 1
                )
            raise
        except httpx.ConnectError as e:
            raise NetworkError(f"Could not connect to {self.profile.server}") from e
        except httpx.TimeoutException as e:
            raise NetworkError("Request timed out") from e

    async def get(
        self, path: str, *, params: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Make a GET request."""
        return await self._request("GET", path, params=params)

    async def post(
        self, path: str, data: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Make a POST request."""
        return await self._request("POST", path, json=data)

    async def put(
        self, path: str, data: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Make a PUT request."""
        return await self._request("PUT", path, json=data)

    async def delete(self, path: str) -> dict[str, Any]:
        """Make a DELETE request."""
        return await self._request("DELETE", path)

    async def patch(
        self, path: str, data: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Make a PATCH request."""
        return await self._request("PATCH", path, json=data)

    async def upload(
        self,
        path: str,
        file_path: str,
        *,
        filename: Optional[str] = None,
        folder_id: Optional[str] = None,
        retry_count: int = 1,
    ) -> dict[str, Any]:
        """Upload a file using multipart form data.

        Args:
            path: API path for upload
            file_path: Local path to the file
            filename: Override filename (uses file_path name if not provided)
            folder_id: Optional folder ID to upload to
            retry_count: Number of retries remaining

        Returns:
            Response JSON data
        """
        import os
        import mimetypes

        if not self._client:
            raise RuntimeError("Client not initialized. Use 'async with' context.")

        actual_filename = filename or os.path.basename(file_path)
        mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

        try:
            with open(file_path, "rb") as f:
                file_content = f.read()

            files = {"file": (actual_filename, file_content, mime_type)}
            data: dict[str, Any] = {}
            if folder_id:
                data["parent_folder_id"] = folder_id

            # Create a new client without Content-Type header for multipart
            auth_headers = {
                "Authorization": self._client.headers.get("Authorization", ""),
                "X-Tenant-ID": self._client.headers.get("X-Tenant-ID", ""),
            }

            async with httpx.AsyncClient(
                base_url=self.profile.server,
                headers=auth_headers,
                timeout=self._timeout,
            ) as upload_client:
                response = await upload_client.post(
                    path,
                    files=files,
                    data=data if data else None,
                )
                await self._handle_response(response)
                return response.json() if response.content else {}
        except TokenExpiredError:
            if retry_count > 0:
                self._client.headers["Authorization"] = (
                    f"Bearer {self.credentials.token}"
                )
                return await self.upload(
                    path,
                    file_path,
                    filename=filename,
                    folder_id=folder_id,
                    retry_count=retry_count - 1,
                )
            raise
        except httpx.ConnectError as e:
            raise NetworkError(f"Could not connect to {self.profile.server}") from e
        except httpx.TimeoutException as e:
            raise NetworkError("Request timed out") from e

    async def download(
        self,
        path: str,
        output_path: str,
        *,
        progress_callback: Optional[Any] = None,
    ) -> int:
        """Download a file with optional progress tracking.

        Args:
            path: API path for download
            output_path: Local path to save the file
            progress_callback: Optional callback(bytes_downloaded, total_bytes)

        Returns:
            Total bytes downloaded
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use 'async with' context.")

        try:
            async with self._client.stream("GET", path) as response:
                if response.status_code == 401:
                    if await self._refresh_token():
                        self._client.headers["Authorization"] = (
                            f"Bearer {self.credentials.token}"
                        )
                        raise TokenExpiredError()
                    raise AuthenticationError(
                        message="Authentication failed.",
                        hint="Run 'vdojo login' to authenticate again.",
                    )

                if response.status_code >= 400:
                    try:
                        content = await response.aread()
                        import json
                        detail = json.loads(content).get("detail", "Unknown error")
                    except Exception:
                        detail = "Download failed"
                    raise APIError(response.status_code, detail)

                total = int(response.headers.get("content-length", 0))
                downloaded = 0

                with open(output_path, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback:
                            progress_callback(downloaded, total)

                return downloaded
        except httpx.ConnectError as e:
            raise NetworkError(f"Could not connect to {self.profile.server}") from e
        except httpx.TimeoutException as e:
            raise NetworkError("Request timed out") from e


class SyncVirtualDojoClient:
    """Synchronous wrapper for VirtualDojoClient.

    This is used by Typer commands which don't support async natively.
    """

    def __init__(self, profile: Optional[str] = None, *, timeout: float = 30.0):
        self._profile_name = profile
        self._timeout = timeout

    def _run_async(self, coro: Any) -> Any:
        """Run an async coroutine synchronously."""
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(coro)

    def get(self, path: str, *, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """Make a GET request."""
        async def _get() -> dict[str, Any]:
            async with VirtualDojoClient(
                self._profile_name, timeout=self._timeout
            ) as client:
                return await client.get(path, params=params)

        return self._run_async(_get())

    def post(
        self, path: str, data: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Make a POST request."""
        async def _post() -> dict[str, Any]:
            async with VirtualDojoClient(
                self._profile_name, timeout=self._timeout
            ) as client:
                return await client.post(path, data)

        return self._run_async(_post())

    def put(
        self, path: str, data: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Make a PUT request."""
        async def _put() -> dict[str, Any]:
            async with VirtualDojoClient(
                self._profile_name, timeout=self._timeout
            ) as client:
                return await client.put(path, data)

        return self._run_async(_put())

    def delete(self, path: str) -> dict[str, Any]:
        """Make a DELETE request."""
        async def _delete() -> dict[str, Any]:
            async with VirtualDojoClient(
                self._profile_name, timeout=self._timeout
            ) as client:
                return await client.delete(path)

        return self._run_async(_delete())

    def upload(
        self,
        path: str,
        file_path: str,
        *,
        filename: Optional[str] = None,
        folder_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Upload a file."""
        async def _upload() -> dict[str, Any]:
            async with VirtualDojoClient(
                self._profile_name, timeout=self._timeout
            ) as client:
                return await client.upload(
                    path, file_path, filename=filename, folder_id=folder_id
                )

        return self._run_async(_upload())

    def download(
        self,
        path: str,
        output_path: str,
        *,
        progress_callback: Optional[Any] = None,
    ) -> int:
        """Download a file."""
        async def _download() -> int:
            async with VirtualDojoClient(
                self._profile_name, timeout=self._timeout
            ) as client:
                return await client.download(
                    path, output_path, progress_callback=progress_callback
                )

        return self._run_async(_download())
