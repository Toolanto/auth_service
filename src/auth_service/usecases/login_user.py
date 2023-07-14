from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from pydantic import BaseModel, Field, constr
from auth_service import SECRET
from auth_service.entities.gateway import EmailGateway
from auth_service.entities.otp import Otp
from auth_service.entities.store import OtpStore, UserStore
from auth_service.entities import encode
import random
import uuid

from auth_service.entities.user import User

OTP_LENGTH = 5
OTP_MINUTES_LIFE = 5


class LoginUserErrors:

    class InvalidCredentials(Exception):
        pass

class LoginUserData(BaseModel):
    email: constr(min_length=1) = Field(..., description="The user email")
    password: constr(min_length=1) = Field(..., description="The user password")

class LoginUserRes(BaseModel):
    session_id: Optional[str] = None
    token: Optional[str] = None


class LoginUserUsecase(BaseModel):
    user_store: UserStore
    otp_store: OtpStore
    email_gateway: EmailGateway

    class Config:
        arbitrary_types_allowed = True

    async def execute(self, req: LoginUserData) -> LoginUserRes:
        user = await self.user_store.get(email=req.email)
        
        if not user.is_valid_password(req.password):
            raise LoginUserErrors.InvalidCredentials("Invalid credentials")
        
        if not user.two_factor_auth_enabled:
            jwt_token = jwt.encode({"email": user.email}, SECRET, algorithm="HS256")
            return LoginUserRes(token = jwt_token)
        

        otp = self._generate_otp(user=user)
        await self.otp_store.save(otp=otp)
        
        body =  f"Hi {user.name}, the OTP is {otp.value}"
        await self.email_gateway.send(to_recipient=user.email, subject="OTP", body=body)
        return LoginUserRes(session_id=otp.session_id)
    
    def _generate_otp(self, user:User) -> Otp:
        now = datetime.now(tz=timezone.utc)
        value = ''.join(str(random.randint(0, 9)) for _ in range(OTP_LENGTH))
        return Otp(
            session_id=str(uuid.uuid4()),
            value=value,
            created=now,
            expired=now + timedelta(minutes=OTP_MINUTES_LIFE),
            email=user.email
        )

    
            
        
        
