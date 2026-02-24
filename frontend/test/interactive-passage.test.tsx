import { describe, it, expect, vi, beforeEach } from "vitest"
import { screen, waitFor, within } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { InteractivePassage } from "@/components/interactive-passage"
import { renderWithQuery, makeArticle } from "./helpers"

vi.mock("@/lib/api", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/api")>()
  return {
    ...actual,
    getTranslation: vi.fn(),
  }
})

import { getTranslation } from "@/lib/api"
const mockGetTranslation = vi.mocked(getTranslation)

const ARTICLE = makeArticle()

beforeEach(() => {
  vi.clearAllMocks()
})

describe("InteractivePassage", () => {
  it("renders word segments as clickable spans", () => {
    renderWithQuery(
      <InteractivePassage text={ARTICLE.text} segments={ARTICLE.segments!} />
    )
    expect(screen.getByText("中国")).toBeInTheDocument()
    expect(screen.getByText("国家")).toBeInTheDocument()
  })

  it("renders punctuation without click interaction (no cursor-pointer)", () => {
    renderWithQuery(
      <InteractivePassage text={ARTICLE.text} segments={ARTICLE.segments!} />
    )
    // Punctuation span should not have cursor-pointer class
    const punct = screen.getByText("。")
    expect(punct).not.toHaveClass("cursor-pointer")
  })

  it("opens popover and shows pinyin on word click", async () => {
    const user = userEvent.setup()
    mockGetTranslation.mockReturnValue(new Promise(() => {})) // stay loading

    renderWithQuery(
      <InteractivePassage text={ARTICLE.text} segments={ARTICLE.segments!} />
    )

    await user.click(screen.getByText("中国"))

    await waitFor(() => {
      // Pinyin from segment should appear immediately
      expect(screen.getByText("zhōng guó")).toBeInTheDocument()
    })
  })

  it("shows loading spinner while translation fetches", async () => {
    const user = userEvent.setup()
    mockGetTranslation.mockReturnValue(new Promise(() => {})) // never resolves

    renderWithQuery(
      <InteractivePassage text={ARTICLE.text} segments={ARTICLE.segments!} />
    )

    await user.click(screen.getByText("中国"))

    await waitFor(() => {
      expect(screen.getByText(/looking up/i)).toBeInTheDocument()
    })
  })

  it("shows translation definitions when found", async () => {
    const user = userEvent.setup()
    mockGetTranslation.mockResolvedValue({
      found: true,
      simplified: "中国",
      pinyin: "Zhong1 guo2",
      definitions: ["China", "Middle Kingdom"],
    })

    renderWithQuery(
      <InteractivePassage text={ARTICLE.text} segments={ARTICLE.segments!} />
    )

    await user.click(screen.getByText("中国"))

    await waitFor(() => {
      expect(screen.getByText("China")).toBeInTheDocument()
      expect(screen.getByText("Middle Kingdom")).toBeInTheDocument()
    })
  })

  it("shows not-available message when word not in dictionary", async () => {
    const user = userEvent.setup()
    mockGetTranslation.mockResolvedValue({ found: false })

    renderWithQuery(
      <InteractivePassage text={ARTICLE.text} segments={ARTICLE.segments!} />
    )

    await user.click(screen.getByText("中国"))

    await waitFor(() => {
      expect(screen.getByText(/translation not available/i)).toBeInTheDocument()
    })
  })

  it("shows error message when API call fails", async () => {
    const user = userEvent.setup()
    mockGetTranslation.mockRejectedValue(new Error("Network error"))

    renderWithQuery(
      <InteractivePassage text={ARTICLE.text} segments={ARTICLE.segments!} />
    )

    await user.click(screen.getByText("中国"))

    await waitFor(() => {
      expect(screen.getByText(/unable to connect to server/i)).toBeInTheDocument()
    })
  })

  it("can open popovers for multiple words in sequence", async () => {
    const user = userEvent.setup()
    mockGetTranslation.mockResolvedValue({
      found: true,
      simplified: "国家",
      definitions: ["country", "nation"],
    })

    renderWithQuery(
      <InteractivePassage text={ARTICLE.text} segments={ARTICLE.segments!} />
    )

    await user.click(screen.getByText("中国"))
    await user.click(screen.getByText("国家"))

    await waitFor(() => {
      expect(screen.getByText("country")).toBeInTheDocument()
    })
  })

  it("shows the sentence context in the popover", async () => {
    const user = userEvent.setup()
    mockGetTranslation.mockReturnValue(new Promise(() => {}))

    renderWithQuery(
      <InteractivePassage text={ARTICLE.text} segments={ARTICLE.segments!} />
    )

    await user.click(screen.getByText("中国"))

    await waitFor(() => {
      // The full sentence should appear in the popover
      expect(screen.getByText("中国是一个国家。")).toBeInTheDocument()
    })
  })
})
