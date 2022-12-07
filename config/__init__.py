"""
Config load
"""
import os
from pathlib import Path
from functools import lru_cache
from pydantic import BaseSettings

# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """
    Settings of the service
    """

    log_level: str = "DEBUG"
    appservice_url: str = "http://appservice:8000"
    data_service_url: str = "http://dataservice"
    source_scenario_id: str = None
    target_scenario_id: str = None

    class Config:
        """
        Config settings
        """

        ENV = os.getenv("ENV", "prod")
        env_file = f"{Path(__file__).parent}/{ENV}.env"


@lru_cache()
def get_settings() -> Settings:
    """
    get settings of the service
    """
    return Settings()


settings = get_settings()
