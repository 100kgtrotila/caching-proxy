import argparse
from base64 import decode

import httpx
import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI, Request, Response
from contextlib import asynccontextmanager

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


