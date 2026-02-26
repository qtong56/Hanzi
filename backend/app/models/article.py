from sqlalchemy import Integer, String, Text, TIMESTAMP, func, Index
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.database import Base

class Article(Base):
    """
    Stores Wikipedia articles
    """
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Metadata
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    word_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    unique_char_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Difficulty
    hsk_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    hsk_level_counts: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Segmented text stored as JSON array
    segments: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(JSONB, nullable=True)

    # Timestamps
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class Dictionary(Base):
    """
    Chinese-English dictionary (CC-CEDICT)
    """
    __tablename__ = "dictionary"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Chinese characters
    simplified: Mapped[str] = mapped_column(String(50), nullable=False, index=True, unique=True)
    traditional: Mapped[str] = mapped_column(String(50))
    
    # Pronunciation
    pinyin: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Definitions (stored as array)
    definitions: Mapped[List[str]] = mapped_column(ARRAY(Text), nullable=False)
    
    # Optional metadata
    hsk_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    frequency_rank: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    def __repr__(self):
        return f"<Dictionary {self.simplified} ({self.pinyin})>"


# Create index for faster lookups
Index('idx_dictionary_simplified', Dictionary.simplified)