"use client"

import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { Card } from "@/components/ui/card"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Loader2 } from "lucide-react"
import type { Segment, TranslationResponse } from "@/lib/api"
import { getTranslation } from "@/lib/api"

const PUNCTUATION = /^[\s，。！？、；：""''（）《》\n]+$/

function findSentence(text: string, charIndex: number): string {
  const sentenceEnders = /[。！？]/
  let start = 0
  let end = text.length

  for (let i = charIndex - 1; i >= 0; i--) {
    if (sentenceEnders.test(text[i])) {
      start = i + 1
      break
    }
  }
  for (let i = charIndex; i < text.length; i++) {
    if (sentenceEnders.test(text[i])) {
      end = i + 1
      break
    }
  }

  return text.slice(start, end).trim()
}

function TranslationContent({ translation }: { translation: TranslationResponse }) {
  if (!translation.found) {
    return (
      <p className="text-sm text-muted-foreground italic">
        {"Translation not available for this word"}
      </p>
    )
  }
  return (
    <div className="space-y-1.5">
      {translation.hsk_level != null && (
        <p className="text-xs font-medium text-muted-foreground">{`HSK ${translation.hsk_level}`}</p>
      )}
      {translation.definitions?.slice(0, 3).map((def, i) => (
        <p key={i} className="text-sm leading-snug">
          <span className="text-muted-foreground mr-1">{i + 1}.</span>
          {def}
        </p>
      ))}
    </div>
  )
}

interface WordPopoverProps {
  segment: Segment
  text: string
}

function WordPopover({ segment, text }: WordPopoverProps) {
  const [open, setOpen] = useState(false)

  const { data: translation, isLoading, isError } = useQuery<TranslationResponse>({
    queryKey: ["translation", segment.text],
    queryFn: () => getTranslation(segment.text),
    enabled: open,
    staleTime: Infinity,  // cache translations forever — dictionary doesn't change
    gcTime: Infinity,
  })

  const sentence = findSentence(text, segment.start)

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <span className="cursor-pointer transition-colors hover:text-accent hover:bg-accent/10 rounded px-0.5">
          {segment.text}
        </span>
      </PopoverTrigger>
      <PopoverContent
        className="w-[calc(100vw-2rem)] max-w-[320px] sm:max-w-100 mx-4"
        align="center"
        side="top"
        sideOffset={8}
      >
        <div className="space-y-3">
          <div className="flex items-baseline gap-3">
            <p className="text-2xl sm:text-3xl font-serif font-bold">{segment.text}</p>
            <p className="text-base sm:text-lg text-muted-foreground">{segment.pinyin}</p>
          </div>

          <div>
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1.5">
              {"Meaning"}
            </p>
            {isLoading ? (
              <div className="flex items-center gap-2 text-muted-foreground">
                <Loader2 className="h-3 w-3 animate-spin" />
                <span className="text-sm">{"Looking up..."}</span>
              </div>
            ) : isError ? (
              <p className="text-sm text-destructive">{"Unable to connect to server"}</p>
            ) : translation ? (
              <TranslationContent translation={translation} />
            ) : null}
          </div>

          <div className="pt-2 border-t border-border">
            <div className="flex items-center justify-between mb-1">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                {"Sentence"}
              </p>
              <a
                href={`https://translate.google.com/?sl=zh-CN&tl=en&text=${encodeURIComponent(sentence)}&op=translate`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-muted-foreground hover:text-foreground underline underline-offset-2"
              >
                {"Translate →"}
              </a>
            </div>
            <p className="text-sm sm:text-base font-serif wrap-break-word">{sentence}</p>
          </div>
        </div>
      </PopoverContent>
    </Popover>
  )
}

// Build a flat render list: interleave segments with any gap text between them
function buildRenderList(text: string, segments: Segment[]): Array<Segment | { type: "plain"; text: string }> {
  const items: Array<Segment | { type: "plain"; text: string }> = []
  let pos = 0

  for (const seg of segments) {
    if (seg.start > pos) {
      items.push({ type: "plain", text: text.slice(pos, seg.start) })
    }
    items.push(seg)
    pos = seg.end
  }

  if (pos < text.length) {
    items.push({ type: "plain", text: text.slice(pos) })
  }

  return items
}

export function InteractivePassage({ text, segments }: { text: string; segments: Segment[] }) {
  const items = buildRenderList(text, segments)

  return (
    <Card className="p-4 sm:p-6 md:p-8">
      <div className="font-serif text-base sm:text-lg md:text-2xl leading-relaxed sm:leading-loose">
        {items.map((item, index) => {
          if ("type" in item) {
            return (
              <span key={index} className="text-muted-foreground">
                {item.text}
              </span>
            )
          }

          if (PUNCTUATION.test(item.text)) {
            return (
              <span key={index} className="text-muted-foreground">
                {item.text}
              </span>
            )
          }

          return <WordPopover key={index} segment={item} text={text} />
        })}
      </div>
    </Card>
  )
}
