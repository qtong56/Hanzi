"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { BookOpen, Menu } from "lucide-react"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"

export function NavHeader() {
  const [open, setOpen] = useState(false)

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto max-w-7xl flex h-16 items-center justify-between px-4 sm:px-6">
        <Link href="/" className="flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent">
            <BookOpen className="h-5 w-5 text-accent-foreground" />
          </div>
          <span className="text-xl font-semibold">Hanzi</span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-8">
          <Link href="/" className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground">
            Home
          </Link>
          <Link
            href="/reading"
            className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
          >
            Reading
          </Link>
          <Link
            href="/about"
            className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
          >
            About
          </Link>
          <Link
            href="/progress"
            className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
          >
            Progress
          </Link>
        </nav>

        {/* Mobile Navigation */}
        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger asChild className="md:hidden">
            <Button variant="ghost" size="icon">
              <Menu className="h-6 w-6" />
              <span className="sr-only">Toggle menu</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="right" className="w-[280px] sm:w-[350px] px-6">
            <nav className="flex flex-col gap-6 mt-8">
              <Link
                href="/"
                className="text-base font-medium transition-colors hover:text-accent py-2"
                onClick={() => setOpen(false)}
              >
                Home
              </Link>
              <Link
                href="/reading"
                className="text-base font-medium transition-colors hover:text-accent py-2"
                onClick={() => setOpen(false)}
              >
                Reading
              </Link>
              <Link
                href="/about"
                className="text-base font-medium transition-colors hover:text-accent py-2"
                onClick={() => setOpen(false)}
              >
                About
              </Link>
              <Link
                href="/progress"
                className="text-base font-medium transition-colors hover:text-accent py-2"
                onClick={() => setOpen(false)}
              >
                Progress
              </Link>
            </nav>
          </SheetContent>
        </Sheet>
      </div>
    </header>
  )
}
