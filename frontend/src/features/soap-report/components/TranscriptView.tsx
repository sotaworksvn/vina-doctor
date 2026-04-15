"use client";

import type { TranscriptTurn } from "@/shared/types/api";

/** Maps well-known speaker labels to Tailwind colour classes. */
function speakerStyle(speaker: string): { badge: string; bubble: string } {
  const key = speaker.toLowerCase();
  if (key === "doctor")
    return {
      badge: "bg-primary-container/20 text-primary-container",
      bubble: "bg-surface-lowest border border-primary-container/20",
    };
  if (key === "patient")
    return {
      badge: "bg-tertiary-container/20 text-on-tertiary-container",
      bubble: "bg-surface-lowest border border-tertiary-container/20",
    };
  if (key === "caregiver")
    return {
      badge: "bg-secondary-container/20 text-on-secondary-container",
      bubble: "bg-surface-lowest border border-secondary-container/20",
    };
  // Fallback for any other label
  return {
    badge: "bg-surface-high text-on-surface-variant",
    bubble: "bg-surface-lowest border border-outline-variant/20",
  };
}

export function TranscriptView({ turns }: { turns: TranscriptTurn[] }) {
  if (!turns || turns.length === 0) return null;

  return (
    <div className="flex flex-col gap-3">
      <h2 className="font-display text-base font-bold text-on-surface">
        Transcript
      </h2>
      <div className="flex flex-col gap-2">
        {turns.map((turn, idx) => {
          const { badge, bubble } = speakerStyle(turn.speaker);
          return (
            <div
              key={idx}
              className={`rounded-2xl px-4 py-3 ${bubble}`}
            >
              <div className="mb-1 flex items-center gap-2">
                <span
                  className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${badge}`}
                >
                  {turn.speaker}
                </span>
                {turn.timestamp && (
                  <span className="text-xs text-on-surface-variant">
                    {turn.timestamp}
                  </span>
                )}
              </div>
              <p className="whitespace-pre-wrap text-sm leading-relaxed text-on-surface">
                {turn.text}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
