from pathlib import Path
from uuid import uuid4
import boto3
from app.core.config import get_settings


class R2StorageService:
    def __init__(self) -> None:
        settings = get_settings()
        self.bucket = settings.r2_bucket
        self.local_dir = Path("/tmp/sheetmind-storage")
        self.use_local = not (settings.r2_endpoint_url and settings.r2_access_key_id and settings.r2_secret_access_key)
        if self.use_local:
            self.local_dir.mkdir(parents=True, exist_ok=True)
            self.client = None
        else:
            self.client = boto3.client(
                "s3",
                endpoint_url=settings.r2_endpoint_url,
                aws_access_key_id=settings.r2_access_key_id,
                aws_secret_access_key=settings.r2_secret_access_key,
                region_name=settings.r2_region,
            )

    def put(self, owner_id: int, filename: str, data: bytes, content_type: str) -> str:
        key = f"users/{owner_id}/{uuid4()}-{filename}"
        if self.use_local:
            path = self.local_dir / key
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            return key
        assert self.client is not None
        from io import BytesIO
        self.client.upload_fileobj(BytesIO(data), self.bucket, key, ExtraArgs={"ContentType": content_type})
        return key

    def get(self, key: str) -> bytes:
        if self.use_local:
            return (self.local_dir / key).read_bytes()
        assert self.client is not None
        obj = self.client.get_object(Bucket=self.bucket, Key=key)
        return obj["Body"].read()
