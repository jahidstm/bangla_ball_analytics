from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.models.db_models import Insight, Post
from app.models.schemas import (
    InsightGenerateRequest,
    InsightResponse,
    InsightListResponse,
)
from app.core.logger import logger
from app.core.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/insights", tags=["Insights"])


@router.post("/generate", response_model=InsightResponse, status_code=status.HTTP_201_CREATED)
async def generate_insight(
    body: InsightGenerateRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    নতুন insight generation শুরু করো।

    Phase 1: DB তে record তৈরি করে 'pending' status দেয়।
    Phase 3: LangGraph agent workflow trigger করবে।
    """
    logger.info("New insight requested", topic=body.topic)

    # DB তে insight record তৈরি করো
    new_insight = Insight(
        topic=body.topic,
        status="pending",
    )
    db.add(new_insight)
    await db.flush()   # ID generate করতে flush করো

    logger.info("Insight record created", insight_id=str(new_insight.id))

    # Phase 3 এ এখানে LangGraph workflow trigger হবে
    # এখন শুধু "pending" status দিয়ে return করছি
    await db.refresh(new_insight)
    return new_insight


@router.get("/", response_model=List[InsightListResponse])
async def list_insights(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    সব insights এর list — History page এর জন্য।
    সর্বশেষটা আগে আসবে।
    """
    # Post count subquery
    post_count_sq = (
        select(Post.insight_id, func.count(Post.id).label("post_count"))
        .group_by(Post.insight_id)
        .subquery()
    )

    result = await db.execute(
        select(
            Insight.id,
            Insight.topic,
            Insight.status,
            Insight.created_at,
            func.coalesce(post_count_sq.c.post_count, 0).label("post_count"),
        )
        .outerjoin(post_count_sq, Insight.id == post_count_sq.c.insight_id)
        .order_by(desc(Insight.created_at))
        .offset(skip)
        .limit(limit)
    )
    rows = result.all()

    return [
        InsightListResponse(
            id=row.id,
            topic=row.topic,
            status=row.status,
            created_at=row.created_at,
            post_count=row.post_count,
        )
        for row in rows
    ]


@router.get("/{insight_id}", response_model=InsightResponse)
async def get_insight(
    insight_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """নির্দিষ্ট একটি insight এর full detail (posts সহ)।"""
    result = await db.execute(
        select(Insight).where(Insight.id == insight_id)
    )
    insight = result.scalar_one_or_none()

    if not insight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Insight {insight_id} পাওয়া যায়নি।",
        )

    # Posts load করো
    posts_result = await db.execute(
        select(Post).where(Post.insight_id == insight_id)
    )
    insight.posts = posts_result.scalars().all()

    return insight


@router.delete("/{insight_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_insight(
    insight_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Insight এবং তার সব posts মুছে দাও।"""
    result = await db.execute(
        select(Insight).where(Insight.id == insight_id)
    )
    insight = result.scalar_one_or_none()

    if not insight:
        raise HTTPException(status_code=404, detail="Insight পাওয়া যায়নি।")

    await db.delete(insight)
    logger.info("Insight deleted", insight_id=str(insight_id))
