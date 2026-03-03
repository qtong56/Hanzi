"use client"

import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { HSK_BAR_COLORS, HSK_LEVEL_COLORS } from "@/lib/api"

const LEVELS = [1, 2, 3, 4, 5, 6, 7]
const BAR_MAX_HEIGHT = 36 // px

interface HskBarProps {
  counts: Record<string, number> | null
  /** The 80%-coverage level */
  hskLevel: number | null
  /** compact=true: show a badge with bars in a hover tooltip (list view).
   *  compact=false (default): show the full bar chart directly (article view). */
  compact?: boolean
}

function Bars({ counts, hskLevel }: { counts: Record<string, number>; hskLevel: number | null }) {
  const maxCount = Math.max(...LEVELS.map((l) => counts[String(l)] ?? 0), 1)

  return (
    <div className="flex items-end gap-0.5">
      {LEVELS.map((level) => {
        const count = counts[String(level)] ?? 0
        const height = count > 0 ? Math.max(4, Math.round((count / maxCount) * BAR_MAX_HEIGHT)) : 2
        const isCoverageLevel = hskLevel === level
        const barColor = count > 0 ? HSK_BAR_COLORS[level] : "bg-muted"

        return (
          <div key={level} className="flex flex-col items-center gap-0.5">
            <div
              className={`w-2.5 rounded-t-sm ${barColor} ${isCoverageLevel ? "ring-2 ring-primary ring-offset-1" : ""}`}
              style={{ height: `${height}px` }}
            />
            <span
              className={`text-[9px] leading-none font-mono tabular-nums ${
                isCoverageLevel ? "font-bold text-foreground" : "text-muted-foreground"
              }`}
            >
              {level}
            </span>
          </div>
        )
      })}
    </div>
  )
}

export function HskBar({ counts, hskLevel, compact = false }: HskBarProps) {
  if (!counts || Object.keys(counts).length === 0) {
    return <span className="text-xs text-muted-foreground">{"—"}</span>
  }

  if (compact) {
    const badgeColor =
      hskLevel != null
        ? HSK_LEVEL_COLORS[hskLevel] ?? "bg-gray-100 text-gray-800"
        : "bg-muted text-muted-foreground"

    return (
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <span className={`text-xs font-medium px-2 py-0.5 rounded-full cursor-default whitespace-nowrap ${badgeColor}`}>
              {hskLevel != null ? `HSK ${hskLevel}` : "—"}
            </span>
          </TooltipTrigger>
          <TooltipContent side="bottom" className="p-3">
            <Bars counts={counts} hskLevel={hskLevel} />
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    )
  }

  return (
    <TooltipProvider>
      {LEVELS.map((level) => {
        const count = counts[String(level)] ?? 0
        return (
          <Tooltip key={level}>
            <TooltipTrigger asChild>
              <span />
            </TooltipTrigger>
            <TooltipContent side="bottom">
              <p className="text-xs">{`HSK ${level}: ${count} word${count !== 1 ? "s" : ""}`}</p>
              {hskLevel === level && (
                <p className="text-xs text-muted-foreground">{"80% coverage level"}</p>
              )}
            </TooltipContent>
          </Tooltip>
        )
      })}
      <Bars counts={counts} hskLevel={hskLevel} />
    </TooltipProvider>
  )
}
