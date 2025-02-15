from functools import lru_cache
import urllib.parse

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool
    SECRET_KEY: SecretStr

    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_NAME: str

    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def DATABASE_URL(self):
        password = self.POSTGRES_PASSWORD.get_secret_value()
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{urllib.parse.quote_plus(password)}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
