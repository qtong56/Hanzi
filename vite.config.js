import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'src/index.html'),
        reader: resolve(__dirname, 'src/reader.html')
      }
    }
  },
  base: '/Hanzi/'
})