from appdirs import user_data_dir  # type: ignore
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

default_data_dir = user_data_dir("LlamaFarm", "LlamaFarm")


class Settings(BaseSettings, env_file=".env"):
    LOG_JSON_FORMAT: bool = False
    LOG_LEVEL: str = "INFO"
    LOG_NAME: str = "server"
    LOG_ACCESS_NAME: str = "server.access"

    lf_use_data_dir: bool = False
    lf_project_dir: str | None = None
    lf_data_dir: str = default_data_dir
    lf_config_template: str = "default"  # e.g. default, rag, completion, chat

    # Ollama Configuration
    designer_ollama_host: str = "http://localhost:11434"
    designer_ollama_model: str = "llama3.1:8b"
    designer_ollama_api_key: str = "ollama"

    runtime_ollama_host: str = "http://localhost:11434"
    runtime_ollama_api_key: str = "ollama"


settings = Settings()
