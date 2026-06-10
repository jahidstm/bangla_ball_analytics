from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from .config import get_settings

settings = get_settings()

# ── SQLAlchemy Async Engine ───────────────────────────────────────────────────
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,        # DEBUG=True হলে SQL query print হবে
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,         # Connection alive কিনা check করে
)

# ── Session Factory ───────────────────────────────────────────────────────────
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,     # commit এর পরেও object access করা যাবে
)

# ── Base Model ────────────────────────────────────────────────────────────────
Base = declarative_base()


# ── Dependency: FastAPI route এ inject করার জন্য ─────────────────────────────
async def get_db() -> AsyncSession:
    """
    FastAPI dependency injection এর জন্য।
    প্রতিটি request-এ নতুন DB session দেয়, request শেষে close করে।

    Usage:
        @router.get("/")
        async def my_route(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    App startup এ call হয়।
    সব SQLAlchemy models এর table তৈরি করে (যদি না থাকে)।
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
