from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.config import get_settings
from app.core.database import get_db
from app.models.schemas import HealthResponse, PinVerifyRequest, PinVerifyResponse

settings = get_settings()
router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    System health check endpoint।
    Database connection alive কিনা পরীক্ষা করে।
    """
    db_status = "disconnected"
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "error"

    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        database=db_status,
        mock_mode=settings.USE_MOCK_DATA,
    )


@router.post("/auth/verify", response_model=PinVerifyResponse, tags=["Auth"])
async def verify_pin(body: PinVerifyRequest):
    """
    Frontend login page থেকে PIN verify করার endpoint।
    PIN ঠিক হলে frontend cookie set করবে।
    """
    if body.pin == settings.APP_PIN:
        response = JSONResponse(
            content={"success": True, "message": "Authentication successful"},
        )
        # httpOnly cookie set করো যাতে middleware check করতে পারে
        response.set_cookie(
            key="app_pin",
            value=body.pin,
            httponly=True,
            samesite="lax",
            max_age=86400 * 7,   # 7 দিন
        )
        return response

    return JSONResponse(
        status_code=401,
        content={"success": False, "message": "ভুল PIN! আবার চেষ্টা করুন।"},
    )
