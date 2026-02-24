import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { NavHeader } from "@/components/nav-header"
import { BookOpen, Sparkles, TrendingUp, Globe } from "lucide-react"

export default function HomePage() {
  return (
    <div className="min-h-screen">
      <NavHeader />

      {/* Hero Section */}
      <section className="container mx-auto max-w-7xl px-4 sm:px-6 py-16 sm:py-24 md:py-32">
        <div className="mx-auto max-w-4xl text-center">
          <h1 className="mb-6 text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold leading-tight tracking-tight text-balance">
            {"Become literate "}
            <span className="text-accent">{"beyond ABC level"}</span>
          </h1>

          <p className="mb-10 text-base sm:text-lg md:text-xl lg:text-2xl text-muted-foreground text-pretty leading-relaxed px-4">
            {
              "Master Chinese reading through authentic passages. Click any character to see translations and build fluency naturally."
            }
          </p>

          <div className="flex flex-col items-center justify-center gap-4 sm:flex-row px-4">
            <Button size="lg" className="text-base w-full sm:w-auto" asChild>
              <Link href="/reading">{"Start Reading"}</Link>
            </Button>
            <Button size="lg" variant="outline" className="text-base bg-transparent w-full sm:w-auto">
              {"Learn More"}
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="border-t border-border bg-muted/30 py-12 sm:py-16 md:py-20">
        <div className="container mx-auto max-w-7xl px-4 sm:px-6">
          <div className="mx-auto max-w-6xl">
            <h2 className="mb-8 sm:mb-12 text-center text-2xl sm:text-3xl md:text-4xl font-bold">{"How it works"}</h2>

            <div className="grid gap-6 sm:gap-8 md:grid-cols-3">
              <Card className="p-6 sm:p-8">
                <div className="mb-4 flex h-12 w-12 sm:h-14 sm:w-14 items-center justify-center rounded-lg bg-accent/10">
                  <BookOpen className="h-6 w-6 sm:h-7 sm:w-7 text-accent" />
                </div>
                <h3 className="mb-3 text-lg sm:text-xl font-semibold">{"Choose Your Level"}</h3>
                <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
                  {"Select from HSK 1-6 passages tailored to your proficiency. Start comfortable, progress naturally."}
                </p>
              </Card>

              <Card className="p-6 sm:p-8">
                <div className="mb-4 flex h-12 w-12 sm:h-14 sm:w-14 items-center justify-center rounded-lg bg-accent/10">
                  <Globe className="h-6 w-6 sm:h-7 sm:w-7 text-accent" />
                </div>
                <h3 className="mb-3 text-lg sm:text-xl font-semibold">{"Click to Translate"}</h3>
                <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
                  {"Tap any character or word for instant translations and pinyin. Learn in context as you read."}
                </p>
              </Card>

              <Card className="p-6 sm:p-8">
                <div className="mb-4 flex h-12 w-12 sm:h-14 sm:w-14 items-center justify-center rounded-lg bg-accent/10">
                  <TrendingUp className="h-6 w-6 sm:h-7 sm:w-7 text-accent" />
                </div>
                <h3 className="mb-3 text-lg sm:text-xl font-semibold">{"Track Progress"}</h3>
                <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
                  {"Monitor your reading speed, vocabulary growth, and comprehension as you advance through levels."}
                </p>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto max-w-7xl px-4 sm:px-6 py-12 sm:py-16 md:py-20">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="mb-6 text-2xl sm:text-3xl md:text-4xl font-bold text-balance">
            {"Ready to improve your Chinese reading?"}
          </h2>
          <p className="mb-8 text-base sm:text-lg text-muted-foreground leading-relaxed px-4">
            {"Join thousands of learners mastering Chinese through authentic reading practice."}
          </p>
          <Button size="lg" asChild className="w-full sm:w-auto">
            <Link href="/reading">{"Browse Reading Passages"}</Link>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8 sm:py-12">
        <div className="container mx-auto max-w-7xl px-4 sm:px-6">
          <div className="flex flex-col items-center justify-between gap-4 sm:gap-6 md:flex-row">
            <div className="flex items-center gap-2">
              <BookOpen className="h-5 w-5 text-accent" />
              <span className="font-semibold">Hanzi</span>
            </div>
            <p className="text-xs sm:text-sm text-muted-foreground">{"© 2025 Hanzi. All rights reserved."}</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
