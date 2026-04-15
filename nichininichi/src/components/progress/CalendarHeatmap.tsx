import type { QuizHistoryEntry } from '../../types';
import { getTodayISO } from '../../utils/dates';
import styles from './CalendarHeatmap.module.css';

interface CalendarHeatmapProps {
  quizHistory: QuizHistoryEntry[];
  daysToShow?: number;
}

export function CalendarHeatmap({
  quizHistory,
  daysToShow = 90,
}: CalendarHeatmapProps) {
  const today = new Date(getTodayISO() + 'T00:00:00');

  // Build a map of date -> best score
  const scoreMap = new Map<string, number>();
  for (const entry of quizHistory) {
    const existing = scoreMap.get(entry.date);
    if (existing === undefined || entry.score > existing) {
      scoreMap.set(entry.date, entry.score);
    }
  }

  // Generate day cells, aligned to weeks
  // Start from (daysToShow) days ago, but align to the start of that week (Sunday)
  const startDate = new Date(today);
  startDate.setDate(startDate.getDate() - daysToShow);
  // Align to Sunday
  startDate.setDate(startDate.getDate() - startDate.getDay());

  const days: Array<{
    date: string;
    dayOfWeek: number;
    isFuture: boolean;
    isToday: boolean;
    score: number | null;
  }> = [];

  const endDate = new Date(today);
  endDate.setDate(endDate.getDate() + (6 - endDate.getDay())); // fill out the week

  const current = new Date(startDate);
  while (current <= endDate) {
    const y = current.getFullYear();
    const m = String(current.getMonth() + 1).padStart(2, '0');
    const d = String(current.getDate()).padStart(2, '0');
    const dateStr = `${y}-${m}-${d}`;
    const isFuture = current > today;
    const isToday = dateStr === getTodayISO();

    days.push({
      date: dateStr,
      dayOfWeek: current.getDay(),
      isFuture,
      isToday,
      score: scoreMap.get(dateStr) ?? null,
    });

    current.setDate(current.getDate() + 1);
  }

  // Group into weeks (columns)
  const weeks: typeof days[] = [];
  for (let i = 0; i < days.length; i += 7) {
    weeks.push(days.slice(i, i + 7));
  }

  function getCellClass(day: (typeof days)[0]) {
    const classes = [styles.cell];
    if (day.isFuture) {
      classes.push(styles.future);
    } else if (day.score !== null) {
      if (day.score === 10) classes.push(styles.perfect);
      else if (day.score >= 7) classes.push(styles.quizDone);
      else classes.push(styles.studied);
    } else {
      classes.push(styles.empty);
    }
    if (day.isToday) classes.push(styles.today);
    return classes.join(' ');
  }

  return (
    <div className={styles.wrapper}>
      <h3 className={styles.title}>Activity</h3>
      <div className={styles.grid}>
        {weeks.map((week, wi) => (
          <div key={wi} className={styles.week}>
            {week.map((day) => (
              <div
                key={day.date}
                className={getCellClass(day)}
                title={
                  day.score !== null
                    ? `${day.date}: Score ${day.score}/10`
                    : day.date
                }
              />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
