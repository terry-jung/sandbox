import type { WordEntry } from '../../types';
import { LangBadge } from '../shared/LangBadge';
import { PosBadge } from '../shared/PosBadge';
import { renderFurigana } from '../../utils/furigana';
import styles from './FlashcardBack.module.css';

interface FlashcardBackProps {
  word: WordEntry;
}

export function FlashcardBack({ word }: FlashcardBackProps) {
  return (
    <div className={styles.back}>
      <div className={styles.reading} lang="ja">
        {word.kanji ? (
          <ruby>
            {word.kanji}
            <rt>{word.reading}</rt>
          </ruby>
        ) : (
          word.reading
        )}
      </div>
      <PosBadge pos={word.partOfSpeech} />
      <div className={styles.translations}>
        <div className={styles.translationRow}>
          <LangBadge lang="en" />
          <span lang="en">{word.translations.en}</span>
        </div>
        <div className={styles.translationRow}>
          <LangBadge lang="it" />
          <span lang="it">{word.translations.it}</span>
        </div>
        <div className={styles.translationRow}>
          <LangBadge lang="ko" />
          <span lang="ko">{word.translations.ko}</span>
        </div>
      </div>
      <div className={styles.example}>
        <p className={styles.exampleJa} lang="ja">
          {word.example.furigana
            ? renderFurigana(word.example.furigana)
            : word.example.ja}
        </p>
        <p className={styles.exampleEn} lang="en">
          {word.example.en}
        </p>
      </div>
    </div>
  );
}
