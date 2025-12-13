import logging
from abc import ABC, abstractmethod
from pathlib import Path

import ibis
import pandas as pd
from pydantic import BaseModel

from .bucket import Blob, Bucket

LOGGER = logging.getLogger(__name__)


class DatasetInfo(BaseModel):
    name: str
    n_blobs: int
    bucket: str
    total_bytes: int


class Dataset(ABC):

    @property
    @abstractmethod
    def info(self) -> DatasetInfo:
        """Retorna informações gerais
        sobre o dataset.

        Returns:
            DatasetInfo: informações.
        """

    @property
    @abstractmethod
    def bucket(self) -> Bucket:
        """Bucket que esse dataset
        faz parte.

        Returns:
            Bucket: bucket.
        """

    @property
    @abstractmethod
    def blobs(self) -> list[Blob]:
        """Blobs que constituem o
        dataset.

        Returns:
            list[Blob]: blobs.
        """

    @abstractmethod
    def to_frame(self) -> pd.DataFrame:
        """Carrega o dataset em um
        DataFrame.

        Returns:
            pd.DataFrame: DataFrame.
        """

    @abstractmethod
    def to_table(self) -> ibis.Table:
        """Carrega o dataset em uma
        tabela do Ibis (DuckDB).

        Returns:
            ibis.Table: tabela.
        """
        raise NotImplementedError("Ibis table aren't supported yet.")

    @abstractmethod
    def download_to_local(self, directory: Path | str, overwrite: bool = False):
        """Realiza o download de todos os
        blobs do dataset para um diretório
        local.

        Os arquivos são salvos com a mesma
        estrutura do bucket remoto, exceto
        o prefixo.
        """
