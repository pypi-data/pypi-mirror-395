from functools import cached_property
from pathlib import Path

import pandas as pd

from .bucket import Blob, Bucket
from .dataset import Dataset, DatasetInfo


class TabularDataset(Dataset):
    """Dataset tabular.

    Essa classe permite o carregamento
    de datasets armazenados em buckets
    de forma particionada ou não.

    A estrutura do dataset carregada é:
        <prefix>
        ├── <subpath>
        │   ├── <...>.parquet
        │   └── <...>.parquet
        ├── <subpath>
        │   └── <subpath>
        │       └── <...>.parquet
        └── ...

    Todos os `.parquet` dentro do prefixo
    são tratados como parte do mesmo dataset.
    """

    def __init__(self, bucket: Bucket, prefix: str, extension: str = "parquet"):
        if extension not in {"parquet", "csv"}:
            raise ValueError(f"Extension format not supported: '{extension}'.")

        self._bucket = bucket
        self._prefix = prefix.rstrip("/")
        self._extension = extension
        self._blobs = self._bucket.list(
            prefix=f"{self._prefix}/",
            glob=f"**/*.{self._extension}",
        )

        if not self._blobs:
            raise ValueError(f"Data source not found on bucket {self._bucket.name}.")

    @cached_property
    def info(self) -> DatasetInfo:
        return DatasetInfo(
            name=self._prefix,
            n_blobs=len(self.blobs),
            bucket=self._bucket.name,
            total_bytes=sum(blob.size for blob in self.blobs),
        )

    @property
    def bucket(self) -> Bucket:
        return self._bucket

    @property
    def blobs(self) -> list[Blob]:
        return self._blobs

    def to_frame(self) -> pd.DataFrame:
        load = pd.read_parquet if self._extension == "parquet" else pd.read_csv
        dfs = []
        for blob in self.blobs:
            dfs.append(load(blob.as_stream()))
        return pd.concat(dfs, ignore_index=True)

    def to_table(self):
        raise NotImplementedError()

    def download_to_local(self, directory: Path | str, overwrite: bool = False):
        directory = Path(directory)
        directory.mkdir(exist_ok=True, parents=True)
        if next(directory.rglob("*"), None) is not None and not overwrite:
            raise ValueError("Directory not empty.")

        for b in self.blobs:
            file_path = directory.join(b.path.replace(f"{self._prefix}/"))
            b.download_to_local(file_path, overwrite=True)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.info.name}', bucket='{self.info.bucket}')"
