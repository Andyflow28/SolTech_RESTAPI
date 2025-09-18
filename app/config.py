from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    API_KEY: str
    SECRET_KEY: str
    CORS_ORIGINS: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Para desarrollo local usa .env, para producción usa variables de entorno
    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()