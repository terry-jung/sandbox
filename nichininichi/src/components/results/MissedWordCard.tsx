import type { WordEntry } from '../../types';
import { LangBadge } from '../shared/LangBadge';
import styles from './MissedWordCard.module.css';

interface MissedWordCardProps {
  word: WordEntry;
}

export function MissedWordCard({ word }: MissedWordCardProps) {
  return (
    <div className={styles.card}>
      <div className={styles.jpSide} lang="ja">
        <span className={styles.kanji}>{word.kanji || word.reading}</span>
        {word.kanji && <span className={styles.reading}>{word.reading}</span>}
      </div>
      <div className={styles.transSide}>
        <div className={styles.row}>
          <LangBadge lang="en" />
          <span lang="en">{word.translations.en}</span>
        </div>
        <div className={styles.row}>
          <LangBadge lang="it" />
          <span lang="it">{word.translations.it}</span>
        </div>
        <div className={styles.row}>
          <LangBadge lang="ko" />
          <span lang="ko">{word.translations.ko}</span>
        </div>
      </div>
    </div>
  );
}
