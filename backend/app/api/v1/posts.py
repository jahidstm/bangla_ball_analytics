from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.models.db_models import Post
from app.models.schemas import PostResponse, PostUpdateRequest, PostSaveToggleResponse

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/saved", response_model=List[PostResponse])
async def get_saved_posts(db: AsyncSession = Depends(get_db)):
    """সব saved posts — Library page এর জন্য।"""
    result = await db.execute(
        select(Post).where(Post.is_saved == True).order_by(Post.created_at.desc())
    )
    return result.scalars().all()


@router.put("/{post_id}", response_model=PostResponse)
async def edit_post(
    post_id: UUID,
    body: PostUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    """Post edit করো — user নিজের মতো modify করতে পারবে।"""
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post পাওয়া যায়নি।")

    post.edited_content = body.edited_content
    post.is_edited = True
    return post


@router.post("/{post_id}/save", response_model=PostSaveToggleResponse)
async def toggle_save_post(
    post_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Post save/unsave toggle করো।"""
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post পাওয়া যায়নি।")

    post.is_saved = not post.is_saved
    action = "সেভ করা হয়েছে" if post.is_saved else "আনসেভ করা হয়েছে"

    return PostSaveToggleResponse(
        id=post.id,
        is_saved=post.is_saved,
        message=f"পোস্ট {action}।",
    )
