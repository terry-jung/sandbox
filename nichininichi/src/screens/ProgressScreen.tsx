import { storage } from '../services/storage';
import { getAllWords } from '../services/wordSelection';
import { VocabCoverage } from '../components/progress/VocabCoverage';
import { StreakCards } from '../components/progress/StreakCards';
import { QuizHistory } from '../components/progress/QuizHistory';
import styles from './ProgressScreen.module.css';

export function ProgressScreen() {
  const wordsStudied = storage.getWordsStudied();
  const quizHistory = storage.getQuizHistory();
  const streak = storage.getStreak();
  const totalWords = getAllWords().length;

  return (
    <div className={styles.screen}>
      <h1 className={styles.title}>Progress</h1>

      <div className={styles.sections}>
        <VocabCoverage studied={wordsStudied.length} total={totalWords} />
        <StreakCards
          currentStreak={streak.currentStreak}
          longestStreak={streak.longestStreak}
        />
<QuizHistory history={quizHistory} />
      </div>
    </div>
  );
}
