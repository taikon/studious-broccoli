import os
import pathlib
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

# The parent's parent of ./fastapi/core/config.py is ./fastapi/
ROOT_PATH = pathlib.Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    CORS_ORIGINS: list = [
        os.getenv("CORS_ORIGIN_REACT"),
    ]
    ACCESS_TOKEN: str = os.getenv("ACCESS_TOKEN")
    OLLAMA_API_ENDPOINT: str = os.getenv("OLLAMA_API_ENDPOINT")
    GRADIO_API_ENDPOINT: str = os.getenv("GRADIO_API_ENDPOINT")

    # OCR Settings
    OCR_MODEL: str = 'openbmb/MiniCPM-Llama3-V-2_5'
    DEVICE: str = 'cuda'

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

