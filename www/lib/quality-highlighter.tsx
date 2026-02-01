import React from "react";

const QUALITY_OPTIONS = ["best", "1080p", "720p", "480p", "audio-only"];

/**
 * Detects quality options in text and highlights them as styled badges
 */
export function highlightQualityOptions(text: string): React.ReactNode[] {
  // Create regex pattern that matches whole words only
  const pattern = new RegExp(
    String.raw`\b(${QUALITY_OPTIONS.join("|")})\b`,
    "gi",
  );

  const parts: React.ReactNode[] = [];
  let lastIndex = 0;

  const matches = Array.from(text.matchAll(pattern));

  matches.forEach((match) => {
    // Add text before the match
    if (match.index > lastIndex) {
      parts.push(text.substring(lastIndex, match.index));
    }

    // Add the quality option as a styled badge
    parts.push(
      <span
        key={`quality-${match.index}`}
        className="inline-block px-2 py-0.5 bg-primary/20 text-primary font-semibold rounded-md text-sm hover:bg-primary/30 transition-colors">
        {match[0]}
      </span>,
    );

    lastIndex = match.index + match[0].length;
  });

  // Add remaining text
  if (lastIndex < text.length) {
    parts.push(text.substring(lastIndex));
  }

  return parts.length > 0 ? parts : [text];
}
