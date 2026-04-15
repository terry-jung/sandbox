import styles from './QuizHeader.module.css';

interface QuizHeaderProps {
  score: number;
  total: number;
}

export function QuizHeader({ score, total }: QuizHeaderProps) {
  return (
    <div className={styles.header}>
      <h1 className={styles.title}>Quiz</h1>
      <div className={styles.score} aria-live="polite">
        <span className={styles.scoreValue}>{score}</span>
        <span className={styles.scoreSep}> / </span>
        <span className={styles.scoreTotal}>{total}</span>
      </div>
    </div>
  );
}
