import logging

import uvicorn
from fastapi import FastAPI

from auth_service.adapters.http.routers import login, users

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s  %(message)s",
    # handlers=[logging.StreamHandler()],
)

app = FastAPI(title="Auth Service")
app.include_router(users.router)
app.include_router(login.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
