import argparse
from contextlib import asynccontextmanager

import httpx
import redis.asyncio as redis
import uvicorn
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


def main():
    parser = argparse.ArgumentParser(description="Redis Caching Proxy")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--origin", type=str)
    parser.add_argument("--clear-cache", action="store_true")

    args = parser.parse_args()

    if args.clear_cache:
        import redis as sync_redis
        r = sync_redis.from_url(config["redis_url"])
        r.flushdb()
        print("Cache cleared")
        return

    if not args.origin:
        print("Error: --origin is required unless clearing cache")
        return

    config["port"] = args.port
    config["origin"] = args.origin

    print(f"🚀 Redis Proxy running on port {args.port} -> forwarding to {args.origin}")

    uvicorn.run(app, host="127.0.0.1", port=args.port)

if __name__ == "__main__":
    main()