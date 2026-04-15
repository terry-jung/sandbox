import styles from './CardDots.module.css';

interface CardDotsProps {
  total: number;
  currentIndex: number;
  flippedIndices: Set<number>;
}

export function CardDots({ total, currentIndex, flippedIndices }: CardDotsProps) {
  return (
    <div
      className={styles.dots}
      role="status"
      aria-label={`Card ${currentIndex + 1} of ${total}`}
    >
      {Array.from({ length: total }, (_, i) => {
        let className = styles.dot;
        if (i === currentIndex) className += ` ${styles.active}`;
        else if (flippedIndices.has(i)) className += ` ${styles.studied}`;

        return (
          <div
            key={i}
            className={className}
            aria-hidden="true"
          />
        );
      })}
    </div>
  );
}
