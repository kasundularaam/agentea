import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from injection import DevContainer
from src.routers import model_router, root_router, status_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

load_dotenv()

container = DevContainer()

container.init_resources()
app = FastAPI()
app.include_router(model_router.router)
app.include_router(status_router.router)
app.include_router(root_router.router)

allowed_hosts = os.getenv("ALLOWED_HOSTS", "*").split(",")

app.add_middleware(CORSMiddleware, allow_origins=allowed_hosts, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])

if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True, timeout_keep_alive=60)
