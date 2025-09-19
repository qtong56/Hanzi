interface VocabularyEntry {
  pinyin: string;
  translation: string;
  hskLevel: number;
  frequency?: number;
}

export class ChineseSegmenter {
  private vocabulary: Map<string, VocabularyEntry>;
  
  constructor(vocabulary: Record<string, VocabularyEntry>) {
    this.vocabulary = new Map(Object.entries(vocabulary));
  }
  
  segmentText(text: string): string[] {
    const segments: string[] = [];
    let i = 0;
    
    while (i < text.length) {
      const char = text[i];
      
      if (this.isChinese(char)) {
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
    for (let len = Math.min(4, text.length); len >= 2; len--) {
      const candidate = text.substring(0, len);
      if (this.vocabulary.has(candidate)) {
        return candidate;
      }
    }
    return null;
  }
  
  private isChinese(char: string): boolean {
    const code = char.charCodeAt(0);
    return (code >= 0x4e00 && code <= 0x9fff) || (code >= 0x3400 && code <= 0x4dbf);
  }
  
  renderClickableText(text: string): string {
    const segments = this.segmentText(text);
    
    return segments.map(segment => {
      if (this.isChinese(segment)) {
        const hasTranslation = this.vocabulary.has(segment);
        const className = hasTranslation ? 'chinese-word clickable' : 'chinese-word unknown';
        return `<span class="${className}" data-word="${segment}">${segment}</span>`;
      }
      return segment;
    }).join('');
  }
  
  getTranslation(word: string): VocabularyEntry | null {
    return this.vocabulary.get(word) || null;
  }
}