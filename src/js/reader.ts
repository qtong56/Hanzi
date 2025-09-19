import { ChineseSegmenter } from './segmentation.js';

interface Article {
  id: number;
  slug: string;
  title: string;
  content: string;
  difficulty: string;
  hskLevel: number;
  estimatedMinutes: number;
  tags: string[];
  source: string;
  wordCount: number;
}

interface UserProgress {
  wordsEncountered: Record<string, {
    count: number;
    firstSeen: string;
    lastSeen: string;
  }>;
  articlesRead: string[];
}

class HanziReader {
  private articles: Article[] = [];
  private segmenter: ChineseSegmenter | null = null;
  private currentArticle: Article | null = null;
  private userProgress: UserProgress;
  private activeTooltip: HTMLElement | null = null;

  constructor() {
    this.userProgress = this.loadUserProgress();
    this.log('Reader initializing...');
    this.init();
  }

  private async init(): Promise<void> {
    try {
      await this.loadData();
      this.setupEventListeners();
      this.renderArticleList();
      this.log('Reader initialized successfully');
    } catch (error) {
      this.handleError('Failed to load reader', error);
    }
  }

  private async loadData(): Promise<void> {
    try {
      // Load vocabulary and articles in parallel
      const [vocabResponse, articlesResponse] = await Promise.all([
        fetch('./data/vocabulary.json'),  // Fixed path
        fetch('./data/articles.json')     // Fixed path
      ]);

      if (!vocabResponse.ok || !articlesResponse.ok) {
        throw new Error('Failed to fetch data files');
      }

      const vocabulary = await vocabResponse.json();
      const articlesData = await articlesResponse.json();

      // Initialize segmenter with vocabulary
      this.segmenter = new ChineseSegmenter(vocabulary);
      this.articles = articlesData.articles;

      this.log(`Loaded ${Object.keys(vocabulary).length} vocabulary entries`);
      this.log(`Loaded ${this.articles.length} articles`);

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      throw new Error(`Failed to load data: ${errorMessage}`);
    }
  }

  private setupEventListeners(): void {
    // Handle Chinese word clicks
    document.addEventListener('click', this.handleWordClick.bind(this));

    // Hide tooltip on outside click
    document.addEventListener('click', this.handleOutsideClick.bind(this));

    // Keyboard shortcuts
    document.addEventListener('keydown', this.handleKeyboard.bind(this));
  }

  private handleWordClick(event: Event): void {
    const target = event.target as HTMLElement;

    if (!target.classList.contains('clickable')) {
      return;
    }

    event.preventDefault();
    event.stopPropagation();

    const word = target.dataset.word;
    if (!word || !this.segmenter) return;

    const translation = this.segmenter.getTranslation(word);
    if (translation) {
      this.showTooltip(target, word, translation);
      this.trackWordEncounter(word);
    }
  }

  private showTooltip(element: HTMLElement, word: string, translation: any): void {
    this.hideTooltip();

    const tooltip = document.createElement('div');
    tooltip.className = 'translation-tooltip';
    tooltip.innerHTML = `
      <div class="tooltip-word">${word}</div>
      <div class="tooltip-pinyin">${translation.pinyin}</div>
      <div class="tooltip-translation">${translation.translation}</div>
      <div class="tooltip-hsk">HSK ${translation.hskLevel}</div>
    `;

    // Position tooltip
    const rect = element.getBoundingClientRect();
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    tooltip.style.position = 'absolute';
    tooltip.style.left = `${rect.left + rect.width / 2}px`;
    tooltip.style.top = `${rect.top + scrollTop - 10}px`;
    tooltip.style.transform = 'translateX(-50%) translateY(-100%)';
    tooltip.style.zIndex = '1000';

    document.body.appendChild(tooltip);
    this.activeTooltip = tooltip;

    // Auto-hide after 4 seconds
    setTimeout(() => {
      if (this.activeTooltip === tooltip) {
        this.hideTooltip();
      }
    }, 4000);
  }

  private hideTooltip(): void {
    if (this.activeTooltip) {
      this.activeTooltip.remove();
      this.activeTooltip = null;
    }
  }

  private handleOutsideClick(event: Event): void {
    const target = event.target as HTMLElement;

    if (this.activeTooltip &&
      !this.activeTooltip.contains(target) &&
      !target.classList.contains('clickable')) {
      this.hideTooltip();
    }
  }

  private handleKeyboard(event: KeyboardEvent): void {
    if (event.key === 'Escape') {
      this.hideTooltip();
    }
  }

  private trackWordEncounter(word: string): void {
    const now = new Date().toISOString();

    if (this.userProgress.wordsEncountered[word]) {
      this.userProgress.wordsEncountered[word].count++;
      this.userProgress.wordsEncountered[word].lastSeen = now;
    } else {
      this.userProgress.wordsEncountered[word] = {
        count: 1,
        firstSeen: now,
        lastSeen: now
      };
    }

    this.saveUserProgress();
    this.log(`Word encounter tracked: ${word}`);
  }

  private renderArticleList(): void {
    const container = document.getElementById('article-container');
    if (!container) return;

    container.innerHTML = `
      <div class="article-list">
        <header class="list-header">
          <h2>Choose an Article</h2>
          <p>Click any Chinese character in the articles for instant translation</p>
        </header>
        
        <div class="article-grid">
          ${this.articles.map(article => `
            <div class="article-card" data-slug="${article.slug}">
              <div class="article-header">
                <span class="difficulty-badge difficulty-${article.difficulty}">
                  ${article.difficulty}
                </span>
                <span class="hsk-level">HSK ${article.hskLevel}</span>
              </div>
              
              <h3 class="article-title">${article.title}</h3>
              
              <div class="article-meta">
                <span>${article.estimatedMinutes} min read</span>
                <span>${article.wordCount} characters</span>
              </div>
              
              <div class="article-tags">
                ${article.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    // Add click event listeners to article cards
    document.querySelectorAll('.article-card').forEach(card => {
      card.addEventListener('click', () => {
        const slug = (card as HTMLElement).dataset.slug;
        if (slug) {
          this.loadArticle(slug);
        }
      });
    });
  }

  public loadArticle(slug: string): void {
    const article = this.articles.find(a => a.slug === slug);
    if (!article || !this.segmenter) return;

    this.currentArticle = article;
    const segmentedContent = this.segmenter.renderClickableText(article.content);

    const container = document.getElementById('article-container');
    if (!container) return;

    container.innerHTML = `
      <article class="reading-article">
        <header class="article-header">
          <div class="article-meta">
            <span class="difficulty-badge difficulty-${article.difficulty}">
              ${article.difficulty}
            </span>
            <span class="hsk-level">HSK ${article.hskLevel}</span>
            <span class="reading-time">${article.estimatedMinutes} min</span>
          </div>
          
          <h1 class="article-title">${article.title}</h1>
          
          <div class="reading-instructions">
            💡 Click any Chinese character for translation and pinyin
          </div>
        </header>
        
        <div class="reading-content">
          <div class="chinese-text">${segmentedContent}</div>
        </div>
        
        <footer class="article-footer">
          <button class="btn btn-secondary" id="backButton">
            ← Back to Articles
          </button>
          <button class="btn btn-primary" id="completeButton">
            Mark as Complete
          </button>
        </footer>
      </article>
    `;

    // Add event listeners to buttons
    document.getElementById('backButton')?.addEventListener('click', () => {
      this.showArticleList();
    });

    document.getElementById('completeButton')?.addEventListener('click', () => {
      this.completeArticle();
    });

    // Update URL without page reload
    const url = new URL(window.location.href);
    url.searchParams.set('article', slug);
    window.history.pushState({}, '', url.toString());
  }

  public completeArticle(): void {
    if (!this.currentArticle) return;

    // Track completion
    if (!this.userProgress.articlesRead.includes(this.currentArticle.slug)) {
      this.userProgress.articlesRead.push(this.currentArticle.slug);
      this.saveUserProgress();
    }

    // Show completion feedback
    alert(`Great job completing "${this.currentArticle.title}"! 🎉`);
    this.showArticleList();
  }

  public showArticleList(): void {
    this.currentArticle = null;
    this.renderArticleList();

    // Update URL
    const url = new URL(window.location.href);
    url.searchParams.delete('article');
    window.history.pushState({}, '', url.toString());
  }

  private loadUserProgress(): UserProgress {
    try {
      const stored = localStorage.getItem('hanzi_progress');
      return stored ? JSON.parse(stored) : {
        wordsEncountered: {},
        articlesRead: []
      };
    } catch (error) {
      this.log('Failed to load user progress, using defaults');
      return { wordsEncountered: {}, articlesRead: [] };
    }
  }

  private saveUserProgress(): void {
    try {
      localStorage.setItem('hanzi_progress', JSON.stringify(this.userProgress));
    } catch (error) {
      this.log('Failed to save user progress');
    }
  }

  private log(message: string): void {
    console.log(`[Reader] ${message}`);
  }

  private handleError(message: string, error: any): void {
    console.error(`[Reader Error] ${message}:`, error);

    const container = document.getElementById('article-container');
    if (container) {
      container.innerHTML = `
        <div class="error-state">
          <h2>Something went wrong</h2>
          <p>${message}</p>
          <button class="btn btn-primary" onclick="location.reload()">
            Try Again
          </button>
        </div>
      `;
    }
  }
}

// Initialize reader and expose globally
let reader: HanziReader;

document.addEventListener('DOMContentLoaded', () => {
  reader = new HanziReader();
  // Expose for debugging/console access
  (window as any).reader = reader;
});