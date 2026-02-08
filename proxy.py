import httpx
import redis.asyncio as redis
from fastapi import Request, Response, APIRouter

router = APIRouter()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_handler(path: str, request: Request):
    http_client: httpx.AsyncClient = request.app.state.http_client
    redis_client: redis.Redis = request.app.state.redis

    full_path = str(request.url).replace(str(request.base_url), "")
    cache_key = f"{request.method}:{full_path}"

    if request.method == "GET":
        cached_content = await redis_client.get(cache_key)

        if cached_content:
            return Response(
                content=cached_content,
                status_code=200,
                headers={"X-Cache": "HIT"}
            )

    req_headers = dict(request.headers)
    req_headers.pop("host", None)

    try:
        upstream_response = await http_client.request(
            method=request.method,
            url=full_path,
            headers=req_headers,
            content=await request.body()
        )
    except httpx.ConnectError:
        return Response("Failed to connect", status_code=502)

    response_content = upstream_response.content

    if request.method == "GET" and upstream_response.status_code == 200:
        await redis_client.setex(name=cache_key, time=300, value=response_content)

    res_headers = dict(upstream_response.headers)
    res_headers["X-Cache"] = "MISS"
    res_headers.pop("content-encoding", None)
    res_headers.pop("content-length", None)

    return Response(
        content=response_content,
        status_code=upstream_response.status_code,
        headers=res_headers
    )