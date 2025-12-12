import asyncio
import json
import os
import uuid
from typing import Any, AsyncIterator

import aiohttp
import jwt
import nest_asyncio
import requests
import sseclient

import pvml.util as util

nest_asyncio.apply()


class PvmlHttpClient:
    """
    A client for the PVML API.

    Attributes:
        api_key (str): The API key for the PVML API.
        user_id (str): The user ID for the PVML API.
        session (aiohttp.ClientSession): The async session for streaming requests.
    """

    def __init__(self, api_key: str, event_loop: asyncio.AbstractEventLoop | None = None) -> None:
        if (api_key is None) or (api_key == ""):
            raise ValueError("api_key is required")
        self.__api_key = api_key
        decoded = jwt.decode(api_key, options={"verify_signature": False})
        if (user_id := decoded.get("user", None)) is None:
            raise ValueError("user is required")
        self.__user_id = user_id
        self.__default_api_url = os.environ.get("PVML_API_URL", "https://platform.pvml.com/platform/api/v1")
        self.__loop = event_loop
        self.__session = None

    @property
    def api_key(self) -> str:
        return self.__api_key

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def session(self) -> aiohttp.ClientSession:
        """Gets or lazily initializes the async session for streaming."""
        if self.__session is None:
            if self.__loop is None:
                try:
                    self.__loop = asyncio.get_running_loop()
                except RuntimeError:
                    self.__loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(self.__loop)
            self.__session = aiohttp.ClientSession(loop=self.__loop)
        return self.__session

    def __del__(self):
        if self.__session is not None:
            try:
                asyncio.get_running_loop().create_task(self.session.close())
            except RuntimeError:
                print("Warning: No running event loop to close session in __del__")

    async def close(self):
        """Closes the async session if it exists."""
        if self.__session is not None:
            await self.__session.close()
            self.__session = None

    def request(self, method: str, endpoint: str, headers: dict[str, str] | None = None, **kwargs) -> Any:
        """
        Makes a synchronous HTTP request to the PVML API.
        
        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint path
            headers: Optional request headers
            **kwargs: Additional arguments passed to requests.request
            
        Returns:
            The JSON response from the API
        """
        self.__method_validation(method)
        if headers is None:
            headers = self._get_auth_headers()

        url = self.__default_api_url + endpoint
        response = requests.request(method, url, headers=headers, **kwargs)

        if not (200 <= response.status_code < 300):
            raise Exception(
                f"HTTP {method.upper()} failed for URL {url} with status {response.status_code}, response: {response.text}"
            )

        if len(response.content) == 0:
            return None

        return response.json()

    def request_expect_text(self, method: str, endpoint: str, headers: dict[str, str] | None = None, **kwargs) -> Any:
        """
        Makes a synchronous HTTP request to the PVML API.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint path
            headers: Optional request headers
            **kwargs: Additional arguments passed to requests.request

        Returns:
            The JSON response from the API
        """
        self.__method_validation(method)
        if headers is None:
            headers = self._get_auth_headers()

        url = self.__default_api_url + endpoint
        response = requests.request(method, url, headers=headers, **kwargs)

        if not (200 <= response.status_code < 300):
            raise Exception(
                f"HTTP {method.upper()} failed for URL {url} with status {response.status_code}, response: {response.text}"
            )

        if len(response.content) == 0:
            return None
        return response.content.decode('utf-8')

    async def request_stream(self, method: str, endpoint: str, headers: dict[str, str] | None = None, **kwargs) -> \
            AsyncIterator[bytes]:
        """
        Makes an asynchronous streaming request to the PVML API.
        
        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint path
            headers: Optional request headers
            **kwargs: Additional arguments passed to aiohttp.ClientSession.request
            
        Returns:
            An async iterator yielding response chunks as bytes
        """
        self.__method_validation(method)
        if headers is None:
            headers = self._get_auth_headers()

        url = self.__default_api_url + endpoint
        async with self.session.request(method, url, headers=headers, **kwargs) as response:
            if not (200 <= response.status < 300):
                raise Exception(
                    f"HTTP {method.upper()} failed for URL {url} with status {response.status}, response: {await response.text()}"
                )
            async for chunk in response.content.iter_any():
                yield chunk

    def request_sse_stream_sync(self, method: str, endpoint: str, headers: dict[str, str] | None = None, **kwargs):
        """
        Makes a synchronous SSE streaming request to the PVML API.
        
        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint path
            headers: Optional request headers
            **kwargs: Additional arguments passed to requests.request
            
        Returns:
            A requests.Response object with stream=True for SSE consumption
        """
        self.__method_validation(method)
        if headers is None:
            headers = self._get_auth_headers()

        url = self.__default_api_url + endpoint
        response = requests.request(method, url, headers=headers, stream=True, **kwargs)

        if not (200 <= response.status_code < 300):
            raise Exception(
                f"HTTP {method.upper()} failed for URL {url} with status {response.status_code}, response: {response.text}"
            )

        client = sseclient.SSEClient(response.raw)

        for event in client.events():
            if event.data:
                yield event.data


    def __method_validation(self, method: str) -> None:
        allowed_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        if method not in allowed_methods:
            raise NotImplementedError(f"Method {method} is not supported")

    def _get_auth_headers(self) -> dict[str, str]:
        """Constructs the authentication headers based on API key."""
        return {"Content-Type": "application/json", "Authorization": f"Bearer {self.__api_key}"}

    def metadata_request(self, request_dict: dict[str, Any], image_bytes: bytes | None = None) -> tuple[
        bytes, dict[str, str]]:
        """
        Prepares a multipart form request with metadata and optional image.
        
        Args:
            request_dict: Dictionary of metadata to include in the request
            image_bytes: Optional image bytes to include in the request
            
        Returns:
            Tuple of (body_bytes, headers) for the request
        """
        boundary = f"----WebKitFormBoundary_{uuid.uuid4()}"

        def b(line: str) -> bytes:
            return line.encode()

        CRLF = b"\r\n"
        parts: list[bytes] = []

        parts += [
            b(f"--{boundary}"),
            b('Content-Disposition: form-data; name="data"'),
            b(""),
            json.dumps(request_dict).encode(),
        ]

        if image_bytes is not None:
            mime = util.sniff_png_jpeg(image_bytes)
            parts += [
                b(f"--{boundary}"),
                b(f'Content-Disposition: form-data; name="image"; filename="image.{mime}"'),
                b(f"Content-Type: image/{mime}"),
                b(""),
                image_bytes,
            ]
        parts += [b(f"--{boundary}--"), b("")]

        body_bytes = CRLF.join(parts)

        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Authorization": f"Bearer {self.api_key}",
            "Content-Length": str(len(body_bytes)),
        }
        return body_bytes, headers

    def get_text_header(self, data: Any) -> dict[str, Any]:
        headers = {
            "Content-Type": "text/plain",
            "Content-Length": str(len(data)),
            "Authorization": f"Bearer {self.api_key}"

        }
        return headers
