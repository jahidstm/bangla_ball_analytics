from app.core.database import Base
from sqlalchemy import (
    Column, String, Text, Boolean, Integer,
    TIMESTAMP, ARRAY, JSON, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid


class Insight(Base):
    """
    একটি insight generation request।
    user একটি topic দেয় → সিস্টেম analyze করে → এখানে সেভ হয়।
    """
    __tablename__ = "insights"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic = Column(Text, nullable=False)

    # Status flow: pending → processing → done | failed
    status = Column(String(20), default="pending", nullable=False)

    # Analyst Agent-এর output (structured JSON)
    analysis_report = Column(JSON, nullable=True)

    # Plotly chart config (JSON) — Recharts এ render করবে
    chart_data = Column(JSON, nullable=True)

    # Kaleido-exported PNG path (Facebook download-এর জন্য)
    chart_image_path = Column(Text, nullable=True)

    # যদি কোনো error হয়
    error_message = Column(Text, nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship: একটি insight → অনেকগুলো post
    posts = relationship("Post", back_populates="insight", cascade="all, delete-orphan")


class Post(Base):
    """
    Copywriter Agent-এর তৈরি করা বাংলা Facebook পোস্ট।
    প্রতিটি insight এর জন্য ৩টি variant পোস্ট থাকে।
    """
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    insight_id = Column(UUID(as_uuid=True), ForeignKey("insights.id", ondelete="CASCADE"))

    # Post content
    content = Column(Text, nullable=False)

    # Style: emotional | analytical | punchy
    style_type = Column(String(50), nullable=True)

    # Hashtags list: ["#Messi", "#Football", "#বাংলাদেশ"]
    hashtags = Column(ARRAY(Text), nullable=True)

    # User actions
    is_saved = Column(Boolean, default=False)
    is_edited = Column(Boolean, default=False)
    edited_content = Column(Text, nullable=True)   # user edited version

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    insight = relationship("Insight", back_populates="posts")


class PlayerCache(Base):
    """
    Player stats cache — বারবার API call না করার জন্য।
    24 ঘণ্টা পর re-fetch হবে।
    """
    __tablename__ = "players_cache"

    id = Column(String(50), primary_key=True)   # API Football player ID
    name = Column(Text, nullable=False)
    team = Column(Text, nullable=True)
    nationality = Column(Text, nullable=True)
    position = Column(Text, nullable=True)
    age = Column(Integer, nullable=True)

    # Full stats JSON (goals, assists, xG, xA, etc.)
    stats = Column(JSON, nullable=True)

    last_updated = Column(TIMESTAMP(timezone=True), server_default=func.now())


class StylePost(Base):
    """
    RAG সিস্টেমের জন্য style reference পোস্ট।
    Vector (embedding) ChromaDB-তে থাকে, metadata এখানে।
    """
    __tablename__ = "style_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    page_name = Column(Text, nullable=True)        # যেমন: Pavilion, Muktobak
    style_type = Column(Text, nullable=True)        # emotional | analytical | punchy
    chroma_doc_id = Column(Text, nullable=True)     # ChromaDB document ID

    added_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
