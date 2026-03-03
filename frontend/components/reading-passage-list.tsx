"use client"

import { useState } from "react"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { useQuery } from "@tanstack/react-query"
import { getArticles, HSK_LEVEL_COLORS } from "@/lib/api"
import { HskBar } from "@/components/hsk-bar"
import { ChevronLeft, ChevronRight } from "lucide-react"

const PAGE_SIZE = 20
const HSK_LEVELS = [1, 2, 3, 4, 5, 6, 7]

function ArticleListSkeleton() {
  return (
    <div className="space-y-8 sm:space-y-12">
      {[1, 2, 3].map((level) => (
        <div key={level}>
          <div className="mb-4 sm:mb-6 h-8 w-24 rounded bg-muted animate-pulse" />
          <div className="grid gap-4 sm:gap-6 md:grid-cols-2 lg:grid-cols-3">
            {[1, 2].map((i) => (
              <div key={i} className="h-40 rounded-lg bg-muted animate-pulse" />
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

export function ReadingPassageList() {
  const [hskFilter, setHskFilter] = useState<number | null>(null)
  const [page, setPage] = useState(1)

  const skip = (page - 1) * PAGE_SIZE

  const { data, isLoading, isError } = useQuery({
    queryKey: ["articles", { hsk_level: hskFilter, skip }],
    queryFn: () => getArticles({ limit: PAGE_SIZE, skip, hsk_level: hskFilter ?? undefined }),
  })

  const articles = data?.articles ?? []
  const total = data?.total ?? 0
  const totalPages = Math.ceil(total / PAGE_SIZE)

  function handleHskFilter(level: number | null) {
    setHskFilter(level)
    setPage(1)
  }

  const levels = hskFilter ? [hskFilter] : HSK_LEVELS

  return (
    <div className="space-y-6">
      {/* HSK Filter */}
      <div className="flex flex-wrap gap-2">
        <Button
          variant={hskFilter === null ? "default" : "outline"}
          size="sm"
          onClick={() => handleHskFilter(null)}
        >
          {"All Levels"}
        </Button>
        {HSK_LEVELS.map((level) => (
          <Button
            key={level}
            variant={hskFilter === level ? "default" : "outline"}
            size="sm"
            className={hskFilter === level ? "" : HSK_LEVEL_COLORS[level]}
            onClick={() => handleHskFilter(level)}
          >
            {`HSK ${level}`}
          </Button>
        ))}
      </div>

      {/* Article Grid */}
      {isLoading ? (
        <ArticleListSkeleton />
      ) : isError ? (
        <p className="text-destructive">{"Unable to connect to server. Please try again."}</p>
      ) : (
        <div className="space-y-8 sm:space-y-12">
          {levels.map((level) => {
            const levelArticles = articles.filter((a) => a.hsk_level === level)
            if (levelArticles.length === 0) return null

            return (
              <div key={level}>
                <h2 className="mb-4 sm:mb-6 text-xl sm:text-2xl font-bold">{`HSK ${level}`}</h2>
                <div className="grid gap-4 sm:gap-6 md:grid-cols-2 lg:grid-cols-3">
                  {levelArticles.map((article) => (
                    <Link key={article.id} href={`/reading/${article.id}`}>
                      <Card className="h-full transition-all hover:shadow-lg hover:border-accent">
                        <CardHeader className="p-4 sm:p-6">
                          <div className="mb-3 flex items-start justify-between gap-2">
                            <div className="font-serif text-xl sm:text-2xl font-semibold">{article.title}</div>
                            <HskBar counts={article.hsk_level_counts} hskLevel={article.hsk_level} compact />
                          </div>
                          <CardTitle className="text-base sm:text-lg text-muted-foreground font-normal">
                            {article.word_count != null ? `${article.word_count} words` : ""}
                          </CardTitle>
                        </CardHeader>
                        {article.summary && (
                          <CardContent className="p-4 sm:p-6 pt-0 sm:pt-0">
                            <CardDescription className="text-sm sm:text-base leading-relaxed line-clamp-3">
                              {article.summary}
                            </CardDescription>
                          </CardContent>
                        )}
                      </Card>
                    </Link>
                  ))}
                </div>
              </div>
            )
          })}

          {articles.length === 0 && (
            <p className="text-muted-foreground">
              {"No articles found. Load sample data to get started."}
            </p>
          )}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between pt-4">
          <p className="text-sm text-muted-foreground">
            {`Page ${page} of ${totalPages} (${total} articles)`}
          </p>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
            >
              <ChevronLeft className="h-4 w-4 mr-1" />
              {"Previous"}
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
            >
              {"Next"}
              <ChevronRight className="h-4 w-4 ml-1" />
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
