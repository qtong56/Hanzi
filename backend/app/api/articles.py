from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.article import Article
from app.schemas.article import (
    ArticleCreate,
    ArticleResponse,
    ArticleListResponse,
    ArticleListItem
)
from app.services.segmentation import segment_text, estimate_hsk_level, dominant_hsk_level, count_chinese_chars

router = APIRouter()

@router.get("/", response_model=ArticleListResponse)
def get_articles(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of items to return"),
    hsk_level: Optional[int] = Query(None, ge=1, le=7, description="Filter by HSK level"),
    db: Session = Depends(get_db)
):
    """
    Get list of articles
    
    - **skip**: Pagination offset
    - **limit**: Max items to return (max 100)
    - **hsk_level**: Optional filter by HSK level (1-6)
    """
    query = db.query(Article)

    # Apply HSK level filter if provided
    if hsk_level is not None:
        query = query.filter(Article.hsk_level == hsk_level)
    
    # Get total count
    total = query.count()

    # Get paginated results
    articles = query.order_by(Article.created_at.desc()).offset(skip).limit(limit).all()

    return {
        "articles": articles,
        "total": total,
        "limit": limit,
        "offset": skip
    }

@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a single article by id

    Returns a full article with segments for reading view
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    
    if not article:
        raise HTTPException(status_code=404, detail=f"Article {article_id} not found")
    
    return article

@router.post("/", response_model=ArticleResponse, status_code=201)
def create_article(
    article_data: ArticleCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new article
    
    Automatically:
    - Segments the text
    - Calculates word count
    - Estimates HSK level
    - Generates summary (first 100 chars)
    """
    # Segment the text
    segments = segment_text(article_data.text)

    # Calculate metadata
    word_count = count_chinese_chars(article_data.text)
    unique_char_count = len(set(article_data.text))
    counts = estimate_hsk_level(article_data.text)
    hsk_level = dominant_hsk_level(counts, count_chinese_chars(article_data.text))
    hsk_level_counts = {str(k): v for k, v in counts.items()}

    # Generate summary (first 100 characters)
    summary = article_data.summary
    if not summary:
        summary = article_data.text[:100]
        if len(article_data.text) > 100:
            summary += "..."

    # Create article
    article = Article(
        title = article_data.title,
        text = article_data.text,
        summary = summary,
        segments=segments,
        word_count = word_count,
        unique_char_count = unique_char_count,
        hsk_level = hsk_level,
        hsk_level_counts = hsk_level_counts,
    )

    db.add(article)
    db.commit()
    db.refresh(article)

    return article

@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    article_data: ArticleCreate,
    db: Session = Depends(get_db)
):
    """
    Update an existing article
    
    Recalculates all metadata and segments
    """
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail=f"Article {article_id} not found")
    
    # Resegment the text
    segments = segment_text(article_data.text)
    counts = estimate_hsk_level(article_data.text)

    # Update fields
    article.title = article_data.title
    article.text = article_data.text
    article.summary = article_data.summary
    article.segments = segments
    article.word_count = count_chinese_chars(article_data.text)
    article.unique_char_count = len(set(article_data.text))
    article.hsk_level = dominant_hsk_level(counts, count_chinese_chars(article_data.text))
    article.hsk_level_counts = {str(k): v for k, v in counts.items()}

    db.commit()
    db.refresh(article)

    return article

@router.delete("/{article_id}", status_code=204)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an article
    """
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail=f"Article {article_id} not found")
    
    db.delete(article)
    db.commit()
    
    return None