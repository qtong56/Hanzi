# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Chinese reading practice platform called "Hanzi" - enables learners to read Chinese articles with instant click-to-translate functionality and difficulty-appropriate content selection.

## Project Status
Early stage - comprehensive PRD exists but implementation not yet started. The project is planned as a static-first platform with TypeScript, vanilla HTML/CSS/JS, targeting GitHub Pages deployment.

## Development Commands
```bash
# Project initialization (when ready)
npm init -y
npm install -D typescript @types/node

# Development workflow (planned)
npm run dev        # Start local development server
npm run build      # Build for production  
npm run test       # Run tests
npm run deploy     # Deploy to GitHub Pages
```

## Architecture Overview
Based on PRD specifications:

### Tech Stack
- **Frontend**: Vanilla HTML/CSS/JavaScript + TypeScript
- **Data**: Static JSON files for articles and vocabulary
- **Hosting**: GitHub Pages (static site)
- **Styling**: Custom CSS with mobile-first approach

### Core Components (planned)
- `ChineseFlowApp` - Main application class handling initialization and state
- `ChineseSegmenter` - Text segmentation for clickable Chinese characters
- Translation tooltip system with pinyin and HSK level indicators
- Progress tracking via localStorage

### File Structure (planned)
```
├── index.html               # Landing page
├── reader.html              # Reading interface  
├── about.html               # About page
├── data/
│   ├── articles.json        # Article metadata + content
│   ├── vocabulary.json      # HSK words + translations
│   └── sentences.json       # Pre-translated sentences
├── js/
│   ├── app.ts              # Main application logic
│   ├── reader.ts           # Reading interface
│   ├── segmentation.ts     # Chinese text processing
│   └── analytics.ts        # Event tracking
├── css/
│   ├── styles.css          # Main styles
│   └── mobile.css          # Mobile optimizations
└── assets/
    └── icons/              # UI icons
```

### Data Models (from PRD)
- **Article**: id, slug, title, content, difficulty, hskLevel, estimatedMinutes, tags, source, wordCount
- **VocabularyEntry**: character → {pinyin, translation, hskLevel, frequency}
- **UserProgress**: articlesRead[], wordsEncountered{}, totalReadingTime

## Key Features
- Click-to-translate Chinese characters with pinyin and English translation
- HSK difficulty level indicators
- Reading progress tracking (localStorage)
- Mobile-first responsive design
- 3 difficulty levels: beginner (HSK 4), intermediate (HSK 5), advanced (HSK 6)

## Development Notes
- Target: 20 curated articles across 3 difficulty levels for MVP
- Focus on mobile reading experience optimization
- No backend initially - static site with JSON data files
- Migration to Next.js planned when reaching 500+ DAU