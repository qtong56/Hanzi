import { NavHeader } from "@/components/nav-header"
import { ReadingPassageList } from "@/components/reading-passage-list"
import { dehydrate, HydrationBoundary, QueryClient } from "@tanstack/react-query"
import { getCachedArticles } from "@/lib/api"

export default async function ReadingPage() {
  const queryClient = new QueryClient()
  await queryClient.prefetchQuery({
    queryKey: ["articles"],
    queryFn: () => getCachedArticles({ limit: 100 }),
  })

  return (
    <div className="min-h-screen">
      <NavHeader />

      <div className="container mx-auto max-w-7xl px-4 sm:px-6 py-8 sm:py-12">
        <div className="mb-8 sm:mb-12">
          <h1 className="mb-4 text-3xl sm:text-4xl font-bold">{"Reading Passages"}</h1>
          <p className="text-base sm:text-lg text-muted-foreground leading-relaxed">
            {"Choose a passage based on your level. Click any character to see translations and learn as you read."}
          </p>
        </div>

        <HydrationBoundary state={dehydrate(queryClient)}>
          <ReadingPassageList />
        </HydrationBoundary>
      </div>
    </div>
  )
}
