"""
The only code in the project that talks to S3. Every other app calls these functions.

One private bucket, one folder per class. Keys always start with classes/<class_id>/.
Nobody gets direct bucket access. The backend checks class membership, then hands
out a short lived presigned URL.
"""

from functools import lru_cache

import boto3
from django.conf import settings


@lru_cache(maxsize=1)
def _client():
    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT_URL,
        region_name=settings.S3_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


def class_key(class_id, *parts) -> str:
    """Build an S3 key inside a class's folder, e.g. classes/<id>/uploads/<file_id>/lecture.pdf"""
    clean = [str(p).strip("/") for p in parts]
    return "/".join([f"classes/{class_id}", *clean])


def presign_upload(key: str, content_type: str) -> str:
    return _client().generate_presigned_url(
        "put_object",
        Params={"Bucket": settings.S3_BUCKET, "Key": key, "ContentType": content_type},
        ExpiresIn=settings.S3_PRESIGN_SECONDS,
    )


def presign_download(key: str, filename: str | None = None) -> str:
    params = {"Bucket": settings.S3_BUCKET, "Key": key}
    if filename:
        params["ResponseContentDisposition"] = f'attachment; filename="{filename}"'
    return _client().generate_presigned_url("get_object", Params=params, ExpiresIn=settings.S3_PRESIGN_SECONDS)


def put_bytes(key: str, data: bytes, content_type: str = "application/octet-stream") -> None:
    _client().put_object(Bucket=settings.S3_BUCKET, Key=key, Body=data, ContentType=content_type)


def get_bytes(key: str) -> bytes:
    return _client().get_object(Bucket=settings.S3_BUCKET, Key=key)["Body"].read()


def exists(key: str) -> bool:
    try:
        _client().head_object(Bucket=settings.S3_BUCKET, Key=key)
        return True
    except _client().exceptions.ClientError:
        return False
