"""Interface para interação com
buckets.
"""

from abc import ABC, abstractmethod
from io import BytesIO
from pathlib import Path
from typing import IO

from smart_open import open


class Blob(ABC):
    """Interface para objetos
    armazenados em buckets.

    Essa classe não armazena o
    conteúdo de um objeto diretamente,
    apenas uma referência para o objeto
    dentro do bucket.

    Para acessar o conteúdo, algum dos
    métodos de leitura deve ser utilizado.
    """

    @property
    @abstractmethod
    def bucket(self) -> "Bucket":
        """Bucket que contém
        esse blob.
        """

    @property
    def name(self) -> str:
        """Nome do blob.

        É a última parte do
        caminho absoluto.
        """
        return self.path.rstrip("/").split("/")[-1]

    @property
    @abstractmethod
    def path(self) -> str:
        """Caminho absoluto do
        blob com relação a
        raiz do bucket.
        """

    @property
    @abstractmethod
    def size(self) -> int:
        """Tamanho total do blob
        em bytes.
        """

    @abstractmethod
    def download_to_local(self, file_path: Path | str, overwrite: bool = False):
        """Realiza a transferência do objeto
        remoto para um arquivo local.

        Args:
            file_path: caminho para o
                salvamento do objeto.
            overwrite: se o arquivo deve
                ser sobrescrito casa exista.
        """

    @abstractmethod
    def as_stream(self) -> BytesIO:
        """Retorna o objeto como
        uma stream de bytes.

        Returns:
            BytesIO: conteúdo do
                objeto.
        """

    @abstractmethod
    def delete(self) -> bool:
        """Remove esse objeto do
        bucket remoto.

        Returns:
            bool: True se a deleção
                foi um sucesso, False
                do contrário.
        """

    def open(self, mode: str, **kwargs) -> IO:
        """Abre esse objeto.

        Args:
            mode: modo de abertura.
            **kwargs: parâmetros extras a serem
                passados para smart_open.open(...).

        Returns:
            IO: file object.
        """
        return self.bucket.open(self.name, mode, **kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}" f"(path='{self.path}', bucket" f"='{self.bucket.name}')"


class Bucket(ABC):
    """Interface para buckets.

    Um bucket é um container para
    diferentes objetos, com tipos
    e formatos variados.
    """

    def __init__(self, bucket_name: str):
        self._name = bucket_name

    @property
    @abstractmethod
    def uri(self) -> str:
        """URI do bucket.

        Returns:
            str: identificador do bucket
                com o schema (e.g., s3://,
                gs://).
        """

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def list(self, prefix: str | None = None, glob: str | None = None) -> list[Blob]:
        """Realiza uma listagem de todos os
        objetos presentes no bucket.

        Args:
            prefix: prefixo para filtragem
                dos blobs. Padrão é sem
                filtros.
            glob: GLOB para filtragem dos
                blobs. Padrão é sem filtros.

        Returns:
            list[Blob]: objetos presentes
                no bucket.
        """

    @abstractmethod
    def get(self, name: str) -> Blob | None:
        """Obtém um objeto no bucket
        com o nome passado.

        Caso o objeto não existe, retorna
        None.

        Args:
            name: nome do objeto.

        Returns:
            Blob: objeto ou None..
        """

    def exists(self, name: str) -> bool:
        """Checa se o objeto com o nome
        passado existe no bucket.

        Args:
            name: nome do objeto.

        Returns:
            bool: True se existe, False
                caso contrário.
        """
        return self.get(name) is not None

    def open(self, name: str, mode: str, **kwargs) -> IO:
        """Abre um objeto no bucket.

        Retorna um objeto igual ao retornado
        por open(...).

        Args:
            name: nome do objeto.
            mode: modo de abertura.
            **kwargs: parâmetros extras a serem
                passados para smart_open.open(...).

        Returns:
            IO: file object.
        """
        path = "/".join([self.uri, name])
        return open(path, mode=mode, **kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
