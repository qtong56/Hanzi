// src/js/reader.ts - Reader page foundation
class HanziReader {
  private articles: any[] = [];
  
  constructor() {
    this.log('Reader initializing...');
    this.init();
  }
  
  private async init(): Promise<void> {
    try {
      await this.loadData();
      this.renderArticleList();
    } catch (error) {
      this.handleError('Failed to load reader', error);
    }
  }
  
  private async loadData(): Promise<void> {
    // For now, use placeholder data
    this.articles = [
      {
        id: 1,
        title: '现代城市生活',
        content: '现在的城市生活和以前很不一样。',
        difficulty: 'intermediate'
      }
    ];
    
    this.log(`Loaded ${this.articles.length} articles`);
  }
  
  private renderArticleList(): void {
    const container = document.getElementById('article-container');
    if (!container) return;
    
    container.innerHTML = `
      <div class="article-list">
        <h2>Choose an Article</h2>
        ${this.articles.map(article => `
          <div class="article-card" onclick="reader.loadArticle(${article.id})">
            <h3>${article.title}</h3>
            <span class="difficulty">${article.difficulty}</span>
          </div>
        `).join('')}
      </div>
    `;
  }
  
  loadArticle(id: number): void {
    const article = this.articles.find(a => a.id === id);
    if (!article) return;
    
    const container = document.getElementById('article-container');
    if (!container) return;
    
    container.innerHTML = `
      <article class="reading-article">
        <h1>${article.title}</h1>
        <div class="content" style="font-family: var(--font-chinese); font-size: 1.5rem; line-height: 2;">
          ${article.content}
        </div>
        <button onclick="reader.showArticleList()">← Back to Articles</button>
      </article>
    `;
  }
  
  showArticleList(): void {
    this.renderArticleList();
  }
  
  private log(message: string): void {
    console.log(`[Reader] ${message}`);
  }
  
  private handleError(message: string, error: any): void {
    console.error(`[Reader Error] ${message}:`, error);
    
    const container = document.getElementById('article-container');
    if (container) {
      container.innerHTML = `
        <div class="error">
          <h2>Something went wrong</h2>
          <p>${message}</p>
          <button onclick="location.reload()">Try Again</button>
        </div>
      `;
    }
  }
}

// Global instance for onclick handlers
let reader: HanziReader;

document.addEventListener('DOMContentLoaded', () => {
  reader = new HanziReader();
});