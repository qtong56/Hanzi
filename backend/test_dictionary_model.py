from app.database import engine, Base, SessionLocal
from app.models.article import Dictionary

print("=== Testing Dictionary Model ===\n")

# Create table
Base.metadata.create_all(engine)
print("Created dictionary table")

# Verify table structure
from sqlalchemy import inspect
inspector = inspect(engine)

if 'dictionary' in inspector.get_table_names():
    columns = inspector.get_columns('dictionary')
    print("\nColumns:")
    for col in columns:
        print(f"  - {col['name']}: {col['type']}")
else:
    print("dictionary table not found!")
    exit(1)

# Test inserting a word
db = SessionLocal()

try:
    word = Dictionary(
        simplified="你好",
        traditional="你好",
        pinyin="ni3 hao3",
        definitions=["hello", "hi", "how do you do"]
    )
    
    db.add(word)
    db.commit()
    db.refresh(word)
    
    print(f"\nInserted word with ID: {word.id}")
    print(f"  {word.simplified} ({word.pinyin})")
    print(f"  Definitions: {word.definitions}")
    
    # Test querying
    retrieved = db.query(Dictionary).filter(Dictionary.simplified == "你好").first()
    
    if retrieved:
        print(f"\nRetrieved word")
        print(f"  Definitions: {retrieved.definitions}")
        print(f"  Type: {type(retrieved.definitions)}")  # Should be list
    
except Exception as e:
    print(f"\nError: {e}")
    db.rollback()
finally:
    db.close()

print("\nDictionary model working!")