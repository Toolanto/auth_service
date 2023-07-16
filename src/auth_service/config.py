from venv import logger

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

load_dotenv()


class DbConfig(BaseSettings):
    db_url: str = Field(env="DB_URL")


class Settings(BaseModel):
    db_config: DbConfig() = DbConfig()


def load():
    try:
        return Settings()
    except Exception as err:
        logger.error(f"error loading configuration: {err}")
