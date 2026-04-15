import styles from './ScoreBadge.module.css';

interface ScoreBadgeProps {
  score: number;
  total: number;
}

export function ScoreBadge({ score, total }: ScoreBadgeProps) {
  let variant = 'low';
  if (score === total) variant = 'perfect';
  else if (score >= 7) variant = 'high';
  else if (score >= 4) variant = 'mid';

  return (
    <span className={`${styles.badge} ${styles[variant]}`}>
      {score}/{total}
    </span>
  );
}
