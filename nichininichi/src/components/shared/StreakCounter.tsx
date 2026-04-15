import { Flame } from 'lucide-react';
import styles from './StreakCounter.module.css';

interface StreakCounterProps {
  count: number;
  showLabel?: boolean;
}

export function StreakCounter({ count, showLabel = false }: StreakCounterProps) {
  const isActive = count > 0;
  return (
    <div className={styles.streak}>
      <Flame
        size={20}
        className={`${styles.icon} ${isActive ? styles.active : styles.inactive}`}
      />
      <span className={styles.count}>{count}</span>
      {showLabel && <span className={styles.label}>day streak</span>}
    </div>
  );
}
