import { NavHeader } from "@/components/nav-header"
import { Card } from "@/components/ui/card"

export default function AboutPage() {
  return (
    <div className="min-h-screen">
      <NavHeader />

      <div className="container px-4 py-12 sm:px-6">
        <div className="mx-auto max-w-3xl">
          <h1 className="mb-6 text-4xl font-bold">{"About Hanzi"}</h1>

          <div className="space-y-6">
            <Card className="p-6">
              <h2 className="mb-3 text-2xl font-semibold">{"Our Mission"}</h2>
              <p className="leading-relaxed text-muted-foreground">
                {
                  "Hanzi is designed to help ABC (American Born Chinese) learners and intermediate Chinese students improve their reading comprehension through authentic, interactive content. We believe that reading is the key to fluency, and our click-to-translate feature makes the learning process seamless and enjoyable."
                }
              </p>
            </Card>

            <Card className="p-6">
              <h2 className="mb-3 text-2xl font-semibold">{"Why Reading?"}</h2>
              <p className="leading-relaxed text-muted-foreground">
                {
                  "Reading in context is one of the most effective ways to learn a language. By engaging with authentic passages at your level, you build vocabulary naturally, understand grammar in context, and develop an intuitive feel for the language."
                }
              </p>
            </Card>

            <Card className="p-6">
              <h2 className="mb-3 text-2xl font-semibold">{"HSK Levels"}</h2>
              <p className="leading-relaxed text-muted-foreground">
                {
                  "All our passages are organized by HSK (Hanyu Shuiping Kaoshi) levels, the standardized Chinese proficiency test. From HSK 1 (beginner) to HSK 6 (advanced), you can progress at your own pace and track your improvement."
                }
              </p>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
