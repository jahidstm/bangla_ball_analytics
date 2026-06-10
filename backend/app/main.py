"""
Bangla Ball Analytics — FastAPI Application Entry Point
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import init_db
from app.core.logger import setup_logging, logger
from app.core.middleware import PinAuthMiddleware
from app.api.v1.router import api_router

settings = get_settings()


# ── Lifespan: startup ও shutdown event ────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """App শুরু হওয়ার সময় DB initialize করে।"""
    setup_logging()
    logger.info(
        "Starting Bangla Ball Analytics API",
        version=settings.APP_VERSION,
        mock_mode=settings.USE_MOCK_DATA,
    )
    await init_db()
    logger.info("Database initialized successfully")
    yield
    logger.info("Shutting down API")


# ── FastAPI App ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="⚽ Bangla Ball Analytics API",
    description="""
    ফুটবল ইনসাইটস এবং বাংলা ফেসবুক পোস্ট জেনারেশন সিস্টেম।

    ## Features
    - 🤖 AI-powered football analysis (Groq Llama-3 + Gemini Flash)
    - 📝 Bangla Facebook post generation (3 variants per insight)
    - 📊 Player & team statistics
    - 🔍 Player search and comparison
    - 📥 Chart PNG export for Facebook
    """,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ── CORS — Next.js frontend allow করো ────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Next.js dev server
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── PIN Auth Middleware ────────────────────────────────────────────────────────
app.add_middleware(PinAuthMiddleware)


# ── API Routes ─────────────────────────────────────────────────────────────────
app.include_router(api_router, prefix="/api/v1")


# ── Root endpoint ─────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "⚽ Bangla Ball Analytics API চলছে!",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "mock_mode": settings.USE_MOCK_DATA,
    }
