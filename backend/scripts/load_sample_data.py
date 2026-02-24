"""
Create sample Wikipedia articles for testing.

This simulates what we'd get from the real Wikipedia dump.
"""
import sys
sys.path.append('..')

from app.database import SessionLocal, Base, engine
from app.models.article import Article
from app.services.segmentation import segment_text, estimate_hsk_level

# Sample Wikipedia articles
SAMPLE_ARTICLES = [
    {
        "title": "中国",
        "text": """中国，全称中华人民共和国，是位于东亚的国家。中国是世界上人口最多的国家，拥有超过14亿人口。

中国有着悠久的历史和丰富的文化传统。中国的首都是北京，最大的城市是上海。

中国的地理环境非常多样，包括高山、平原、沙漠和海岸线。长江是中国最长的河流，黄河被称为中华民族的母亲河。

中国是世界第二大经济体，在科技、制造业和贸易方面都有重要地位。""",
        "category": "Geography"
    },
    {
        "title": "北京",
        "text": """北京是中华人民共和国的首都，也是中国的政治、文化和教育中心。北京有着3000多年的建城史。

北京有许多著名的历史遗迹，包括故宫、长城、天坛和颐和园。这些景点每年吸引数百万游客。

现代北京是一个国际化大都市，拥有发达的交通系统，包括地铁、高速公路和国际机场。

北京也是中国的教育中心，拥有清华大学和北京大学等世界知名学府。""",
        "category": "Cities"
    },
    {
        "title": "长城",
        "text": """长城是中国古代的军事防御工程，也是世界上最长的人造建筑。长城的历史可以追溯到公元前7世纪。

长城主要分布在中国北方，东起河北省，西至甘肃省。最著名的长城段落是明长城。

长城不仅是中国的象征，也被联合国教科文组织列为世界文化遗产。每年有数百万游客到长城参观。

关于长城有一个著名的说法："不到长城非好汉。"这句话表达了人们对长城的敬仰。""",
        "category": "History"
    },
    {
        "title": "春节",
        "text": """春节是中国最重要的传统节日，也被称为中国新年。春节通常在一月底或二月初，根据农历确定日期。

春节期间，家人团聚，共享美食。传统的春节活动包括贴春联、放鞭炮、发红包。

在春节前，人们会进行大扫除，准备年货。除夕夜，全家人一起吃团圆饭。

春节的庆祝活动通常持续15天，以元宵节结束。现在，春节不仅在中国庆祝，在世界各地的华人社区也很流行。""",
        "category": "Culture"
    },
    {
        "title": "熊猫",
        "text": """大熊猫是中国的国宝，也是世界上最可爱的动物之一。熊猫主要生活在中国四川省的山区。

熊猫以竹子为主要食物，每天要吃12-16个小时。成年熊猫的体重可达100-150公斤。

熊猫的数量很少，被列为濒危物种。中国政府采取了许多保护措施，建立了熊猫保护区。

熊猫也是中国的外交使者。中国经常将熊猫赠送或租借给其他国家，促进国际友谊。""",
        "category": "Animals"
    },
    {
        "title": "中文",
        "text": """中文是世界上使用人数最多的语言，有超过10亿人使用。中文属于汉藏语系。

中文使用汉字作为书写系统。汉字有几千年的历史，是世界上最古老的文字系统之一。

现代中文主要有两种形式：普通话（标准汉语）和粤语。普通话是中国的官方语言。

学习中文对外国人来说是一个挑战，但也很有趣。掌握中文可以帮助了解中国文化和历史。""",
        "category": "Language"
    },
    {
        "title": "茶文化",
        "text": """茶是中国最重要的饮料之一，有着几千年的历史。中国是茶的故乡。

中国有六大茶类：绿茶、红茶、乌龙茶、白茶、黄茶和黑茶。不同的茶有不同的味道和功效。

喝茶在中国不仅是解渴，更是一种文化和艺术。茶道讲究泡茶的技巧和品茶的心境。

茶馆是中国城市中常见的场所。人们在茶馆里喝茶、聊天、下棋。""",
        "category": "Culture"
    },
    {
        "title": "上海",
        "text": """上海是中国最大的城市，也是重要的经济和金融中心。上海位于长江入海口。

上海有着独特的历史。在20世纪初，上海是远东最繁华的城市之一。外滩保留了许多历史建筑。

现代上海是一个国际大都市。陆家嘴的摩天大楼展示了上海的现代化。

上海也是中国的时尚和文化中心。这里有众多博物馆、剧院和艺术画廊。""",
        "category": "Cities"
    },
    {
        "title": "高铁",
        "text": """中国高速铁路网是世界上最大的高铁系统。高铁连接了中国的主要城市。

中国的高铁速度可达每小时350公里。从北京到上海只需要5个小时。

高铁的发展改变了中国人的出行方式。现在，人们可以方便快捷地在城市之间旅行。

中国高铁技术也出口到其他国家，帮助建设他们的铁路系统。""",
        "category": "Technology"
    },
    {
        "title": "饺子",
        "text": """饺子是中国最受欢迎的传统食物之一。饺子通常用面皮包裹肉和蔬菜馅。

在中国北方，过年时吃饺子是重要的传统。饺子的形状像古代的元宝，象征财富。

制作饺子是一项家庭活动。家人围坐在一起，边包饺子边聊天。

饺子有多种烹饪方法：可以煮、蒸或煎。不同地区有不同的饺子馅料和做法。""",
        "category": "Food"
    },
]

def load_sample_articles():
    """Load sample articles into database"""
    print("="*60)
    print("LOADING SAMPLE WIKIPEDIA ARTICLES")
    print("="*60)
    print()

    # Create tables
    Base.metadata.create_all(engine)

    db = SessionLocal()

    try:
        loaded = 0
        
        for article_data in SAMPLE_ARTICLES:
            print(f"Processing: {article_data['title']}")
            
            # Check if article already exists
            existing = db.query(Article).filter(Article.title == article_data['title']).first()
            if existing:
                print(f"Already exists, skipping")
                continue
            
            # Segment text
            segments = segment_text(article_data['text'])
            
            # Calculate metadata
            word_count = len(segments)
            unique_chars = len(set(article_data['text']))
            hsk_level = estimate_hsk_level(article_data['text'])
            
            # Create summary (first 100 chars)
            summary = article_data['text'][:100]
            if len(article_data['text']) > 100:
                summary += "..."
            
            # Create article
            article = Article(
                title=article_data['title'],
                text=article_data['text'],
                summary=summary,
                category=article_data['category'],
                segments=segments,
                word_count=word_count,
                unique_char_count=unique_chars,
                hsk_level=hsk_level
            )
            
            db.add(article)
            loaded += 1
            
            print(f"Loaded - {word_count} words, HSK {hsk_level}")
        
        db.commit()
        
        print(f"\n{'='*60}")
        print(f"Successfully loaded {loaded} articles")
        print(f"{'='*60}")
        
        # Show stats
        total = db.query(Article).count()
        print(f"\nDatabase now has {total} total articles")
        
        # Show articles by category
        print("\nArticles by category:")
        from sqlalchemy import func
        categories = db.query(
            Article.category,
            func.count(Article.id).label('count')
        ).group_by(Article.category).all()
        
        for cat, count in categories:
            print(f"  {cat}: {count} articles")
        
        # Show HSK distribution
        print("\nArticles by HSK level:")
        hsk_dist = db.query(
            Article.hsk_level,
            func.count(Article.id).label('count')
        ).group_by(Article.hsk_level).order_by(Article.hsk_level).all()
        
        for level, count in hsk_dist:
            print(f"  HSK {level}: {count} articles")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        db.rollback()
        return False
    
    finally:
        db.close()


if __name__ == "__main__":
    success = load_sample_articles()
    
    if success:
        print("\n" + "="*60)
        print("SAMPLE ARTICLES LOADED SUCCESSFULLY")
        print("="*60)
        print("\nTest your API:")
        print("  curl http://localhost:8000/api/articles")
    else:
        print("\n" + "="*60)
        print("LOADING FAILED")
        print("="*60)   