from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    DATABASE_URL: str

    @property
    def async_database_url(self) -> str:

        url = self.DATABASE_URL

        if not os.getenv("RUNNING_IN_DOCKER"):
            url = url.replace("@db:", "@localhost")
        return url

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()