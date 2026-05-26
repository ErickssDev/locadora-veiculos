from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.middleware import SlowAPIMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api.v1 import api_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="Locadora Guilherme API",
        version="1.0.0",
        description="Backend do MVP de locação de veículos.",
    )

    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter

    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"success": False, "detail": str(exc), "code": "invalid_request"},
        )

    @app.exception_handler(PermissionError)
    async def permission_error_handler(request: Request, exc: PermissionError) -> JSONResponse:
        return JSONResponse(
            status_code=403,
            content={"success": False, "detail": str(exc), "code": "forbidden"},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"success": False, "detail": exc.errors(), "code": "validation_error"},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "detail": exc.detail, "code": "http_error"},
        )

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
        return JSONResponse(
            status_code=429,
            content={"success": False, "detail": "Too Many Requests", "code": "too_many_requests"},
        )

    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
