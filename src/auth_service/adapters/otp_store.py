import asyncio
from pathlib import Path
from auth_service.entities.otp import Otp

from auth_service.entities.store import OtpStore, OtpStoreErrors
from pydantic.dataclasses import dataclass
import json
import aiofiles

@dataclass
class InMemoryOtpStoreConf:
    otp_file: Path

otp_lock = asyncio.Lock()

@dataclass
class InMemoryOtpStore(OtpStore):
    config: InMemoryOtpStoreConf

    def __post_init__(self):
        self.otps = {}
        if not self.config.otp_file.exists():
            self.config.otp_file.touch()
        with open(self.config.otp_file, "r+") as f:
            for r in f.readlines():
                otp =Otp(**json.loads(r))
                self.otps[otp.session_id] = otp
    

    async def save(self, otp: Otp) -> Otp:
        if otp.session_id in self.otps:
            raise OtpStoreErrors.AlreadyExists("Otp already exist")
        await self._save(otp)
        return otp
        

    async def get(self, session_id: str) -> Otp:
        if session_id not in self.otps:
            raise OtpStoreErrors.NotFoundError("Otp not found")
        async with otp_lock:
            otp = self.otps[session_id]
        return otp
    
    async def mark_checked(self, otp: Otp):
        otp.checked = True
        await self._save(otp)
        
    async def _save(self, otp: Otp) -> Otp:
        async with otp_lock:
            self.otps[otp.session_id] = otp
        async with aiofiles.open(self.config.otp_file, mode='a') as handle:
            await handle.write(otp.model_dump_json() + "\n")
        return otp