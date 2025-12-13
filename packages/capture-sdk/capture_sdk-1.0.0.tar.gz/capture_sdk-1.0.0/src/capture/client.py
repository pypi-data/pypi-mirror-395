import hashlib
from typing import Any, Dict, Literal, Optional, Union
from urllib.parse import urlencode

import aiohttp
from yarl import URL

RequestType = Literal["image", "pdf", "content", "metadata", "animated"]
RequestOptions = Dict[str, Union[str, int, bool]]

class Capture:
    API_URL = "https://cdn.capture.page"
    EDGE_URL = "https://edge.capture.page"

    def __init__(
        self, key: str, secret: str, options: Optional[Dict[str, bool]] = None
    ) -> None:
        self.key = key
        self.secret = secret
        self.options = options or {}

    def _generate_token(self, secret: str, url: str) -> str:
        token_string = f"{secret}{url}"
        return hashlib.md5(token_string.encode()).hexdigest()

    def _encode_query_string(self, params: Dict[str, Any]) -> str:
        filtered_params = {}
        for k, v in params.items():
            if v is None:
                continue
            if isinstance(v, bool):
                filtered_params[k] = str(v).lower()
            else:
                filtered_params[k] = v

        return urlencode(filtered_params, safe="")

    def _build_url(
        self, url: str, request_type: RequestType, options: Optional[RequestOptions] = None
    ) -> str:
        if not self.key or not self.secret:
            raise ValueError("Key and Secret is required")

        if url is None:
            raise ValueError("url is required")

        if not isinstance(url, str):
            raise TypeError("url should be of type string (something like www.google.com)")

        params = options.copy() if options else {}
        params["url"] = url

        query_string = self._encode_query_string(params)
        token = self._generate_token(self.secret, query_string)

        base_url = self.EDGE_URL if self.options.get("useEdge") else self.API_URL

        return f"{base_url}/{self.key}/{token}/{request_type}?{query_string}"

    def build_image_url(self, url: str, options: Optional[RequestOptions] = None) -> str:
        return self._build_url(url, "image", options)

    def build_pdf_url(self, url: str, options: Optional[RequestOptions] = None) -> str:
        return self._build_url(url, "pdf", options)

    def build_content_url(self, url: str, options: Optional[RequestOptions] = None) -> str:
        return self._build_url(url, "content", options)

    def build_metadata_url(self, url: str, options: Optional[RequestOptions] = None) -> str:
        return self._build_url(url, "metadata", options)

    def build_animated_url(self, url: str, options: Optional[RequestOptions] = None) -> str:
        return self._build_url(url, "animated", options)

    async def fetch_image(self, url: str, options: Optional[RequestOptions] = None) -> bytes:
        fetch_url = self.build_image_url(url, options)
        async with aiohttp.ClientSession() as session:
            async with session.get(URL(fetch_url, encoded=True)) as response:
                response.raise_for_status()
                return await response.read()

    async def fetch_pdf(self, url: str, options: Optional[RequestOptions] = None) -> bytes:
        fetch_url = self.build_pdf_url(url, options)
        async with aiohttp.ClientSession() as session:
            async with session.get(URL(fetch_url, encoded=True)) as response:
                response.raise_for_status()
                return await response.read()

    async def fetch_content(
        self, url: str, options: Optional[RequestOptions] = None
    ) -> Dict[str, Union[bool, str]]:
        fetch_url = self.build_content_url(url, options)
        async with aiohttp.ClientSession() as session:
            async with session.get(URL(fetch_url, encoded=True)) as response:
                response.raise_for_status()
                return await response.json()

    async def fetch_metadata(
        self, url: str, options: Optional[RequestOptions] = None
    ) -> Dict[str, Union[bool, Dict[str, Union[str, int]]]]:
        fetch_url = self.build_metadata_url(url, options)
        async with aiohttp.ClientSession() as session:
            async with session.get(URL(fetch_url, encoded=True)) as response:
                response.raise_for_status()
                return await response.json()

    async def fetch_animated(self, url: str, options: Optional[RequestOptions] = None) -> bytes:
        fetch_url = self.build_animated_url(url, options)
        async with aiohttp.ClientSession() as session:
            async with session.get(URL(fetch_url, encoded=True)) as response:
                response.raise_for_status()
                return await response.read()
