from typing import Optional
from venv import logger
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from auth_service.adapters import email_gateway

load_dotenv()

class UserStore(BaseSettings):
    user_file: str = Field(env="USER_FILE")

class OtpStore(BaseSettings):
    otp_file: str = Field(env="OTP_FILE")

class Settings(BaseModel):
    user_store: UserStore = UserStore()
    otp_store: OtpStore = OtpStore()



def load():
    try:
        return Settings()
    except Exception as err:
        logger.error(f"error loading configuration: {err}")
