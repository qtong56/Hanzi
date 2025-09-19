import { defineConfig } from 'vite'
import { resolve } from 'path'
import fs from 'fs'

export default defineConfig(({ command }) => ({
  root: 'src',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        index: resolve(__dirname, 'src/index.html'),
        reader: resolve(__dirname, 'src/reader.html')
      },
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    },
  },
  plugins: [
    {
      name: 'copy-data',
      closeBundle() {
        // Copy data directory to dist
        const srcDataDir = resolve(__dirname, 'src/data')
        const distDataDir = resolve(__dirname, 'dist/data')
        
        if (fs.existsSync(srcDataDir)) {
          fs.mkdirSync(distDataDir, { recursive: true })
          const files = fs.readdirSync(srcDataDir)
          files.forEach(file => {
            fs.copyFileSync(
              resolve(srcDataDir, file),
              resolve(distDataDir, file)
            )
          })
        }
      }
    }
  ],
  // Only use /Hanzi/ base for production builds
  base: command === 'build' ? '/Hanzi/' : '/',
  server: {
    port: 3000,
    open: true
  }
}))