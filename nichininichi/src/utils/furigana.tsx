import React from 'react';

/**
 * Parses a furigana string and renders it as React elements with <ruby> tags.
 * Format: "{漢字|かんじ}の{例|れい}" — text outside braces is plain, inside braces is kanji|reading.
 * Falls back to plain text if no furigana markers are found.
 */
export function renderFurigana(text: string): React.ReactNode {
  if (!text.includes('{')) return text;

  const parts: React.ReactNode[] = [];
  const regex = /\{([^|]+)\|([^}]+)\}|([^{]+)/g;
  let match;
  let key = 0;

  while ((match = regex.exec(text)) !== null) {
    if (match[1] && match[2]) {
      // {kanji|reading}
      parts.push(
        <ruby key={key++}>
          {match[1]}
          <rt>{match[2]}</rt>
        </ruby>
      );
    } else if (match[3]) {
      // plain text
      parts.push(<span key={key++}>{match[3]}</span>);
    }
  }

  return <>{parts}</>;
}
