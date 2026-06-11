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
    নতুন insight generation শুরু করো। LangGraph Agentic workflow ট্রিগার করবে।
    """
    from app.agents.graph import app_graph
    import asyncio
    from functools import partial

    logger.info("New insight requested", topic=body.topic)

    # ── Step 1: Run LangGraph FIRST in thread executor ─────────────────
    try:
        logger.info("Triggering LangGraph Workflow", topic=body.topic)
        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(
            None,
            partial(app_graph.invoke, {"topic": body.topic})
        )
        graph_succeeded = not final_state.get("error")
        if not graph_succeeded:
            logger.error("Graph returned error", error=final_state.get("error"))
        logger.info("LangGraph finished successfully")
    except Exception as e:
        logger.error("Workflow crashed inside run_in_executor", error=str(e))
        final_state = {"error": str(e)}
        graph_succeeded = False

    # ── Step 2: Now do ALL DB operations in async context ───────────────
    try:
        logger.info("Before db.add")
        status_val = "completed" if graph_succeeded else "failed"
        new_insight = Insight(
            topic=body.topic,
            status=status_val,
            analysis_report=final_state.get("analysis_result") if graph_succeeded else None,
        )
        db.add(new_insight)
        logger.info("Before db.flush")
        await db.flush()  # Get the ID
        logger.info("After db.flush")

        if graph_succeeded:
            posts_to_add = []
            for post_variant in final_state.get("bangla_posts", []):
                post_record = Post(
                    insight_id=new_insight.id,
                    style_type=post_variant.style,
                    content=post_variant.content,
                )
                posts_to_add.append(post_record)
            db.add_all(posts_to_add)

        logger.info("Before db.commit")
        await db.commit()

        logger.info("Before selectinload query")
        from sqlalchemy.orm import selectinload
        # Fetch the complete insight with posts eagerly loaded
        # This prevents Pydantic from triggering a synchronous lazy load (which causes MissingGreenlet)
        final_result = await db.execute(
            select(Insight)
            .options(selectinload(Insight.posts))
            .where(Insight.id == new_insight.id)
        )
        final_insight = final_result.scalar_one()
        
        logger.info("Generation complete and returning response")
        return final_insight
    except Exception as e:
        logger.error(f"DB operation crashed: {type(e).__name__}", error=str(e))
        raise


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
