from contextlib import asynccontextmanager

import httpx
import redis.asyncio as redis
from fastapi import FastAPI
from proxy import router as proxy_router

config = {
    "origin": "",
    "port": 8000,
    "redis_url": "redis://localhost:6379"
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(base_url=config["origin"])
    app.state.redis = redis.from_url(config["redis_url"], decode_responses=False)
    yield

    await app.state.http_client.aclose()
    await app.state.redis.close()

app = FastAPI(lifespan=lifespan)
app.include_router(proxy_router)

