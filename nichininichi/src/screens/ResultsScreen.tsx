import { useNavigate } from 'react-router-dom';
import { useStudy } from '../contexts/StudyContext';
import { useQuiz } from '../contexts/QuizContext';
import { ScoreDisplay } from '../components/results/ScoreDisplay';
import { MissedWordCard } from '../components/results/MissedWordCard';
import { StreakCounter } from '../components/shared/StreakCounter';
import { Button } from '../components/shared/Button';
import { getEncouragementMessage } from '../utils/encouragement';
import { formatTime } from '../utils/dates';
import { storage } from '../services/storage';
import styles from './ResultsScreen.module.css';

export function ResultsScreen() {
  const navigate = useNavigate();
  const { state: studyState } = useStudy();
  const { state: quizState, resetQuiz } = useQuiz();
  const streak = storage.getStreak();

  const { dailyWords } = studyState;
  const { correctFirstTry, mistakes, elapsedSeconds } = quizState;

  const total = dailyWords.length;
  const missedWords = dailyWords.filter((w) => mistakes.has(w.id));

  const handleGoHome = () => {
    resetQuiz();
    navigate('/');
  };

  const handleGoProgress = () => {
    navigate('/progress');
  };

  return (
    <div className={styles.screen}>
      <h1 className="sr-only">Quiz Results</h1>
      <ScoreDisplay score={correctFirstTry} total={total} />

      <p className={styles.encouragement}>
        {getEncouragementMessage(correctFirstTry, total)}
      </p>

      <div className={styles.statsRow}>
        <div className={styles.statItem}>
          <StreakCounter count={streak.currentStreak} showLabel />
        </div>
        <div className={styles.statItem}>
          <span className={styles.statValue}>{formatTime(elapsedSeconds)}</span>
          <span className={styles.statLabel}>time</span>
        </div>
      </div>

      {missedWords.length > 0 && (
        <div className={styles.missedSection}>
          <h3 className={styles.missedTitle}>Words to review</h3>
          <div className={styles.missedList}>
            {missedWords.map((word) => (
              <MissedWordCard key={word.id} word={word} />
            ))}
          </div>
        </div>
      )}

      <div className={styles.actions}>
        <Button onClick={handleGoHome} fullWidth>
          Back to Today
        </Button>
        <Button variant="secondary" onClick={handleGoProgress} fullWidth>
          View Progress
        </Button>
      </div>
    </div>
  );
}
