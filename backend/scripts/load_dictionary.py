"""
Load CC-CEDICT into the dictionary table.

Run from the backend/ directory:
    python scripts/load_dictionary.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.database import SessionLocal, Base, engine
from app.models.article import Dictionary
from app.services.translation import parse_cedict_file

BATCH_SIZE = 1000


def load_dictionary():
    print("=" * 60)
    print("LOADING CC-CEDICT DICTIONARY")
    print("=" * 60)

    # Create tables if they don't exist
    Base.metadata.create_all(engine)

    db = SessionLocal()

    try:
        existing = db.query(Dictionary).count()
        if existing > 0:
            print(f"Dictionary already has {existing} entries. Skipping.")
            return True

        print("Parsing CC-CEDICT file...")
        batch = []
        loaded = 0
        skipped = 0
        duplicates = 0

        for simplified, traditional, pinyin, definitions in parse_cedict_file():
            # Skip entries with no Chinese characters (numbers, punctuation, etc.)
            if not any('\u4e00' <= c <= '\u9fff' for c in simplified):
                skipped += 1
                continue

            batch.append({
                "simplified": simplified,
                "traditional": traditional,
                "pinyin": pinyin,
                "definitions": definitions,
            })

            if len(batch) >= BATCH_SIZE:
                stmt = pg_insert(Dictionary).values(batch)
                stmt = stmt.on_conflict_do_nothing(index_elements=["simplified"])
                result = db.execute(stmt)
                db.commit()
                inserted = result.rowcount
                duplicates += len(batch) - inserted
                loaded += inserted
                batch = []
                print(f"  Loaded {loaded} entries...", end="\r")

        # Final batch
        if batch:
            stmt = pg_insert(Dictionary).values(batch)
            stmt = stmt.on_conflict_do_nothing(index_elements=["simplified"])
            result = db.execute(stmt)
            db.commit()
            loaded += result.rowcount

        print(f"\nLoaded {loaded} dictionary entries")
        print(f"Skipped {skipped} non-Chinese entries, {duplicates} duplicates ignored")
        print(f"Total in database: {db.query(Dictionary).count()}")
        return True

    except Exception as e:
        print(f"\nError: {e}")
        db.rollback()
        return False

    finally:
        db.close()


if __name__ == "__main__":
    success = load_dictionary()
    if success:
        print("\n" + "=" * 60)
        print("DICTIONARY LOADED SUCCESSFULLY")
        print("=" * 60)
        print("\nTest a lookup:")
        print("  curl http://localhost:8000/api/dictionary/你好")
    else:
        print("\nLOADING FAILED")
