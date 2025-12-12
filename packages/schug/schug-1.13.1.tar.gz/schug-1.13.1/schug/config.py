from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DEMO_DB: str = "sqlite://"
SCHUG_PACKAGE = Path(__file__).parent
PACKAGE_ROOT: Path = SCHUG_PACKAGE.parent
ENV_FILE: Path = PACKAGE_ROOT / ".env"


class Settings(BaseSettings):
    """Settings for serving the schug app"""

    model_config = SettingsConfigDict(env_file=str(ENV_FILE))
    db_uri: str = DEMO_DB
    host: str = "localhost"
    port: int = 8000


settings = Settings()
