from fastapi import FastAPI
import time
from contextlib import asynccontextmanager

from src.settings import Settings
from src.logger import logger
from src.orders.router import router as orders_router
from src.users.router import router as users_router


app = FastAPI()

SETTINGS = Settings()

app.include_router(orders_router)
app.include_router(users_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Startup")
    yield
    logger.info("Shutting Down, Closing DB conn")


@app.get("/health")
async def health_check():
    return {"time": time.time(), "environment": SETTINGS.env}
