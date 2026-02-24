import { type ReactNode } from "react"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { render } from "@testing-library/react"

export function renderWithQuery(ui: ReactNode) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  })
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>
  )
}

export function makeArticle(overrides = {}) {
  return {
    id: 1,
    title: "中国",
    summary: "中国是位于东亚的国家。",
    hsk_level: 1,
    word_count: 50,
    text: "中国是一个国家。",
    segments: [
      { text: "中国", start: 0, end: 2, pinyin: "zhōng guó" },
      { text: "是", start: 2, end: 3, pinyin: "shì" },
      { text: "一个", start: 3, end: 5, pinyin: "yī gè" },
      { text: "国家", start: 5, end: 7, pinyin: "guó jiā" },
      { text: "。", start: 7, end: 8, pinyin: "" },
    ],
    created_at: null,
    ...overrides,
  }
}

export function makeArticleList(count = 3) {
  return Array.from({ length: count }, (_, i) => ({
    id: i + 1,
    title: `文章 ${i + 1}`,
    summary: "这是一篇文章。",
    hsk_level: ((i % 6) + 1) as 1 | 2 | 3 | 4 | 5 | 6,
    word_count: 100 + i * 10,
  }))
}
