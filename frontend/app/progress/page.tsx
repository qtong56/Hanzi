import { NavHeader } from "@/components/nav-header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, BookOpen, Clock } from "lucide-react"

export default function ProgressPage() {
  return (
    <div className="min-h-screen">
      <NavHeader />

      <div className="container px-4 py-12 sm:px-6">
        <div className="mx-auto max-w-4xl">
          <h1 className="mb-6 text-4xl font-bold">{"Your Progress"}</h1>
          <p className="mb-8 text-lg text-muted-foreground">
            {"Track your learning journey and see how far you've come"}
          </p>

          <div className="grid gap-6 md:grid-cols-3">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BookOpen className="h-5 w-5 text-accent" />
                  {"Passages Read"}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold">24</p>
                <CardDescription className="mt-2">{"Across all levels"}</CardDescription>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-accent" />
                  {"Current Level"}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold">{"HSK 3"}</p>
                <CardDescription className="mt-2">{"Keep going!"}</CardDescription>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="h-5 w-5 text-accent" />
                  {"Study Time"}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold">{"12h"}</p>
                <CardDescription className="mt-2">{"This month"}</CardDescription>
              </CardContent>
            </Card>
          </div>

          <Card className="mt-6">
            <CardHeader>
              <CardTitle>{"Recent Activity"}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">{"Your reading history and vocabulary growth will appear here."}</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
