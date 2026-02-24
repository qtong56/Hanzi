from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import articles, dictionary

Base.metadata.create_all(engine)

app = FastAPI(
    title="Hanzi API",
    description="Chinese reading practice API",
    version="1.0.0"
)

app.include_router(articles.router, prefix="/api/articles")
app.include_router(dictionary.router, prefix="/api/dictionary")

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

@app.get("/health")
def health():
    return {"status": "healthy"}