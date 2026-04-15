import type { QuizHistoryEntry } from '../../types';
import { ScoreBadge } from '../shared/ScoreBadge';
import { formatDate, formatTime } from '../../utils/dates';
import styles from './QuizHistory.module.css';

interface QuizHistoryProps {
  history: QuizHistoryEntry[];
}

export function QuizHistory({ history }: QuizHistoryProps) {
  if (history.length === 0) {
    return (
      <div className={styles.wrapper}>
        <h3 className={styles.title}>Quiz History</h3>
        <p className={styles.empty}>No quizzes taken yet. Complete today's quiz to see your history.</p>
      </div>
    );
  }

  const recent = [...history].reverse().slice(0, 20);

  return (
    <div className={styles.wrapper}>
      <h3 className={styles.title}>Quiz History</h3>
      <div className={styles.list}>
        {recent.map((entry, i) => (
          <div key={i} className={styles.row}>
            <span className={styles.date}>{formatDate(entry.date)}</span>
            <ScoreBadge score={entry.score} total={entry.totalWords} />
            <span className={styles.time}>{formatTime(entry.timeSeconds)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
