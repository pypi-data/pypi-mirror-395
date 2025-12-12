from __future__ import annotations

from typing import TYPE_CHECKING

import botocore.exceptions

if TYPE_CHECKING:
    import mypy_boto3_s3


def s3_obj_exists(s3_client: mypy_boto3_s3.S3Client, bucket: str, key: str) -> bool:
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except botocore.exceptions.ClientError as exc:
        if exc.response["Error"]["Code"] == "404":
            return False

        raise exc
