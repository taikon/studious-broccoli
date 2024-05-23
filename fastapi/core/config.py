import os
import pathlib
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

# The parent's parent of .app/app/core/config.py is .app/app/
ROOT_PATH = pathlib.Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    CORS_ORIGINS: list = [os.getenv("CORS_ORIGIN")]
    HUGGING_FACE_SERVERLESS_INFERENCE_API_KEY: str = os.getenv("HUGGING_FACE_SERVERLESS_INFERENCE_API_KEY")
    HUGGING_FACE_MODEL: str = os.getenv("HUGGING_FACE_MODEL")

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

