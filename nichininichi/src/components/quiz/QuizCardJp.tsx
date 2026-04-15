import type { WordEntry } from '../../types';
import styles from './QuizCardJp.module.css';

interface QuizCardJpProps {
  word: WordEntry;
  state: 'default' | 'selected' | 'correct' | 'dimmed' | 'matched';
  onSelect: () => void;
}

export function QuizCardJp({ word, state, onSelect }: QuizCardJpProps) {
  if (state === 'matched') return null;

  return (
    <button
      className={`${styles.card} ${styles[state]}`}
      onClick={onSelect}
      aria-pressed={state === 'selected'}
      aria-label={`Japanese word: ${word.kanji || word.reading}, ${word.reading}`}
    >
      <span className={styles.kanji} lang="ja">
        {word.kanji || word.reading}
      </span>
      {word.kanji && (
        <span className={styles.reading} lang="ja">
          {word.reading}
        </span>
      )}
    </button>
  );
}
