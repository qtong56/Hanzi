from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base

class Article(Base):
    """
    Stores Wikipedia articles
    """
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    text = Column(Text)
    summary = Column(Text)

    # Metadata
    category = Column(String(100))
    word_count = Column(Integer)
    unique_char_count = Column(Integer)

    # Difficulty
    hsk_level = Column(Integer)

    # Segmented text stored as JSON array
    segments = Column(JSONB)

    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class Dictionary(Base):
    """
    Chinese-English dictionary (from CC-CEDICT)
    """
    __tablename__ = "dictionary"
    id = Column(Integer, primary_key=True)
    simplified = Column(String(50), unique=True)
    traditional = Column(String(50))
    pinyin = Column(String(200))
    definitions = Column(JSONB)

    hsk_level = Column(Integer)
    frequency_rank = Column(Integer)
