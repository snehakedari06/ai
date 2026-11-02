import os
from typing import Optional

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    # Fallback for Pydantic v1 or environments without pydantic-settings
    try:
        from pydantic import BaseSettings  # type: ignore
    except ImportError:
        # Minimal fallback if Pydantic is not installed yet
        class BaseSettings:  # type: ignore
            def __init__(self):
                self.APP_ENV = os.getenv("APP_ENV", "development")
                self.PORT = int(os.getenv("PORT", "8000"))
                self.LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
                self.MODEL_NAME = os.getenv("MODEL_NAME", "dummy-model")
                self.MODEL_PATH = os.getenv("MODEL_PATH", "models/dummy-model")

# Dummy SettingsConfigDict fallback if not imported
try:
    SettingsConfigDict
except NameError:
    SettingsConfigDict = dict  # type: ignore

class Settings(BaseSettings):
    APP_ENV: str = "development"
    PORT: int = 8000
    LOG_LEVEL: str = "info"
    
    # Model settings
    MODEL_NAME: Optional[str] = "dummy-model"
    MODEL_PATH: Optional[str] = "models/dummy-model"

    # Modern configuration dictionary (Pydantic v2)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Instantiate global settings
settings = Settings()
