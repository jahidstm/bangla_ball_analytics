from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """
    Application configuration — সব values .env ফাইল থেকে লোড হয়।
    """

    # ── App ──────────────────────────────────────────────────
    APP_NAME: str = "Bangla Ball Analytics"
    APP_VERSION: str = "1.0.0"
    APP_PIN: str = "1234"           # Simple PIN-based auth
    DEBUG: bool = False

    # ── Data Strategy ────────────────────────────────────────
    # True রাখলে soccerdata / real API বাদ দিয়ে mock JSON দেবে
    USE_MOCK_DATA: bool = True

    # ── Database (Supabase PostgreSQL) ───────────────────────
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    DATABASE_URL: str = ""          # postgresql+asyncpg://...

    # ── AI APIs ──────────────────────────────────────────────
    GROQ_API_KEY: str = ""          # Analyst Agent (Llama-3.3-70B)
    GOOGLE_API_KEY: str = ""        # Copywriter Agent (Gemini 1.5 Flash)

    # ── External Football Data ───────────────────────────────
    API_FOOTBALL_KEY: Optional[str] = None   # Phase 3+ তে লাগবে

    # ── Local Paths ──────────────────────────────────────────
    CHROMA_PATH: str = "./chroma_db"
    EXPORT_PATH: str = "./exports"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Singleton — একবার লোড হয়, সবখানে একই instance।"""
    return Settings()
