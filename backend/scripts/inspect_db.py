"""
Quick database inspector — shows a summary of what's in the DB.

Usage:
    cd backend
    .venv/bin/python scripts/inspect_db.py            # summary
    .venv/bin/python scripts/inspect_db.py --full     # include HSK counts per article
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models.article import Article
from sqlalchemy import func


def inspect(full: bool = False):
    db = SessionLocal()
    try:
        total = db.query(Article).count()
        print(f"\n{'='*60}")
        print(f"  DATABASE: hanzi@localhost:5432")
        print(f"  Total articles: {total}")
        print(f"{'='*60}\n")

        # HSK level distribution
        dist = (
            db.query(Article.hsk_level, func.count(Article.id))
            .group_by(Article.hsk_level)
            .order_by(Article.hsk_level)
            .all()
        )
        print("HSK level distribution:")
        for level, count in dist:
            bar = "█" * count
            print(f"  HSK {level}  {bar}  ({count})")

        # Per-article listing
        print(f"\n{'─'*60}")
        print(f"  {'ID':>3}  {'Title':<16}  {'HSK':>3}  {'Chars':>5}  {'Category':<12}  HSK counts")
        print(f"{'─'*60}")

        articles = (
            db.query(Article)
            .order_by(Article.hsk_level, Article.id)
            .all()
        )
        for a in articles:
            counts = a.hsk_level_counts or {}
            counts_str = "  ".join(
                f"L{k}:{v}"
                for k, v in sorted(counts.items(), key=lambda x: int(x[0]))
                if v > 0
            )
            print(
                f"  {a.id:>3}  {a.title:<16}  HSK{a.hsk_level:>2}  "
                f"{(a.word_count or 0):>5}  {(a.category or ''):.<12}  {counts_str}"
            )

        if full:
            print(f"\n{'─'*60}")
            print("Full article summaries:\n")
            for a in articles:
                print(f"[{a.id}] {a.title}  (HSK {a.hsk_level}, {a.word_count} chars)")
                if a.summary:
                    print(f"    {a.summary[:80]}{'...' if len(a.summary or '') > 80 else ''}")
                print()

    finally:
        db.close()


if __name__ == "__main__":
    inspect(full="--full" in sys.argv)
