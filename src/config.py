from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "PinLens API"
    ENVIRONMENT: str = "development"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    OPENAI_API_KEY: str = "mock-key-for-dev"

    class Config:
        env_file = ".env"

settings = Settings()