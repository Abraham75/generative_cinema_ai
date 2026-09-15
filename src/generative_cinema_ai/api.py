"""Local-only FastAPI transport with bounded, redacted validation failures."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from .models import AnalysisRequest, AnalysisResult
from .service import AnalysisService
from .settings import Settings

settings = Settings.from_env()
app = FastAPI(
    title="Generative Cinema AI",
    version="0.1.0",
    docs_url="/docs" if settings.environment == "development" else None,
    redoc_url=None,
    openapi_url="/openapi.json" if settings.environment == "development" else None,
)
service = AnalysisService()


class BodySizeLimitMiddleware:
    """Reject oversized bodies before framework JSON/model validation."""

    def __init__(self, wrapped: ASGIApp, max_bytes: int) -> None:
        self.wrapped = wrapped
        self.max_bytes = max_bytes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.wrapped(scope, receive, send)
            return
        headers = dict(scope.get("headers", []))
        raw_length = headers.get(b"content-length")
        if raw_length and raw_length.isdigit() and int(raw_length) > self.max_bytes:
            await self._too_large(send)
            return
        consumed = 0

        async def bounded_receive() -> Message:
            nonlocal consumed
            message = await receive()
            if message["type"] == "http.request":
                consumed += len(message.get("body", b""))
                if consumed > self.max_bytes:
                    raise _BodyTooLarge
            return message

        try:
            await self.wrapped(scope, bounded_receive, send)
        except _BodyTooLarge:
            await self._too_large(send)

    @staticmethod
    async def _too_large(send: Send) -> None:
        body = b'{"type":"about:blank","title":"Request body too large","status":413}'
        await send(
            {
                "type": "http.response.start",
                "status": 413,
                "headers": [(b"content-type", b"application/problem+json"), (b"content-length", str(len(body)).encode())],
            }
        )
        await send({"type": "http.response.body", "body": body})


class _BodyTooLarge(Exception):
    pass


class LocalOnlyMiddleware:
    """Block non-loopback clients until explicitly enabled for controlled testing."""

    def __init__(self, wrapped: ASGIApp, allow_network: bool) -> None:
        self.wrapped = wrapped
        self.allow_network = allow_network

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        client = scope.get("client")
        host = client[0] if client else ""
        if scope["type"] == "http" and not self.allow_network and host not in {"127.0.0.1", "::1", "testclient"}:
            response = JSONResponse(status_code=403, content={"type": "about:blank", "title": "Local access only", "status": 403})
            await response(scope, receive, send)
            return
        await self.wrapped(scope, receive, send)


app.add_middleware(BodySizeLimitMiddleware, max_bytes=settings.max_body_bytes)
app.add_middleware(LocalOnlyMiddleware, allow_network=settings.allow_network_api)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    errors: list[dict[str, Any]] = []
    for item in exc.errors()[:20]:
        errors.append(
            {
                "location": [str(part) for part in item.get("loc", ())],
                "message": str(item.get("msg", "Invalid value"))[:240],
                "code": str(item.get("type", "validation_error"))[:120],
            }
        )
    return JSONResponse(
        status_code=422,
        content={"type": "about:blank", "title": "Request validation failed", "status": 422, "errors": errors},
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": app.version, "exposure": "local-development-only"}


@app.post("/v1/analysis", response_model=AnalysisResult)
def analyze(request: AnalysisRequest) -> AnalysisResult:
    """IDs are trace context only; authentication and tenant isolation are not implemented."""
    return service.analyze(request)
