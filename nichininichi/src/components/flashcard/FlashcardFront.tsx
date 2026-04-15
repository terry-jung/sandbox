import type { WordEntry } from '../../types';
import styles from './FlashcardFront.module.css';

interface FlashcardFrontProps {
  word: WordEntry;
}

function renderFurigana(kanji: string, reading: string) {
  // For compound words, we show the full reading as furigana over the kanji
  return (
    <ruby>
      {kanji}
      <rt>{reading}</rt>
    </ruby>
  );
}

export function FlashcardFront({ word }: FlashcardFrontProps) {
  return (
    <div className={styles.front} lang="ja">
      <div className={styles.kanji}>
        {word.kanji ? renderFurigana(word.kanji, word.reading) : word.reading}
      </div>
      <p className={styles.hint}>Tap to reveal</p>
    </div>
  );
}
