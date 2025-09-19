// vite.config.js - Production-ready from day 1
import { defineConfig } from 'vite';

export default defineConfig({
  root: 'src',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: 'src/index.html',
        reader: 'src/reader.html'
      }
    }
  },
  server: {
    port: 3000,
    open: true,
    host: true // Allow network access for mobile testing
  },
  // GitHub Pages deployment
  base: process.env.NODE_ENV === 'production' ? '/hanzi/' : '/'
});