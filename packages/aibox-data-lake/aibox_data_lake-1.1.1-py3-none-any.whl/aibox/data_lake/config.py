"""Configurações da biblioteca."""

import json
from pathlib import Path
from typing import Annotated

import platformdirs
from pydantic import AfterValidator, AnyUrl
from pydantic_settings import BaseSettings, JsonConfigSettingsSource


class BucketUrl(AnyUrl):
    allowed_schemes = ["s3", "gs"]

    @classmethod
    def validate(cls, value: str) -> str:
        cls(value)
        return value


class Config(BaseSettings):
    model_config = {"env_prefix": "AIBOX_DL_"}

    registered_buckets: dict[str, Annotated[str, AfterValidator(BucketUrl.validate)]]

    def save_to_file(self):
        """Salva as configurações para o JSON
        padrão.
        """
        path = self.local_file_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.model_dump_json(indent=2), encoding="utf-8")

    @classmethod
    def local_file_path(cls) -> Path:
        """Obtém o caminho padrão das
        configurações.

        Returns:
            Path: caminho para configuração.
        """
        return Path(platformdirs.user_config_dir(appname="data_lake", appauthor="aibox")).joinpath(
            "config.json"
        )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        order = [init_settings, env_settings]
        path = cls.local_file_path()
        if path.exists():
            try:
                data = json.loads(path.read_text("utf-8"))
                # Validate expected format for current version
                if "registered_buckets" in data and len(data) == 1:
                    order.append(JsonConfigSettingsSource(settings_cls, json_file=path))
            except:
                pass

        order.append(file_secret_settings)
        return tuple(order)
