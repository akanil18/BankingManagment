from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "BankingManagementSystem"
    APP_ENV: str = "development"
    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 40

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    REDIS_URL: str = "redis://localhost:6379/0"
    RATE_LIMIT_PER_MINUTE: int = 10

    LLAMA_SERVER_URL: str = "http://localhost:8080/v1"
    LLAMA_MODEL_NAME: str = "qwen-banking"
    LLAMA_MAX_TOKENS: int = 1024
    LLAMA_TEMPERATURE: float = 0.1

    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: str = "xlsx,xls,csv"
    UPLOAD_DIR: str = "./uploads"

    CORS_ORIGINS: str = "http://localhost:8080,http://localhost:3000"

    AGENT_TOP_K_RESULTS: int = 5
    AGENT_MAX_CONVERSATION_HISTORY: int = 20

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    @property
    def allowed_extensions_list(self) -> List[str]:
        return [e.strip() for e in self.ALLOWED_EXTENSIONS.split(",")]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
