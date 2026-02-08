import redis
from anyio.functools import cache
from fastapi import Request, Response
from main import app


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def prodxy_handler(path: str, request: Request):
    full_path = str(request.url).replace(str(request.base_url),"")
    cache_key = f"{request.method}:{full_path}"

    if request.method == "GET":
        cached_content = await redis.client.get(cache_key)

        if cached_content:
            return Response(
                content=cached_content,
                status_code=200,
                headers={
                    "X-Cache": "HIT"
                }
            )
