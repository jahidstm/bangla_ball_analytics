from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from .config import get_settings
from .logger import logger

settings = get_settings()

# ── যে paths এ PIN চেক করা হবে না ────────────────────────────────────────────
PUBLIC_PATHS = {
    "/",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/api/v1/health",
    "/api/v1/auth/verify",
}


class PinAuthMiddleware(BaseHTTPMiddleware):
    """
    Simple PIN-based authentication middleware।
    প্রতিটি request-এ Header বা Cookie এ PIN আছে কিনা check করে।

    Frontend থেকে request করার সময়:
        Header: X-API-Pin: 1234
    অথবা Cookie: app_pin=1234
    """

    async def dispatch(self, request: Request, call_next):
        # Public paths skip করো
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        # PIN check করো
        pin_from_header = request.headers.get("X-API-Pin")
        pin_from_cookie = request.cookies.get("app_pin")
        provided_pin = pin_from_header or pin_from_cookie

        if provided_pin != settings.APP_PIN:
            logger.warning(
                "Unauthorized access attempt",
                path=request.url.path,
                ip=request.client.host if request.client else "unknown",
            )
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or missing PIN"},
            )

        return await call_next(request)
