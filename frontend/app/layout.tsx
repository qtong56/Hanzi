import type React from "react"
import type { Metadata } from "next"
import { Inter, Noto_Serif_SC } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import { Providers } from "@/components/providers"
import "./globals.css"

const _inter = Inter({ subsets: ["latin"] })
const _notoSerifSC = Noto_Serif_SC({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
})

export const metadata: Metadata = {
  title: "Hanzi - Improve Your Chinese Reading Skills",
  description:
    "Learn Chinese through interactive reading passages at all levels. Click to translate and learn as you read.",
  generator: "v0.app",
  icons: {
    icon: [
      {
        url: "/icon-light-32x32.png",
        media: "(prefers-color-scheme: light)",
      },
      {
        url: "icons8-open-book-ios-17-outlined-32.png",
        media: "(prefers-color-scheme: dark)",
      },
      {
        url: "/icons8-open-book-ios-17-outlined-32.png",
        type: "image/svg+xml",
      },
    ],
    apple: "/apple-icon.png",
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`font-sans antialiased`}>
        <Providers>
          {children}
        </Providers>
        <Analytics />
      </body>
    </html>
  )
}
