import { NavHeader } from "@/components/nav-header"
import { ArticleView } from "@/components/article-view"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { ArrowLeft } from "lucide-react"
import { notFound } from "next/navigation"
import { dehydrate, HydrationBoundary, QueryClient } from "@tanstack/react-query"
import { getCachedArticle } from "@/lib/api"

export default async function PassagePage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const articleId = Number(id)

  if (isNaN(articleId)) {
    notFound()
  }

  const queryClient = new QueryClient()

  try {
    await queryClient.prefetchQuery({
      queryKey: ["articles", articleId],
      queryFn: () => getCachedArticle(articleId),
    })
  } catch {
    notFound()
  }

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <div className="min-h-screen">
        <NavHeader />
        <div className="container mx-auto max-w-4xl px-4 sm:px-6 py-8 sm:py-12">
          <Link href="/reading">
            <Button variant="ghost" className="mb-6">
              <ArrowLeft className="mr-2 h-4 w-4" />
              {"Back to Reading"}
            </Button>
          </Link>

          <ArticleView articleId={articleId} />
        </div>
      </div>
    </HydrationBoundary>
  )
}
