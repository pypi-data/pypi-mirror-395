"""Implementações das interfaces
básicas para o GCP.
"""

from functools import cached_property
from io import BytesIO
from pathlib import Path

from google.cloud import storage

from .core import Blob, Bucket

_CLIENT = storage.Client()


class GCSBlob(Blob):
    def __init__(self, blob: storage.Blob):
        self._blob = blob

    @property
    def bucket(self) -> Bucket:
        return GCSBucket(self._blob.bucket.name)

    @cached_property
    def name(self) -> str:
        return super().name

    @cached_property
    def path(self) -> str:
        return self._blob.name

    @cached_property
    def size(self) -> int:
        return self._blob.size or 0

    def download_to_local(self, file_path: Path | str, overwrite: bool = False):
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if file_path.exists() and not overwrite:
            raise ValueError(f"File already exists: {file_path}.")

        self._blob.download_to_filename(str(file_path), client=_CLIENT)

    def as_stream(self) -> BytesIO:
        return BytesIO(self._blob.download_as_bytes(client=_CLIENT))

    def delete(self) -> bool:
        try:
            self._blob.delete(client=_CLIENT)
        except:
            return False

        return True


class GCSBucket(Bucket):
    def __init__(self, bucket_name: str):
        super().__init__(bucket_name)
        self._bucket = _CLIENT.bucket(bucket_name)
        if not self._bucket.exists():
            raise ValueError(f"Bucket '{bucket_name}' not found.")

    @property
    def uri(self) -> str:
        return f"gs://{self._bucket.name}"

    def list(self, prefix: str | None = None, glob: str | None = None) -> list[Blob]:
        return [GCSBlob(blob) for blob in self._bucket.list_blobs(prefix=prefix, match_glob=glob)]

    def get(self, name: str) -> Blob:
        return GCSBlob(self._bucket.get_blob(name))
