import os
from functools import lru_cache
from pathlib import Path

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent  # orion/config
PROJECT_ROOT = BASE_DIR.parent  # orion/




class Settings(BaseSettings):
    # === Ejemplos de configuración ===
    LOG_LEVEL: str

    URL_DB_EMPATIA: str
    URL_DB_BELLATRIX: str

    ENDPOINT_API_SOFTIN_VILLACRUZ: str
    ENDPOINT_API_SOFTIN_CASTILLO: str
    ENDPOINT_API_SOFTIN_ALQUIVENTAS: str
    ACCESS_TOKEN_SOFTIN_VILLACRUZ: str
    ACCESS_TOKEN_SOFTIN_CASTILLO: str
    ACCESS_TOKEN_SOFTIN_ALQUIVENTAS: str

    USERNAME_SIMI: str
    PASSWORD_SIMI: str

    HOST_SERVER_FTP: str
    USER_SERVER_FTP: str
    PASSWORD_SERVER_FTP: str

    SUBJECT_MLS_ACRECER: str

    model_config = SettingsConfigDict(
        # env_file=_optional_env_file(),
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Carga configuración la primera vez que una tarea lo necesita.
    Invócalo dentro del callable de cada tarea (runtime, no import).
    """
    try:
        # print(f"{_optional_env_file()=}")
        s = Settings()

        # logger.info(f"[settings] PYTHON_ENV_ORION={s.model_config.get('env_file')}")
        logger.info(f"[settings] PYTHON_ENV_ORION={os.getenv('PYTHON_ENV_ORION')=}")
        logger.info(f"{s.URL_DB_BELLATRIX=}")
        logger.info(f"{s.URL_DB_EMPATIA=}")
        logger.debug(f"[settings] LOG_LEVEL={s.LOG_LEVEL}")
        return s
    except Exception as e:
        logger.error(f"[settings] Error cargando settings: {e}")
        raise
