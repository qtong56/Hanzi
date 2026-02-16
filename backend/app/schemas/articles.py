from pydantic import BaseModel
from typing import List, Optional

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
    """For creating new articles"""
    pass

class ArticleResponse(ArticleBase):
    """For API responses"""
    id: int
    segments: Optional[List[SegmentSchema]] = None
    word_count: Optional[int] = None

    class Config:
        from_attributes = True # Allows SQLAlchemy modesl to convert

class ArticlesListResponse(BaseModel):
    """List of articles"""
    articles: List[ArticleResponse]
    total: int

class TranslationResponses(BaseModel):
    """Translation lookup result"""
    word: str
    found: bool
    simplified: Optional[str] = None
    traditional: Optional[str] = None
    pinyin: Optional[str] = None
    definitions: Optional[str] = None
    hsk_level: Optional[int] = None