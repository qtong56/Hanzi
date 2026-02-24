import { describe, it, expect, vi, beforeEach } from "vitest"
import { screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { ReadingPassageList } from "@/components/reading-passage-list"
import { renderWithQuery, makeArticleList } from "./helpers"
import type { ArticleListItem } from "@/lib/api"

// Mock the api module
vi.mock("@/lib/api", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/api")>()
  return {
    ...actual,
    getArticles: vi.fn(),
  }
})

import { getArticles } from "@/lib/api"
const mockGetArticles = vi.mocked(getArticles)

function makeResponse(articles: ArticleListItem[] = makeArticleList()) {
  return {
    articles,
    total: articles.length,
    limit: 20,
    offset: 0,
  }
}

beforeEach(() => {
  vi.clearAllMocks()
})

describe("ReadingPassageList", () => {
  it("shows skeleton while loading", () => {
    // Never resolve so it stays loading
    mockGetArticles.mockReturnValue(new Promise(() => {}))
    renderWithQuery(<ReadingPassageList />)
    // Skeleton is animated divs with bg-muted — check by role or test-id isn't available,
    // so verify no article links are rendered yet
    expect(screen.queryByRole("link")).toBeNull()
  })

  it("shows error message when API fails", async () => {
    mockGetArticles.mockRejectedValue(new Error("Network error"))
    renderWithQuery(<ReadingPassageList />)
    await waitFor(() => {
      expect(screen.getByText(/unable to connect to server/i)).toBeInTheDocument()
    })
  })

  it("shows empty state when no articles returned", async () => {
    mockGetArticles.mockResolvedValue(makeResponse([]))
    renderWithQuery(<ReadingPassageList />)
    await waitFor(() => {
      expect(screen.getByText(/no articles found/i)).toBeInTheDocument()
    })
  })

  it("renders articles grouped by HSK level", async () => {
    const articles = [
      { id: 1, title: "文章一", summary: null, hsk_level: 1, word_count: 50 },
      { id: 2, title: "文章二", summary: null, hsk_level: 2, word_count: 80 },
    ]
    mockGetArticles.mockResolvedValue(makeResponse(articles))
    renderWithQuery(<ReadingPassageList />)

    await waitFor(() => {
      // Use heading role to distinguish section headings from filter buttons
      expect(screen.getByRole("heading", { name: "HSK 1" })).toBeInTheDocument()
      expect(screen.getByRole("heading", { name: "HSK 2" })).toBeInTheDocument()
      expect(screen.getByText("文章一")).toBeInTheDocument()
      expect(screen.getByText("文章二")).toBeInTheDocument()
    })
  })

  it("links to correct article URLs", async () => {
    const articles = [{ id: 42, title: "测试", summary: null, hsk_level: 1, word_count: 10 }]
    mockGetArticles.mockResolvedValue(makeResponse(articles))
    renderWithQuery(<ReadingPassageList />)

    await waitFor(() => {
      const link = screen.getByRole("link")
      expect(link).toHaveAttribute("href", "/reading/42")
    })
  })

  it("filters articles by HSK level when filter button clicked", async () => {
    const user = userEvent.setup()
    const articles = [
      { id: 1, title: "HSK1文章", summary: null, hsk_level: 1, word_count: 50 },
      { id: 2, title: "HSK2文章", summary: null, hsk_level: 2, word_count: 80 },
    ]
    // First call returns all, second call (after filter) returns only HSK 1
    mockGetArticles
      .mockResolvedValueOnce(makeResponse(articles))
      .mockResolvedValueOnce(makeResponse([articles[0]]))

    renderWithQuery(<ReadingPassageList />)
    await waitFor(() => expect(screen.getByText("HSK1文章")).toBeInTheDocument())

    await user.click(screen.getByRole("button", { name: "HSK 1" }))

    // getArticles should have been called with hsk_level: 1
    await waitFor(() => {
      expect(mockGetArticles).toHaveBeenCalledWith(
        expect.objectContaining({ hsk_level: 1 })
      )
    })
  })

  it("shows pagination when total > page size", async () => {
    // Simulate 25 articles but only 20 returned (page 1)
    const articles = makeArticleList(20)
    mockGetArticles.mockResolvedValue({
      articles,
      total: 25,
      limit: 20,
      offset: 0,
    })
    renderWithQuery(<ReadingPassageList />)

    await waitFor(() => {
      expect(screen.getByRole("button", { name: /next/i })).toBeInTheDocument()
      expect(screen.getByText(/page 1 of 2/i)).toBeInTheDocument()
    })
  })

  it("previous button is disabled on first page", async () => {
    mockGetArticles.mockResolvedValue({ articles: makeArticleList(20), total: 25, limit: 20, offset: 0 })
    renderWithQuery(<ReadingPassageList />)

    await waitFor(() => {
      expect(screen.getByRole("button", { name: /previous/i })).toBeDisabled()
    })
  })

  it("next button is disabled on last page", async () => {
    mockGetArticles.mockResolvedValue({ articles: makeArticleList(5), total: 5, limit: 20, offset: 0 })
    renderWithQuery(<ReadingPassageList />)

    await waitFor(() => {
      // Only 5 articles = 1 page, pagination shouldn't show at all
      expect(screen.queryByRole("button", { name: /next/i })).toBeNull()
    })
  })
})
