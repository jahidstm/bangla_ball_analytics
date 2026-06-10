from fastapi import APIRouter

from .health import router as health_router
from .insights import router as insights_router
from .posts import router as posts_router
from .search import router as search_router

# মূল API router — সব sub-router এখানে যোগ হয়
api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(insights_router)
api_router.include_router(posts_router)
api_router.include_router(search_router)
