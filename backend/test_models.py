from app.models.article import Article, Base
from app.database import engine, SessionLocal

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
        "Article Queries": test_query_articles()
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