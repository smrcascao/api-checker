
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

app = FastAPI()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="\n[%(asctime)s] [%(levelname)s] %(message)s\n",
    datefmt="%Y-%m-%d %H:%M:%S",
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    client_ip = request.client.host
    method = request.method
    path = request.url.path
    query = str(request.url.query)
    headers = dict(request.headers)
    http_version = request.scope.get("http_version", "unknown")
    body = await request.body()

    log_data = {
        "client_ip": client_ip,
        "http_version": http_version,
        "method": method,
        "path": path,
        "query_params": query,
        "headers": headers,
        "body": body.decode("utf-8", errors="ignore") if body else None
    }

    logging.info(f"Incoming Request:\n{log_data}\n{'-'*60}")

    response = await call_next(request)
    return response

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def catch_all(request: Request, path: str):
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    cookies = request.cookies
    body = await request.body()
    client_ip = request.client.host
    http_version = request.scope.get("http_version", "unknown")

    return JSONResponse({
        "path": f"/{path}",
        "method": request.method,
        "headers": headers,
        "query_params": query_params,
        "cookies": cookies,
        "body": body.decode("utf-8", errors="ignore") if body else None,
        "client_ip": client_ip,
        "http_version": http_version
    })

@app.get("/errorcode/{code:int}")
async def return_error_code(code: int, request: Request):
    if 100 <= code <= 599:
        client_ip = request.client.host
        http_version = request.scope.get("http_version", "unknown")
        headers = dict(request.headers)
        query_params = dict(request.query_params)
        cookies = request.cookies
        body = await request.body()

        log_data = {
            "status_code": code,
            "client_ip": client_ip,
            "http_version": http_version,
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.url.query),
            "headers": headers,
            "body": body.decode("utf-8", errors="ignore") if body else None
        }

        logging.info(f"Generated Error Code Response:\n{log_data}\n{'-'*60}")

        return JSONResponse(
            status_code=code,
            content={
                "status_code": code,
                "message": f"Generated error with status {code}",
                "path": str(request.url.path),
                "method": request.method,
                "headers": headers,
                "query_params": query_params,
                "cookies": cookies,
                "body": body.decode("utf-8", errors="ignore") if body else None,
                "client_ip": client_ip,
                "http_version": http_version
            }
        )

    return JSONResponse(status_code=400, content={"error": "Invalid status code"})
