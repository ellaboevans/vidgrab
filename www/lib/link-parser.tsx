import React from "react";

/**
 * Detects URLs in text and converts them to clickable links
 * Supports http://, https://, and www. URLs
 */
export function parseLinksInText(text: string): React.ReactNode[] {
  // Regex pattern to match URLs
  const urlRegex =
    /(https?:\/\/[^\s]+|www\.[^\s]+|github\.com\/[^\s]+)/g;

  const parts: React.ReactNode[] = [];
  let lastIndex = 0;

  const matches = Array.from(text.matchAll(urlRegex));

  matches.forEach((match) => {
    // Add text before the URL
    if (match.index > lastIndex) {
      parts.push(text.substring(lastIndex, match.index));
    }

    // Add the URL as a clickable link
    let url = match[0];
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
      url = "https://" + url;
    }

    parts.push(
      <a
        key={`link-${match.index}`}
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-primary hover:text-primary/80 underline font-semibold transition-colors"
      >
        {match[0]}
      </a>
    );

    lastIndex = match.index + match[0].length;
  });

  // Add remaining text
  if (lastIndex < text.length) {
    parts.push(text.substring(lastIndex));
  }

  return parts.length > 0 ? parts : [text];
}
