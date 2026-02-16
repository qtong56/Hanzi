from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, get_db
from app.models.article import Article

Base.metadata.create_all(engine)

app = FastAPI(
    title="Hanzi API",
    description="Chinese reading practice API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"message": "Hanzi API - Working!"}

@app.get("/api/articles")
def get_articles(db: Session = Depends(get_db)):
    """Get all articles"""
    articles = db.query(Article).all()

    return {
        "articles": [
            {
                "id": a.id,
                "title": a.title,
                "text": a.text,
                "hsk_level": a.hsk_level,
            } for a in articles
        ],
        "total": len(articles)
    }

@app.get("/api/articles/{article_id}")
def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get single article by ID"""
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return {
        "id": article.id,
        "title": article.title,
        "text": article.text,
        "hsk_level": article.hsk_level,
        "word_count": article.word_count
    }

@app.get("/health")
def health():
    return {"status": "healthy"}