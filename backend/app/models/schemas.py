from pydantic import BaseModel, Field
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
# AUTH
# ═══════════════════════════════════════════════════════════════

class PinVerifyRequest(BaseModel):
    pin: str = Field(..., min_length=1, max_length=20)

class PinVerifyResponse(BaseModel):
    success: bool
    message: str


# ═══════════════════════════════════════════════════════════════
# INSIGHT
# ═══════════════════════════════════════════════════════════════

class InsightGenerateRequest(BaseModel):
    """User যখন নতুন insight generate করতে চায়"""
    topic: str = Field(..., min_length=3, max_length=500, example="মেসির বর্তমান ফর্ম ২০২৫")

class InsightResponse(BaseModel):
    """Insight-এর full response"""
    id: UUID
    topic: str
    status: str
    analysis_report: Optional[dict] = None
    chart_data: Optional[dict] = None
    chart_image_path: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    posts: Optional[List["PostResponse"]] = []

    class Config:
        from_attributes = True

class InsightListResponse(BaseModel):
    """Insight list এর জন্য (history page)"""
    id: UUID
    topic: str
    status: str
    created_at: datetime
    post_count: int = 0

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════════════
# POST
# ═══════════════════════════════════════════════════════════════

class PostResponse(BaseModel):
    """Generated Facebook post"""
    id: UUID
    insight_id: UUID
    content: str
    style_type: Optional[str] = None
    hashtags: Optional[List[str]] = []
    is_saved: bool
    is_edited: bool
    edited_content: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class PostUpdateRequest(BaseModel):
    """Post edit করার জন্য"""
    edited_content: str = Field(..., min_length=10)

class PostSaveToggleResponse(BaseModel):
    id: UUID
    is_saved: bool
    message: str


# ═══════════════════════════════════════════════════════════════
# SEARCH / PLAYER
# ═══════════════════════════════════════════════════════════════

class PlayerSearchResult(BaseModel):
    id: str
    name: str
    team: Optional[str] = None
    position: Optional[str] = None
    nationality: Optional[str] = None

class PlayerStatsResponse(BaseModel):
    id: str
    name: str
    team: Optional[str] = None
    position: Optional[str] = None
    nationality: Optional[str] = None
    age: Optional[int] = None
    stats: Optional[dict] = None


# ═══════════════════════════════════════════════════════════════
# RAG / STYLE POST
# ═══════════════════════════════════════════════════════════════

class StylePostCreateRequest(BaseModel):
    """RAG-এ নতুন style post যোগ করা"""
    content: str = Field(..., min_length=50, max_length=5000)
    page_name: str = Field(..., example="Pavilion")
    style_type: str = Field(..., example="emotional")

class StylePostResponse(BaseModel):
    id: UUID
    content: str
    page_name: Optional[str] = None
    style_type: Optional[str] = None
    added_at: datetime

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════════════
# GENERIC
# ═══════════════════════════════════════════════════════════════

class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    mock_mode: bool

class ErrorResponse(BaseModel):
    detail: str
    code: Optional[str] = None


# Forward reference update
InsightResponse.model_rebuild()
