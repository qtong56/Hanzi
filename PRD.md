ChineseFlow - Final Production Ready Document (PRD)
Executive Summary
Product: Static-first Chinese reading practice platform
Timeline: 2 weeks to launch
Goal: 100+ daily active users within 30 days
Architecture: Static site → Next.js migration path

1. Product Specification
1.1 Core User Problem
Chinese language learners struggle to find reading material at their appropriate difficulty level and lack instant translation tools for unknown words.
1.2 Solution
A curated collection of Chinese articles with instant click-to-translate functionality and difficulty-appropriate content selection.
1.3 MVP Features (Launch Week)
✅ 20 hand-curated articles across 3 difficulty levels
✅ Click-to-translate - Any Chinese character shows pinyin + translation
✅ Difficulty indicators - Clear HSK level labeling
✅ Progress tracking - localStorage-based reading history
✅ Mobile-first design - Optimized for phone reading
1.4 Success Metrics

Primary: 60%+ article completion rate
Secondary: 5+ articles read per active user
Growth: 20%+ week-over-week user growth


2. Technical Architecture
2.1 Technology Stack
Frontend: Vanilla HTML/CSS/JavaScript + TypeScript
Data: Static JSON files
Hosting: GitHub Pages (free, global CDN)
Analytics: Google Analytics 4
Monitoring: Simple error logging
2.2 File Structure
chineseflow/
├── index.html                 # Landing page
├── reader.html                # Reading interface  
├── about.html                 # About page
├── data/
│   ├── articles.json          # Article metadata + content
│   ├── vocabulary.json        # HSK words + translations
│   └── sentences.json         # Pre-translated sentences
├── js/
│   ├── app.ts                 # Main application logic
│   ├── reader.ts              # Reading interface
│   ├── segmentation.ts        # Chinese text processing
│   └── analytics.ts           # Event tracking
├── css/
│   ├── styles.css             # Main styles
│   └── mobile.css             # Mobile optimizations
├── assets/
│   └── icons/                 # UI icons
└── README.md
2.3 Data Schema
typescript// articles.json
interface Article {
  id: number;
  slug: string;
  title: string;
  content: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  hskLevel: 4 | 5 | 6;
  estimatedMinutes: number;
  tags: string[];
  source: string;
  wordCount: number;
}

// vocabulary.json  
interface VocabularyEntry {
  [character: string]: {
    pinyin: string;
    translation: string;
    hskLevel: number;
    frequency?: number;
  };
}

// User progress (localStorage)
interface UserProgress {
  articlesRead: string[];
  wordsEncountered: Record<string, {
    count: number;
    firstSeen: string;
    lastSeen: string;
  }>;
  totalReadingTime: number;
}

3. Development Plan
3.1 Sprint 1 (Days 1-7): Foundation
Day 1-2: Setup & Structure

 GitHub repo setup with GitHub Pages
 Basic HTML structure and navigation
 TypeScript configuration
 CSS framework (custom, mobile-first)

Day 3-5: Core Reading Interface

 Chinese text rendering and segmentation
 Click-to-translate tooltip system
 Article navigation and routing
 Progress tracking (localStorage)

Day 6-7: Content Integration

 Article JSON structure and loading
 Vocabulary JSON integration
 Error handling and fallbacks

3.2 Sprint 2 (Days 8-14): Content & Launch
Day 8-10: Content Creation

 Curate and format 20 articles
 Verify translations and pinyin
 Difficulty level assignment and testing
 Article tagging and categorization

Day 11-12: Polish & Testing

 Cross-browser testing (Chrome, Safari, Firefox)
 Mobile responsiveness testing
 Performance optimization
 SEO optimization

Day 13-14: Launch Preparation

 Analytics integration
 Error monitoring setup
 Social sharing features
 Feedback collection system


4. Content Strategy
4.1 Article Selection Criteria
Topics: Daily life, culture, technology, travel, food
Length: 200-500 characters (5-10 minute reads)
Sources: Public domain texts, original content, CC-licensed material
Distribution:

Beginner (HSK 4): 5 articles - 85%+ known vocabulary
Intermediate (HSK 5): 10 articles - 70-80% known vocabulary
Advanced (HSK 6): 5 articles - 60-70% known vocabulary

4.2 Quality Standards

Native Chinese speaker content review
Manual translation verification for key vocabulary
User testing with 3+ Chinese learners per difficulty level
Mobile reading experience optimization


5. Core Implementation
5.1 Main Application Logic
typescript// app.ts - Core application class
class ChineseFlowApp {
  private vocabulary: Map<string, VocabularyEntry>;
  private articles: Article[];
  private userProgress: UserProgress;
  private currentArticle: Article | null = null;

  constructor() {
    this.userProgress = this.loadUserProgress();
    this.init();
  }

  async init(): Promise<void> {
    try {
      await this.loadData();
      this.setupEventListeners();
      this.renderInterface();
    } catch (error) {
      this.handleError('Failed to initialize app', error);
    }
  }

  private async loadData(): Promise<void> {
    const [vocabData, articleData] = await Promise.all([
      fetch('/data/vocabulary.json').then(r => r.json()),
      fetch('/data/articles.json').then(r => r.json())
    ]);
    
    this.vocabulary = new Map(Object.entries(vocabData));
    this.articles = articleData.articles;
  }

  private handleCharacterClick(event: Event): void {
    const target = event.target as HTMLElement;
    const character = target.textContent?.trim();
    
    if (character && this.vocabulary.has(character)) {
      const translation = this.vocabulary.get(character)!;
      this.showTooltip(target, translation);
      this.trackWordEncounter(character);
    }
  }

  private showTooltip(element: HTMLElement, data: VocabularyEntry): void {
    const tooltip = document.createElement('div');
    tooltip.className = 'translation-tooltip';
    tooltip.innerHTML = `
      <div class="pinyin">${data.pinyin}</div>
      <div class="translation">${data.translation}</div>
      <div class="hsk-level">HSK ${data.hskLevel}</div>
    `;

    // Position tooltip
    const rect = element.getBoundingClientRect();
    tooltip.style.left = `${rect.left + rect.width / 2}px`;
    tooltip.style.top = `${rect.top - 10}px`;
    tooltip.style.transform = 'translateX(-50%) translateY(-100%)';

    document.body.appendChild(tooltip);
    setTimeout(() => tooltip.remove(), 3000);
  }

  private trackWordEncounter(character: string): void {
    const now = new Date().toISOString();
    
    if (this.userProgress.wordsEncountered[character]) {
      this.userProgress.wordsEncountered[character].count++;
      this.userProgress.wordsEncountered[character].lastSeen = now;
    } else {
      this.userProgress.wordsEncountered[character] = {
        count: 1,
        firstSeen: now,
        lastSeen: now
      };
    }
    
    this.saveUserProgress();
  }

  private saveUserProgress(): void {
    localStorage.setItem('chineseflow_progress', JSON.stringify(this.userProgress));
  }

  private loadUserProgress(): UserProgress {
    const stored = localStorage.getItem('chineseflow_progress');
    return stored ? JSON.parse(stored) : {
      articlesRead: [],
      wordsEncountered: {},
      totalReadingTime: 0
    };
  }
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
  new ChineseFlowApp();
});
5.2 Chinese Text Segmentation
typescript// segmentation.ts - Simple but effective word boundary detection
class ChineseSegmenter {
  constructor(private vocabulary: Map<string, VocabularyEntry>) {}

  segmentText(text: string): string[] {
    const segments: string[] = [];
    let i = 0;

    while (i < text.length) {
      const char = text[i];
      
      if (this.isChinese(char)) {
        // Try to find longest matching word (up to 4 characters)
        const word = this.findLongestWord(text.substring(i)) || char;
        segments.push(word);
        i += word.length;
      } else {
        segments.push(char);
        i++;
      }
    }

    return segments;
  }

  private findLongestWord(text: string): string | null {
    // Check 4-char, 3-char, 2-char combinations
    for (let len = Math.min(4, text.length); len >= 2; len--) {
      const candidate = text.substring(0, len);
      if (this.vocabulary.has(candidate)) {
        return candidate;
      }
    }
    return null;
  }

  private isChinese(char: string): boolean {
    return /[\u4e00-\u9fff]/.test(char);
  }

  renderSegmentedText(text: string): string {
    const segments = this.segmentText(text);
    
    return segments.map(segment => {
      if (this.isChinese(segment)) {
        const hasTranslation = this.vocabulary.has(segment);
        const className = hasTranslation ? 'chinese-word translatable' : 'chinese-word';
        return `<span class="${className}" data-word="${segment}">${segment}</span>`;
      }
      return segment;
    }).join('');
  }
}
5.3 Mobile-First CSS
css/* styles.css - Clean, responsive design */
:root {
  --primary-color: #2563eb;
  --secondary-color: #64748b;
  --background: #ffffff;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --border: #e2e8f0;
  --success: #10b981;
  --warning: #f59e0b;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: var(--text-primary);
  background: var(--background);
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

/* Reading Interface */
.reading-text {
  font-size: 18px;
  line-height: 2;
  font-family: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  margin: 40px 0;
}

.chinese-word {
  cursor: pointer;
  padding: 2px 1px;
  border-radius: 3px;
  transition: all 0.2s ease;
}

.chinese-word.translatable:hover {
  background-color: #dbeafe;
  transform: scale(1.05);
}

/* Translation Tooltip */
.translation-tooltip {
  position: fixed;
  background: #1f2937;
  color: white;
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  z-index: 1000;
  max-width: 250px;
  pointer-events: none;
}

.translation-tooltip .pinyin {
  color: #93c5fd;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 4px;
}

.translation-tooltip .translation {
  font-size: 14px;
  line-height: 1.4;
  margin-bottom: 4px;
}

.translation-tooltip .hsk-level {
  color: #9ca3af;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Article List */
.article-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 16px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.article-card:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.article-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.article-meta {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

.difficulty-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.difficulty-beginner { background: #dcfce7; color: #166534; }
.difficulty-intermediate { background: #fef3c7; color: #92400e; }
.difficulty-advanced { background: #fecaca; color: #991b1b; }

/* Mobile Responsive */
@media (max-width: 768px) {
  .container {
    padding: 16px;
  }
  
  .reading-text {
    font-size: 16px;
    line-height: 1.8;
    margin: 24px 0;
  }
  
  .article-card {
    padding: 20px;
  }
  
  .translation-tooltip {
    max-width: 200px;
    padding: 10px 12px;
  }
}

/* Loading States */
.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  font-size: 16px;
  color: var(--text-secondary);
}

/* Error States */
.error-message {
  background: #fef2f2;
  color: #991b1b;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #fecaca;
  margin: 20px 0;
}

6. Launch & Growth Strategy
6.1 Pre-Launch (Days 11-14)

 Beta test with 10 Chinese learners
 Social media accounts setup (@ChineseFlow)
 Content calendar for launch week
 Feedback collection system setup

6.2 Launch Week

 Submit to r/ChineseLanguage and language learning communities
 Share on Twitter with development story thread
 Post to Hacker News with "Show HN" post
 Reach out to Chinese learning YouTubers/bloggers

6.3 Growth Metrics
Week 1 Goals:

100+ unique visitors
50+ articles read
10+ user feedback responses

Month 1 Goals:

1000+ unique visitors
500+ total articles read
20%+ return visitor rate


7. Migration Path
7.1 When to Add Backend (Triggers)

500+ daily active users
Users requesting account sync
Need for user-generated content
Complex analytics requirements

7.2 Next.js Migration Strategy
typescript// Gradual migration: Static → SSG → Full Stack
// Phase 1: Keep static files, add dynamic features
// Phase 2: Move to database, add user accounts
// Phase 3: Add real-time features, community features
7.3 Feature Roadmap (Post-MVP)
Phase 2 (Month 2-3):

User accounts and progress sync
More article categories
Reading statistics dashboard
Social sharing features

Phase 3 (Month 4-6):

Automated content sourcing
Spaced repetition system
Community features (comments, ratings)
Mobile app (React Native)


8. Deployment Instructions
8.1 Setup Commands
bash# Clone and setup
git clone https://github.com/yourusername/chineseflow.git
cd chineseflow
npm init -y
npm install -D typescript @types/node

# Development
npm run dev        # Start local server
npm run build      # Build for production
npm run test       # Run tests
npm run deploy     # Deploy to GitHub Pages
8.2 GitHub Pages Configuration
yaml# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '18'
    - name: Install and Build
      run: |
        npm install
        npm run build
    - name: Deploy
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./dist

9. Success Definition
Technical Success:

Site loads in <3 seconds on mobile
99%+ uptime (GitHub Pages SLA)
Zero critical bugs in production

Product Success:

100+ daily active users by day 30
60%+ article completion rate
4.5+ user satisfaction rating

Business Success:

Organic growth through word-of-mouth
Featured in Chinese learning communities
Potential partnerships or acquisition interest


This PRD provides everything needed to ship a production-ready Chinese reading platform in 2 weeks. The focus is on user value over technical complexity, with a clear path to scale based on real user feedback.