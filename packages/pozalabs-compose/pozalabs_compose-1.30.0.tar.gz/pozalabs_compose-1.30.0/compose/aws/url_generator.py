from __future__ import annotations

import urllib.parse
from typing import TYPE_CHECKING

from compose.types import ContentDisposition

if TYPE_CHECKING:
    import mypy_boto3_s3

type Seconds = int


class S3UrlGenerator:
    def __init__(
        self,
        s3_client: mypy_boto3_s3.Client,
        bucket: str | None = None,
        expires_in: Seconds = 3600,
    ):
        self.s3_client = s3_client
        self.bucket = bucket
        self.expires_in = expires_in

    def generate_download_url(
        self,
        key: str,
        filename: str | None = None,
        bucket: str | None = None,
        expires_in: Seconds | None = None,
        params: dict[str, str] | None = None,
    ) -> str:
        if (bucket := bucket or self.bucket) is None:
            raise ValueError("`bucket` must be provided if default bucket is not set")

        filename = urllib.parse.quote(filename or key.split("/")[-1])
        default_params = {
            "Bucket": bucket,
            "Key": key,
            "ResponseContentDisposition": ContentDisposition.attachment(filename),
        }
        return self.s3_client.generate_presigned_url(
            "get_object",
            Params=default_params | (params or {}),
            ExpiresIn=expires_in or self.expires_in,
        )

    def generate_upload_url(
        self,
        key: str,
        bucket: str | None = None,
        expires_in: Seconds | None = None,
        params: dict[str, str] | None = None,
    ) -> str:
        if (bucket := bucket or self.bucket) is None:
            raise ValueError("`bucket` must be provided if default bucket is not set")

        return self.s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": bucket, "Key": key} | (params or {}),
            ExpiresIn=expires_in or self.expires_in,
        )
