from __future__ import annotations

from typing import Any, Dict, BinaryIO
import os

from luna.http import HttpClient
from luna.http.types import RequestConfig
from luna.types import Bucket, BucketList, FileObject
from luna.errors import LunaError, ErrorCode, create_error


class BucketsResource:
    """Manages storage buckets."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client
        self._base_path = "/v1/storage/buckets"

    async def get(self, bucket_id: str) -> Bucket:
        """Get a bucket by ID."""
        resp = await self._client.request(
            RequestConfig(
                method="GET",
                path=f"{self._base_path}/{bucket_id}",
            )
        )
        return Bucket.model_validate(resp.data)

    async def list(self) -> BucketList:
        """List all buckets."""
        resp = await self._client.request(
            RequestConfig(
                method="GET",
                path=self._base_path,
            )
        )
        return BucketList.model_validate(resp.data)

    async def upload(
        self, 
        bucket_id: str, 
        file: BinaryIO | bytes, 
        filename: str | None = None,
        metadata: Dict[str, str] | None = None
    ) -> FileObject:
        """
        Upload a file to a bucket.
        
        Args:
            bucket_id: The ID of the bucket.
            file: File-like object or bytes.
            filename: Optional filename.
            metadata: Optional key-value metadata.
        """
        files = {"file": (filename or "upload", file)}
        data = {"metadata": metadata} if metadata else {}
        
        resp = await self._client.request(
            RequestConfig(
                method="POST",
                path=f"{self._base_path}/{bucket_id}/upload",
                files=files,
                body=data,
            )
        )
        return FileObject.model_validate(resp.data)


class FilesResource:
    """Manages file operations."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client
        self._base_path = "/v1/storage/files"

    async def get_download_url(self, id: str) -> str:
        """Get download URL for a file."""
        resp = await self._client.request(
            RequestConfig(
                method="GET",
                path=f"{self._base_path}/{id}/download",
            )
        )
        
        if isinstance(resp.data, dict) and "url" in resp.data:
             return str(resp.data["url"])
        
        raise LunaError(
            code=ErrorCode.RESOURCE_NOT_FOUND,
            message="Download URL not found in response",
            status=404,
            request_id=resp.request_id
        )


class StorageResource:
    """Storage Service resources."""

    def __init__(self, client: HttpClient) -> None:
        self.buckets = BucketsResource(client)
        self.files = FilesResource(client)
