import { Flame, Trophy } from 'lucide-react';
import styles from './StreakCards.module.css';

interface StreakCardsProps {
  currentStreak: number;
  longestStreak: number;
}

export function StreakCards({ currentStreak, longestStreak }: StreakCardsProps) {
  return (
    <div className={styles.grid}>
      <div className={styles.card}>
        <div className={styles.iconWrap}>
          <Flame size={24} className={styles.flameIcon} />
        </div>
        <span className={styles.value}>{currentStreak}</span>
        <span className={styles.label}>Current Streak</span>
      </div>
      <div className={styles.card}>
        <div className={styles.iconWrap}>
          <Trophy size={24} className={styles.trophyIcon} />
        </div>
        <span className={styles.value}>{longestStreak}</span>
        <span className={styles.label}>Longest Streak</span>
      </div>
    </div>
  );
}
