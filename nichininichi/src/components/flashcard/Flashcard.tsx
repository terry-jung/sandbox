import type { WordEntry } from '../../types';
import { useSwipe } from '../../hooks/useSwipe';
import { FlashcardFront } from './FlashcardFront';
import { FlashcardBack } from './FlashcardBack';
import styles from './Flashcard.module.css';

interface FlashcardProps {
  word: WordEntry;
  isFlipped: boolean;
  onFlip: () => void;
  onSwipeLeft?: () => void;
  onSwipeRight?: () => void;
}

export function Flashcard({
  word,
  isFlipped,
  onFlip,
  onSwipeLeft,
  onSwipeRight,
}: FlashcardProps) {
  const { onTouchStart, onTouchEnd } = useSwipe(onSwipeLeft, onSwipeRight);

  return (
    <div
      className={styles.perspective}
      onTouchStart={onTouchStart}
      onTouchEnd={onTouchEnd}
    >
      <div
        className={`${styles.card} ${isFlipped ? styles.flipped : ''}`}
        onClick={onFlip}
        role="button"
        tabIndex={0}
        aria-label={
          isFlipped
            ? `${word.kanji || word.reading}. Reading: ${word.reading}. English: ${word.translations.en}. Italian: ${word.translations.it}. Korean: ${word.translations.ko}.`
            : `Japanese word: ${word.kanji || word.reading}. Tap to reveal translation.`
        }
        onKeyDown={(e) => {
          if (e.key === ' ' || e.key === 'Enter') {
            e.preventDefault();
            onFlip();
          }
        }}
        lang="ja"
      >
        <div className={styles.front}>
          <FlashcardFront word={word} />
        </div>
        <div className={styles.back}>
          <FlashcardBack word={word} />
        </div>
      </div>
    </div>
  );
}
