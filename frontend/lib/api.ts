import { cache } from "react"

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

export interface Segment {
  text: string
  start: number
  end: number
  pinyin: string
}

export interface ArticleListItem {
  id: number
  title: string
  summary: string | null
  hsk_level: number | null
  word_count: number | null
}

export interface Article extends ArticleListItem {
  text: string
  segments: Segment[] | null
  created_at: string | null
}

export interface ArticleListResponse {
  articles: ArticleListItem[]
  total: number
  limit: number
  offset: number
}

export const HSK_LEVEL_COLORS: Record<number, string> = {
  1: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
  2: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100",
  3: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
  4: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-100",
  5: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
  6: "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-100",
}

export function hskLevelColor(level: number | null): string {
  return HSK_LEVEL_COLORS[level ?? 0] ?? "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100"
}

export async function getArticles(params?: {
  limit?: number
  skip?: number
  hsk_level?: number
}): Promise<ArticleListResponse> {
  const url = new URL(`${API_BASE}/api/articles/`)
  if (params?.limit != null) url.searchParams.set("limit", String(params.limit))
  if (params?.skip != null) url.searchParams.set("skip", String(params.skip))
  if (params?.hsk_level != null) url.searchParams.set("hsk_level", String(params.hsk_level))

  const res = await fetch(url.toString(), { next: { revalidate: 60 } })
  if (!res.ok) throw new Error(`Failed to fetch articles: ${res.status}`)
  return res.json()
}

export async function getArticle(id: number): Promise<Article> {
  const res = await fetch(`${API_BASE}/api/articles/${id}`, { next: { revalidate: 60 } })
  if (!res.ok) throw new Error(`Failed to fetch article ${id}: ${res.status}`)
  return res.json()
}

export interface TranslationResponse {
  found: boolean
  simplified?: string
  traditional?: string
  pinyin?: string
  definitions?: string[]
  hsk_level?: number | null
}

export async function getTranslation(word: string): Promise<TranslationResponse> {
  const res = await fetch(`${API_BASE}/api/dictionary/${encodeURIComponent(word)}`)
  if (!res.ok) throw new Error(`Translation lookup failed: ${res.status}`)
  return res.json()
}

// Server-side cached versions: deduplicate identical calls within a single request
export const getCachedArticles = cache(getArticles)
export const getCachedArticle = cache(getArticle)
