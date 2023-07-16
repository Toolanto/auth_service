import random
import uuid
from datetime import datetime, timedelta

import jwt

from auth_service.entities.otp import Otp
from auth_service.entities.user import User

SECRET = "secret"
JWT_TIME_LIFE_MINUTES = 30

OTP_LENGTH = 5
OTP_MINUTES_LIFE = 5


def get_jwt_token(user: User, current_time: datetime) -> str:
    payload = {
        "email": user.email,
        "expired": (current_time + timedelta(minutes=JWT_TIME_LIFE_MINUTES)).isoformat(),
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


def get_otp(user: User, current_time: datetime) -> Otp:
    value = "".join(str(random.randint(0, 9)) for _ in range(OTP_LENGTH))
    return Otp(
        id=str(uuid.uuid4()),
        value=value,
        created=current_time,
        expired=current_time + timedelta(minutes=OTP_MINUTES_LIFE),
        user_id=user.id,
    )
