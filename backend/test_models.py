from app.models.article import Article, Base
from app.database import engine, SessionLocal
from app.services.segmentation import segment_text, estimate_hsk_level, dominant_hsk_level

def test_create_article_with_segments():
    """Test creating article with auto-segmentation"""
    print("\n=== Integration Test: Article + Segmentation ===")
    
    Base.metadata.create_all(engine)
    db = SessionLocal()
    
    try:
        # Create article text
        text = "中国是一个历史悠久的国家。中国有很多人口。"
        
        # Segment it
        segments = segment_text(text)
        print(f"\nText: {text}")
        print(f"Segments: {len(segments)}")
        
        # Calculate metadata
        word_count = len(segments)
        unique_chars = len(set(text))
        counts = estimate_hsk_level(text)
        hsk_level = dominant_hsk_level(counts, word_count)
        hsk_level_counts = {str(k): v for k, v in counts.items()}

        # Create article
        article = Article(
            title="中国",
            text=text,
            segments=segments,  # Store as JSONB
            word_count=word_count,
            unique_char_count=unique_chars,
            hsk_level=hsk_level,
            hsk_level_counts=hsk_level_counts,
        )

        db.add(article)
        db.commit()
        db.refresh(article)

        print(f"\n✓ Created article with ID: {article.id}")
        print(f"  Word count: {article.word_count}")
        print(f"  Unique chars: {article.unique_char_count}")
        print(f"  HSK level (80% coverage): {article.hsk_level}")
        print(f"  HSK counts: {article.hsk_level_counts}")
        stored_segs = article.segments or []
        print(f"  Segments stored: {len(stored_segs)}")

        # Verify we can query and retrieve segments
        retrieved = db.query(Article).filter(Article.id == article.id).first()
        assert retrieved is not None and retrieved.segments is not None, "Segments should be stored"
        assert len(retrieved.segments) == len(segments), "Segment count should match"

        print(f"\n✓ Segments retrieved correctly from database")
        print(f"\nFirst 3 segments:")
        for seg in retrieved.segments[:3]:
            print(f"  {seg['text']:8} | {seg['pinyin']}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Integration test failed: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def test_segmentation():
    """Test text segmentation"""
    print("\n=== Testing Segmentation Service ===")
    
    # Test 1: Basic segmentation
    text1 = "我喜欢学习中文"
    segments1 = segment_text(text1)
    
    print(f"\nTest 1: Basic")
    print(f"  Text: {text1}")
    print(f"  Segments: {len(segments1)}")
    assert len(segments1) > 0, "Should have segments"
    
    # Verify reconstruction
    reconstructed = ''.join([s['text'] for s in segments1])
    assert reconstructed == text1, f"Reconstruction failed: {reconstructed} != {text1}"
    print(f"  ✓ Reconstruction matches")
    
    # Test 2: With punctuation
    text2 = "今天天气很好。"
    segments2 = segment_text(text2)
    
    print(f"\nTest 2: With punctuation")
    print(f"  Text: {text2}")
    print(f"  Segments: {len(segments2)}")
    
    # Test 3: Empty text
    text3 = ""
    segments3 = segment_text(text3)
    
    print(f"\nTest 3: Empty text")
    assert len(segments3) == 0, "Empty text should return empty list"
    print(f"  ✓ Returns empty list")
    
    # Test 4: HSK level estimation
    print(f"\nTest 4: HSK level estimation")
    texts = [
        ("我爱你", 1),  # Very short, simple
        ("中国是一个历史悠久的国家。中国有很多人口。" * 5, 2),  # More unique chars
    ]
    
    for text, _ in texts:
        segs = segment_text(text)
        counts = estimate_hsk_level(text)
        level = dominant_hsk_level(counts, len(segs))
        print(f"  '{text[:20]}...' → counts={counts}, 80%-coverage HSK {level}")
    
    print(f"\n✓ All segmentation tests passed")
    return True


def test_db_connection():
    """Test database connection"""
    print("\n=== Testing Database Connection ===")
    try:
        connection = engine.connect()
        print("Successfully connected to PostgreSQL!")
        connection.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

def test_create_tables():
    """Test table creation"""
    print("\n=== Testing Table Creation ===")
    try:
        Base.metadata.create_all(engine)
        print("Tables created successfully!")
        
        # Verify table exists
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tables in database: {tables}")

        if 'articles' in tables:
            print("'articles' table exists!")

            # Show columns
            columns = inspector.get_columns('articles')
            print("\nColumns:")
            for col in columns:
                print(f" - {col['name']}: {col['type']}")
            return True
        else:
            print("'articles' table not found!")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_create_article():
    """Test article creation"""
    print("\n=== Testing Article Creation ===")
    Base.metadata.create_all(engine)

    db = SessionLocal()
    try:
        # Create an article
        article = Article(
            title="测试文章",
            text="这是一个测试。",
            hsk_level=1,
            word_count=5
        )
        db.add(article)
        db.commit()
        db.refresh(article)

        print(f"Created article with ID: {article.id}")
        print(f"Title: {article.title}")
        print(f"Text: {article.text}")
        return True
    except Exception as e:
        print(f"Insert failed: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
def test_query_articles():
    """Test querying articles"""
    print("\n=== Testing Article Queries ===")
    db = SessionLocal()

    print("Testing query...")
    try:
        # Query all articles
        articles = db.query(Article).all()
        print(f"Found {len(articles)} articles")

        if len(articles) > 0:
            for article in articles:
                print(f"\nID: {article.id}")
                print(f"Title: {article.title}")
                print(f"Text: {article.text}")
                print(f"HSK Level: {article.hsk_level}")
        else:
            print("No articles in database. Run test_create_article() first.")
            return False
        
        # Test filtering
        hsk1_articles = db.query(Article).filter(Article.hsk_level == 1).all()
        print(f"\n Found {len(hsk1_articles)} HSK 1 articles")
        return True
    except Exception as e:
        print(f"Query failed: {e}")
        return False
    finally:
        db.close()

def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "="*50)
    print("RUNNING ALL TESTS")
    print("="*50)
    
    results = {
        "Database Connection": test_db_connection(),
        "Table Creation": test_create_tables(),
        "Article Creation": test_create_article(),
        "Article Queries": test_query_articles(),
        "Segmentation": test_segmentation()
    }
    
    print("\n" + "="*50)
    print("TEST RESULTS SUMMARY")
    print("="*50)
    
    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nPassed: {passed}/{total}")
    
    return all(results.values())

if __name__ == "__main__":
    # test_db_connection()
    # test_create_tables()
    # test_create_article()
    # test_query_articles()

    # Run all tests
    run_all_tests()