import uvicorn
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI

from core.config import setting
from core.model import db_helper
from api.user_api import router as router_user

logging.basicConfig(
    level=logging.INFO,
    format=setting.logging.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # shutdown
    await db_helper.dispose()


app_main = FastAPI(lifespan=lifespan)
app_main.include_router(router=router_user)


@app_main.get("/")
async def get_hello():
    return {
        "message": "Hello World",
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app_main",
        host=setting.run.host,
        port=setting.run.port,
    )
