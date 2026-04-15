import { ChevronLeft, ChevronRight } from 'lucide-react';
import styles from './CardNav.module.css';

interface CardNavProps {
  onPrev: () => void;
  onNext: () => void;
  hasPrev: boolean;
  hasNext: boolean;
}

export function CardNav({ onPrev, onNext, hasPrev, hasNext }: CardNavProps) {
  return (
    <div className={styles.nav}>
      <button
        className={styles.button}
        onClick={onPrev}
        disabled={!hasPrev}
        aria-label="Previous card"
      >
        <ChevronLeft size={24} />
      </button>
      <button
        className={styles.button}
        onClick={onNext}
        disabled={!hasNext}
        aria-label="Next card"
      >
        <ChevronRight size={24} />
      </button>
    </div>
  );
}
