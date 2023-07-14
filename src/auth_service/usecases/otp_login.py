import jwt
from pydantic import BaseModel, Field, constr
from auth_service import SECRET
from auth_service.entities.store import OtpStore, OtpStoreErrors, UserStore
from datetime import datetime, timezone

class OtpLoginErrors:

    class InvalidCredentials(Exception):
        pass

class OtpLoginData(BaseModel):
    session_id: constr(min_length=1) = Field(..., description="The OTP session_id. Only for user with 2FA enabled.")
    otp: constr(min_length=1) = Field(..., description="The OTP value received by email.")


class OtpLoginUsecase(BaseModel):
    user_store: UserStore
    otp_store: OtpStore

    class Config:
        arbitrary_types_allowed = True

    async def execute(self, req: OtpLoginData) -> str:
        try:
            otp = await self.otp_store.get(session_id=req.session_id)
        except OtpStoreErrors.NotFoundError:
            raise OtpLoginErrors.InvalidCredentials("Invalid OTP")
        
        current_time = datetime.now(tz= timezone.utc)
        if not otp.is_valid_otp(otp=req.otp, current_time=current_time):
            raise OtpLoginErrors.InvalidCredentials("Invalid OTP")
        
        user = await self.user_store.get(email=otp.email)
        jwt_token =  jwt.encode({"email": user.email}, SECRET, algorithm="HS256")
        
        await self.otp_store.mark_checked(otp=otp)
        return jwt_token
        
        
        
        
    


    
            
        
        
