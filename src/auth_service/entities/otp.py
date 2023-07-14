from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Otp(BaseModel):
    session_id: str
    value: str
    created: datetime
    expired: datetime
    checked: Optional[bool] = False
    email: str

    class Config:
        arbitrary_types_allowed = True


    def is_valid_otp(self, otp: str, current_time: datetime) -> bool:
        return all([
            otp == self.value, 
            current_time < self.expired,
            not self.checked
        ])
    