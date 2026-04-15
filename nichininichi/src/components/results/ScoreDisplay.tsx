import { useState, useEffect } from 'react';
import { prefersReducedMotion } from '../../utils/accessibility';
import styles from './ScoreDisplay.module.css';

interface ScoreDisplayProps {
  score: number;
  total: number;
}

export function ScoreDisplay({ score, total }: ScoreDisplayProps) {
  const [displayScore, setDisplayScore] = useState(
    prefersReducedMotion() ? score : 0
  );

  useEffect(() => {
    if (prefersReducedMotion()) {
      setDisplayScore(score);
      return;
    }

    const duration = 600;
    const start = performance.now();

    function animate(now: number) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      setDisplayScore(Math.round(progress * score));
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    }

    requestAnimationFrame(animate);
  }, [score]);

  return (
    <div
      className={styles.display}
      aria-label={`Score: ${score} out of ${total} matched on first try`}
    >
      <div className={styles.scoreRow}>
        <span className={styles.value}>{displayScore}</span>
        <span className={styles.separator}>/</span>
        <span className={styles.total}>{total}</span>
      </div>
      <p className={styles.label}>matched on first try</p>
    </div>
  );
}
