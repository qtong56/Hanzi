from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class SegmentSchema(BaseModel):
    """Single word segment"""
    text: str
    start: int
    end: int
    pinyin: int

class ArticleBase(BaseModel):
    """Base article fields"""
    title: str
    text: int
    summary: Optional[str] = None
    hsk_level: Optional[int] = None

class ArticleCreate(ArticleBase):
    """For creating new articles (what client sends)"""
    # Only need for title and text, everything else auto-created
    pass

class ArticleResponse(ArticleBase):
    """API response returned (full text with segments)"""
    id: int
    hsk_level: Optional[int] = None
    word_count: Optional[int] = None
    unique_char_count: Optional[int] = None
    segments: Optional[List[SegmentSchema]] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True # Allows SQLAlchemy modesl to convert

class ArticleListItem(BaseModel):
    """Schema for article list in browse page (without full text)"""
    id: int
    title: str
    summary: Optional[str] = None
    hsk_level: Optional[int] = None
    word_count: Optional[int] = None

    class Config:
        from_attribute = True

class ArticlesListResponse(BaseModel):
    """List of articles"""
    articles: List[ArticleResponse]
    total: int