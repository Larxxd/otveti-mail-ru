from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    secret_key: str
    algorithm: str

    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / ".env")
    
settings = Settings(**{})