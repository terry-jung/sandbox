import type { WordEntry } from '../../types';
import { LangBadge } from '../shared/LangBadge';
import styles from './QuizCardTrans.module.css';

interface QuizCardTransProps {
  word: WordEntry;
  state: 'default' | 'selected' | 'correct' | 'incorrect' | 'reveal' | 'matched';
  onSelect: () => void;
}

export function QuizCardTrans({ word, state, onSelect }: QuizCardTransProps) {
  if (state === 'matched') return null;

  return (
    <button
      className={`${styles.card} ${styles[state]}`}
      onClick={onSelect}
      aria-label={`Translation: English ${word.translations.en}, Italian ${word.translations.it}, Korean ${word.translations.ko}`}
    >
      <div className={styles.row}>
        <LangBadge lang="en" />
        <span lang="en" className={styles.text}>{word.translations.en}</span>
      </div>
      <div className={styles.row}>
        <LangBadge lang="it" />
        <span lang="it" className={styles.text}>{word.translations.it}</span>
      </div>
      <div className={styles.row}>
        <LangBadge lang="ko" />
        <span lang="ko" className={styles.text}>{word.translations.ko}</span>
      </div>
    </button>
  );
}
