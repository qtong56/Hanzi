"use client"

import { useQuery } from "@tanstack/react-query"
import { Badge } from "@/components/ui/badge"
import { Card } from "@/components/ui/card"
import { InteractivePassage } from "@/components/interactive-passage"
import { getArticle, hskLevelColor } from "@/lib/api"

function ReadingViewSkeleton() {
  return (
    <div className="animate-pulse space-y-6">
      <div className="space-y-3">
        <div className="h-10 w-2/3 rounded bg-muted" />
        <div className="h-4 w-24 rounded bg-muted" />
        <div className="h-4 w-48 rounded bg-muted" />
      </div>
      <Card className="p-4 sm:p-6 md:p-8 space-y-3">
        {[80, 95, 70, 88, 60, 92, 75].map((w, i) => (
          <div key={i} className="h-6 rounded bg-muted" style={{ width: `${w}%` }} />
        ))}
      </Card>
    </div>
  )
}

export function ArticleView({ articleId }: { articleId: number }) {
  const { data: article, isLoading, isError } = useQuery({
    queryKey: ["articles", articleId],
    queryFn: () => getArticle(articleId),
  })

  if (isLoading) return <ReadingViewSkeleton />

  if (isError || !article) {
    return (
      <p className="text-destructive">{"Unable to load article. Please try again."}</p>
    )
  }

  return (
    <>
      <div className="mb-6 sm:mb-8">
        <div className="mb-4 flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 sm:gap-4">
          <div>
            <h1 className="mb-2 font-serif text-2xl sm:text-4xl font-bold">{article.title}</h1>
            {article.word_count != null && (
              <p className="text-sm text-muted-foreground">{`${article.word_count} words`}</p>
            )}
          </div>
          {article.hsk_level != null && (
            <Badge className={hskLevelColor(article.hsk_level)} variant="secondary">
              {`HSK ${article.hsk_level}`}
            </Badge>
          )}
        </div>
        <p className="text-sm sm:text-base text-muted-foreground">
          {"Click any word to see its pinyin and meaning"}
        </p>
      </div>

      <InteractivePassage text={article.text} segments={article.segments ?? []} />
    </>
  )
}
