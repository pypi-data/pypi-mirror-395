'''
example usage:
client = AuthentaClient(
    base_url="https://platform.authenta.ai/api",
    client_id="...",
    client_secret="...",
)

'''

import os
import time
import mimetypes
from typing import Any, Dict, Optional

import requests


class AuthentaClient:
    """
    Authenta Python SDK.

    Features:
    - Builds Auth headers with x-client-id / x-client-secret.
    - Wraps /media endpoints for create, get, list, delete.
    - Implements two-step upload (POST /media -> PUT to S3).
    - Process deepfake-detection
    """

    def __init__(self, base_url: str, client_id: str, client_secret: str):
        """
        Create new Authenta client

        Args:
            base_url: Authenta API base URL, e.g. "https://platform.authenta.ai/api" or platform base URL : "https://platform.authenta.ai".
            client_id: Your Authenta client ID.
            client_secret: Your Authenta client secret.
        """
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret

    def _headers(self) -> Dict[str, str]:
        """Return default headers for Authenta API calls."""
        return {
            "x-client-id": self.client_id,
            "x-client-secret": self.client_secret,
            "Content-Type": "application/json",
        }

    def _content_type(self, path: str) -> str:
        """
        Guess the MIME type for a file path.

        Falls back to 'application/octet-stream' if unknown.
        """
        filetype, _ = mimetypes.guess_type(path)
        return filetype or "application/octet-stream"

    def create_media(
        self,
        name: str,
        content_type: str,
        size: int,
        model_type: str,
    ) -> Dict[str, Any]:
        """
        POST /media: create a media record and get an upload URL.

        Args:
            name: Original file name.
            content_type: MIME type of the file (e.g. "image/png", "video/mp4").
            size: File size in bytes.
            model_type: Detection model type, e.g. "AC-1" or "DF-1".
            "AC-1" - Image
            "DF-1" - Video

        Returns:
            Parsed JSON response containing at least 'mid' and 'uploadUrl'.
        """
        url = f"{self.base_url}/media"
        payload = {
            "name": name,
            "contentType": content_type,
            "size": size,
            "modelType": model_type,
        }
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_media(self, mid: str) -> Dict[str, Any]:
        """
        GET /media/{mid}: fetch a single media record.

        Args:
            mid: Media ID returned by create_media / upload_file.

        Returns:
            Parsed JSON media record.
        """
        url = f"{self.base_url}/media/{mid}"
        resp = requests.get(url, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()

    def upload_file(self, path: str, model_type: str) -> Dict[str, Any]:
        """
        Upload a file via the two-step Authenta media flow.

        Steps:
            1) POST /media to create the record and obtain 'mid' + 'uploadUrl'.
            2) PUT the file bytes to the presigned S3 'uploadUrl'.

        Args:
            path: Local path to the media file.
            model_type: Detection model type to use, e.g. "AC-1" or "DF-1".

        Returns:
            The JSON response from POST /media (includes 'mid', 'status', etc.).
        """
        filename = os.path.basename(path)
        content_type = self._content_type(path)
        size = os.path.getsize(path)

        # Step 1: create media
        meta = self.create_media(
            name=filename,
            content_type=content_type,
            size=size,
            model_type=model_type,
        )
        upload_url = meta.get("uploadUrl")
        if not upload_url:
            raise RuntimeError("No uploadUrl in create_media response")

        # Step 2: upload to S3
        with open(path, "rb") as f:
            put_resp = requests.put(
                upload_url,
                data=f,
                headers={"Content-Type": content_type},
                timeout=300,
            )
        put_resp.raise_for_status()
        return meta

    def wait_for_media(self, 
                       mid: str, 
                       interval: float = 5.0, 
                       timeout: float = 600.0, 
                      ) -> Dict[str, Any]:
        
        start = time.time()
        while True:
            media = self.get_media(mid)
            status = (media.get("status") or "").upper()
            if status in {"PROCESSED", "FAILED", "ERROR"}:
                return media
            if time.time() - start > timeout:
                raise TimeoutError(f"Timed out waiting for media {mid}, last status={status!r}")
            time.sleep(interval)

    def list_media(self, **params) -> Dict[str, Any]:
        """
        GET /media: list media for this client.
        Accepts optional query params (page, pageSize, filters) if the API supports them.
        """
        url = f"{self.base_url}/media"
        resp = requests.get(url, headers=self._headers(), params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def process(self,
                path: str,
                model_type: str,
                interval: float = 5.0,
                timeout: float = 600.0,
                ) -> Dict[str, Any]:
        """
        High-level helper:
          1) upload_file(path, model_type) -> get mid
          2) wait_for_media(mid)
        """
    
        meta = self.upload_file(path, model_type=model_type)
        mid = meta.get("mid")
        if not mid:
            raise RuntimeError("No 'mid' in upload response")
        return self.wait_for_media(mid, interval=interval, timeout=timeout)



    def delete_media(self, mid: str) -> None:
        
        """ DELETE /media/{mid}: delete a media record """
        
        url = f"{self.base_url}/media/{mid}"
        resp = requests.delete(url, headers=self._headers(), timeout=30)
        resp.raise_for_status()

    
        
