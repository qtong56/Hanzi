"""
Create sample Wikipedia articles for testing.

This simulates what we'd get from the real Wikipedia dump.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, Base, engine
from app.models.article import Article
from app.services.segmentation import segment_text, estimate_hsk_level, dominant_hsk_level, count_chinese_chars

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

    # --- HSK 1 target ---
    {
        "title": "我的家人",
        "text": """我叫王明，是学生。我家有四口人：爸爸、妈妈、我和妹妹。爸爸是老师，妈妈在家。妹妹很小，今年五岁。

我家在北京。我们的家不大，但是很好。家里有三个房间。我的房间里有一张床和一张桌子。

我每天去学校。我喜欢学校，老师好，朋友多。我们一起学习，一起玩。

我喜欢吃水果，苹果和香蕉都好吃。我也喜欢喝水和喝牛奶。妈妈做的饭很好吃，我最喜欢吃妈妈做的菜。

今天天气很好。我和朋友去公园玩。公园里有很多花，很漂亮。我们很快乐。晚上回家，一家人在一起说话，很幸福。""",
        "category": "Life"
    },
    {
        "title": "我的学校",
        "text": """我的学校很大，有很多学生和老师。学校里有教室、图书馆和运动场。

我每天早上八点到学校。上午我们上语文和数学课。语文老师是女老师，她很好。数学老师是男老师，他说话很多。

中午我在学校吃饭。学校的饭很好吃，有米饭、肉和菜。我喜欢吃学校的饭。

下午我们学习英语。英语课很有意思。我喜欢说英语，但是不太好。

下午三点我回家。回家后我做作业。作业不多，我很快就做完了。做完作业我看书或者看电视。

我喜欢我的学校，也喜欢我的老师和同学。""",
        "category": "Education"
    },

    # --- HSK 2 target ---
    {
        "title": "学汉语",
        "text": """我是外国人，我在北京学习汉语。汉语有一点难，但是很有意思。

我每天学习新的汉字。汉字很多，我需要每天练习。我的中文老师叫李老师，她说话很慢，我能听懂。她对我帮助很大。

我住在学校旁边。每天早上七点半起床，洗脸以后吃早饭。早饭后骑自行车去学校，大约十分钟到。

下午放学后，我喜欢去超市买东西。中国超市里东西很多，价格也不贵。我买了很多水果、蔬菜和牛奶。

我也喜欢看中文电影，听中文音乐。这样可以学到很多新词，也很有趣。

现在我可以说一些简单的中文了，我非常高兴。我会继续努力学习，希望以后能说得很好。""",
        "category": "Education"
    },
    {
        "title": "中国的天气",
        "text": """中国地方很大，不同地方的天气很不一样。

北方的冬天非常冷，会下雪。北京一月的气温经常在零度以下。夏天很热，有时候四十度。北方春天和秋天天气很好，不冷也不热。

南方的天气比北方暖和。广州在南方，冬天不冷，夏天很热，也很湿。南方雨水很多，特别是夏天。

中国西部有高山和沙漠。高山上很冷，沙漠里白天很热，晚上很冷。

中国东部是海，夏天有时候有台风。台风来的时候雨很大，风也很大，要在家里等台风过去。

中国人很喜欢说天气。见面的时候常说"今天天气真好"或者"今天太热了"。天气是大家都喜欢说的话题。""",
        "category": "Geography"
    },

    # --- HSK 3 target ---
    {
        "title": "中国传统节日食品",
        "text": """中国各地的传统节日都有特色食品。这些食品不仅美味，还有特殊的文化意义。

春节是最重要的节日，北方人吃饺子，南方人吃年糕和汤圆。饺子的形状像古代的金元宝，象征财富和好运。大年三十晚上，全家人一起包饺子、吃团圆饭，是最温暖幸福的时刻。

中秋节吃月饼，圆圆的月饼代表团圆和美满。月饼的馅料丰富多样，有莲蓉、豆沙、五仁和蛋黄等。节日当天，人们在月光下赏月、吃月饼、谈天说地，享受节日的气氛。

端午节在农历五月初五，人们赛龙舟、吃粽子，纪念爱国诗人屈原。粽子用竹叶包裹糯米，里面加上豆沙、猪肉或蛋黄，有甜有咸，各地口味不同。

元宵节正月十五，家家户户吃汤圆，象征家庭圆满幸福。这一天还有猜灯谜和赏花灯的活动，非常热闹。

这些节日食品不只是食物，更是中国文化的组成部分，承载着人们对家人团聚和幸福生活的美好愿望。""",
        "category": "Culture"
    },
    {
        "title": "中国的教育",
        "text": """中国非常重视教育。家长都希望孩子能接受良好的教育，考上好大学，找到好工作。

中国的学校教育分为小学、初中、高中和大学。小学六年，初中三年，高中三年。高中毕业后参加高考，根据成绩申请大学。高考对中国学生来说非常重要，被称为"人生的转折点"。

中国学生学习压力比较大。除了学校的功课，很多学生还要参加课外补习班，学习数学、英语、音乐或者画画。

近年来，中国政府推行教育改革，希望减轻学生负担，培养学生的创造力和综合能力，而不只是追求考试成绩。

中国的大学数量越来越多，教育质量也在不断提高。北京大学和清华大学是中国最著名的两所高校，在世界大学排名中也名列前茅。

随着国际化发展，越来越多的中国学生选择出国留学，同时也有更多外国学生来中国学习汉语和了解中国文化。""",
        "category": "Education"
    },

    # --- HSK 5 target ---
    {
        "title": "人工智能",
        "text": """人工智能是当今科技领域发展最为迅猛的方向之一。近年来，深度学习技术的突破推动了图像识别、自然语言处理和自动驾驶等领域的飞速进步。

人工智能的广泛应用正在深刻改变人类的生活和工作方式。智能语音助手、人脸识别系统、医疗辅助诊断等已逐渐融入日常生活，极大提升了效率与便利性。

然而，人工智能的快速发展也引发了伦理和社会层面的广泛担忧。算法偏见可能导致不公平的决策；大规模数据收集对个人隐私构成威胁；自动化生产则可能引发结构性失业问题。

在国际竞争层面，主要大国都将人工智能列为战略性核心技术，加大研发投入，争夺未来竞争格局中的主导地位。

未来，如何在推动技术创新的同时建立有效的监管框架，确保人工智能的发展真正造福全人类，而非加剧不平等或威胁人类安全，是政府、企业和研究者共同面临的紧迫课题。""",
        "category": "Technology"
    },
    {
        "title": "中国城镇化",
        "text": """改革开放以来，中国经历了世界历史上规模最大、速度最快的城镇化进程。数以亿计的农村人口涌入城市，深刻改变了中国的社会结构与经济格局。

城镇化带来了显著的经济效益。城市集聚了先进技术、充裕资本和大量劳动力，为工业化和现代化提供了坚实基础。城市居民的收入水平和生活质量总体上高于农村地区。

然而，快速城镇化也衍生出一系列深层次社会问题。住房紧张、交通拥堵、环境污染以及城乡收入差距持续扩大，成为制约可持续发展的突出矛盾。大量进城务工人员难以平等享有城市公共服务，形成所谓"半城镇化"困境。

为此，中国政府提出"新型城镇化"战略，强调以人为本，推动农业转移人口真正融入城市，同时促进城乡协调发展，致力于实现更高质量、更加包容、更具可持续性的城镇化道路。""",
        "category": "Society"
    },

    # --- HSK 6 target ---
    {
        "title": "古典文学传承",
        "text": """中国古典文学是中华文明数千年积淀的精华，其内在的哲学意蕴、审美追求与人文关怀，在当代社会仍具有不可替代的精神价值。

《诗经》《楚辞》以降，历经汉赋、唐诗、宋词、元曲至明清小说，中国文学呈现出一脉相承而又各具特色的演进脉络。唐诗宋词尤为世人称道，李白的飘逸豪放、杜甫的沉郁顿挫、苏轼的旷达超然，共同构筑了中华诗学的巅峰。

研读古典文学，不仅是对语言文字之美的体悟，更是与先贤智慧的精神对话。儒家的仁义礼智、道家的自然无为、佛家的慈悲圆融，都在文学作品中得到了深刻诠释与生动呈现。

然而，当代年轻人与古典文学之间的距离正在拉大。文言文的阅读障碍、应试教育的功利取向以及数字媒体的冲击，使得传统经典日益边缘化。如何以现代视角重新激活古典文学的生命力，使之成为当代人的精神滋养，是文化传承工作面临的核心挑战。""",
        "category": "Culture"
    },

    # --- HSK 7 target ---
    {
        "title": "先秦哲学",
        "text": """先秦诸子百家所构建的哲学体系，历经两千余年的演变与诠释，至今仍是中华思想文化的精神根脉。儒道释三家的深层对话，塑造了中国人独特的宇宙观、人生观与价值观，其影响渗透于政治制度、伦理规范、文艺创作乃至日常生计的诸多层面。

儒学以"仁"为核心，主张通过修身、齐家、治国、平天下的道德实践来实现社会和谐。孔子所倡导的"克己复礼"与"仁者爱人"，在当代语境下被重新诠释为公民责任、社会关怀与文明对话的思想资源。

道家则以"道法自然"为宗旨，强调"无为而治"与万物齐一的境界。这种对人与自然关系的深刻洞见，在生态文明建设日趋迫切的今天，展现出超越时代的前瞻智慧。

然而，传统哲学的现代转化并非简单的复古或挪用，而需经由严格的诠释学反思与批判性重构。如何在保持传统精髓的同时，回应当代人类面临的普遍性困境，将民族性的思想资源转化为具有普世意义的哲学贡献，仍是中国哲学研究者的重大使命与时代担当。""",
        "category": "Philosophy"
    },
]

def load_sample_articles():
    """Load sample articles into database"""
    print("="*60)
    print("LOADING SAMPLE WIKIPEDIA ARTICLES")
    print("="*60)
    print()

    # Drop and recreate articles table to pick up schema changes
    Article.__table__.drop(engine, checkfirst=True)
    Base.metadata.create_all(engine)
    print("Recreated articles table with latest schema.\n")

    db = SessionLocal()

    try:
        loaded = 0

        for article_data in SAMPLE_ARTICLES:
            print(f"Processing: {article_data['title']}")

            # Segment text
            segments = segment_text(article_data['text'])

            # Calculate metadata
            word_count = count_chinese_chars(article_data['text'])
            unique_chars = len(set(article_data['text']))
            counts = estimate_hsk_level(article_data['text'])
            hsk_level = dominant_hsk_level(counts, count_chinese_chars(article_data['text']))
            hsk_level_counts = {str(k): v for k, v in counts.items()}
            
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
                hsk_level=hsk_level,
                hsk_level_counts=hsk_level_counts,
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