import asyncio
from pathlib import Path

from auth_service.entities.user import User
from auth_service.entities.store import UserStore, UserStoreErrors
from pydantic.dataclasses import dataclass
import json
import aiofiles

@dataclass
class InMemoryUserStoreConf:
    user_file: Path

user_lock = asyncio.Lock()

@dataclass
class InMemoryUserStore(UserStore):
    config: InMemoryUserStoreConf

    def __post_init__(self):
        self.users = {}
        if not self.config.user_file.exists():
            self.config.user_file.touch()
        with open(self.config.user_file, "r+") as f:
            for r in f.readlines():
                user =User(**json.loads(r))
                self.users[user.email] = user
    

    async def save(self, user: User) -> User:
        if user.email in self.users:
            raise UserStoreErrors.AlreadyExists("User already exist")
        async with user_lock:
            self.users[user.email] = user
        async with aiofiles.open(self.config.user_file, mode='a') as handle:
            await handle.write(user.model_dump_json() + "\n")
        return user
        

    async def get(self, email: str) -> User:
        if email not in self.users:
            raise UserStoreErrors.NotFoundError("User not found")
        async with user_lock:
            user = self.users[email]
        return user
    
        
