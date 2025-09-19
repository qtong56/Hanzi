// src/js/app.ts - Minimal but extensible foundation
interface AppConfig {
  debug: boolean;
  version: string;
}

class HanziApp {
  private config: AppConfig;
  
  constructor() {
    this.config = {
      debug: location.hostname === 'localhost',
      version: '1.0.0'
    };
    
    this.log('Hanzi app initializing...');
    this.init();
  }
  
  private async init(): Promise<void> {
    try {
      this.setupEventListeners();
      this.log('App initialized successfully');
    } catch (error) {
      this.handleError('Failed to initialize app', error);
    }
  }
  
  private setupEventListeners(): void {
    // Global error handling
    window.addEventListener('error', (event) => {
      this.handleError('Uncaught error', event.error);
    });
    
    // Handle CTA button clicks
    document.querySelectorAll('.cta-button').forEach(button => {
      button.addEventListener('click', (e) => {
        this.log('User clicked start reading');
        // Analytics would go here
      });
    });
  }
  
  private log(message: string, data?: any): void {
    if (this.config.debug) {
      console.log(`[Hanzi] ${message}`, data || '');
    }
  }
  
  private handleError(message: string, error: any): void {
    console.error(`[Hanzi Error] ${message}:`, error);
    // Error reporting would go here
  }
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
  new HanziApp();
});