import { useCallback, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useStudy } from '../contexts/StudyContext';
import { useKeyboardNav } from '../hooks/useKeyboardNav';
import { Flashcard } from '../components/flashcard/Flashcard';
import { CardDots } from '../components/flashcard/CardDots';
import { CardNav } from '../components/flashcard/CardNav';
import { Button } from '../components/shared/Button';
import { StreakCounter } from '../components/shared/StreakCounter';
import { storage } from '../services/storage';
import { selectDailyWords } from '../services/wordSelection';
import { getTodayISO } from '../utils/dates';
import styles from './TodayScreen.module.css';

export function TodayScreen() {
  const { state, dispatch } = useStudy();
  const navigate = useNavigate();
  const streak = storage.getStreak();

  const savedGoal = storage.getSettings().dailyGoal ?? 10;
  const [goalInput, setGoalInput] = useState(String(savedGoal));

  const handleGoalApply = useCallback(() => {
    const count = Math.max(1, Math.min(800, parseInt(goalInput) || 10));
    setGoalInput(String(count));
    const settings = storage.getSettings();
    storage.setSettings({ ...settings, dailyGoal: count });
    const today = getTodayISO();
    const wordsStudied = storage.getWordsStudied();
    const result = selectDailyWords(wordsStudied, today, count);
    storage.setDailyWords({ date: today, wordIds: result.words.map((w) => w.id), goal: count });
    dispatch({ type: 'SET_DAILY_WORDS', words: result.words, allWordsCovered: result.allWordsCovered });
  }, [dispatch, goalInput]);

  const { dailyWords, currentIndex, flippedCards, isFirstVisit, dayNumber, allWordsCovered } =
    state;

  const currentWord = dailyWords[currentIndex];
  const isFlipped = flippedCards.has(currentIndex);
  const hasFlippedAny = flippedCards.size > 0;

  const handleFlip = useCallback(() => {
    dispatch({ type: 'FLIP_CARD', index: currentIndex });
  }, [dispatch, currentIndex]);

  const handleNext = useCallback(() => {
    dispatch({ type: 'NEXT_CARD' });
  }, [dispatch]);

  const handlePrev = useCallback(() => {
    dispatch({ type: 'PREV_CARD' });
  }, [dispatch]);

  const handleStartQuiz = useCallback(() => {
    navigate('/quiz');
  }, [navigate]);

  useKeyboardNav({
    onLeft: handlePrev,
    onRight: handleNext,
    onFlip: handleFlip,
    onEnter: handleStartQuiz,
    enabled: true,
  });

  if (!currentWord) {
    return (
      <div className={styles.screen}>
        <p className={styles.loading}>Loading today's words...</p>
      </div>
    );
  }

  const welcomeMessage = allWordsCovered
    ? "You've seen all words. Time to sharpen what you know."
    : isFirstVisit
      ? `Welcome. Let's start with today's ${dailyWords.length} words.`
      : `Welcome back. Day ${dayNumber} \u2014 here are today's words.`;

  return (
    <div className={styles.screen}>
      <div className={styles.header}>
        <h1 className={styles.appName} lang="ja">
          NichiNichi
        </h1>
        <StreakCounter count={streak.currentStreak} />
      </div>

      <div className={styles.goalRow}>
        <label className={styles.goalLabel} htmlFor="goal-input">Words today</label>
        <input
          id="goal-input"
          className={styles.goalInput}
          type="number"
          min={1}
          max={800}
          value={goalInput}
          onChange={(e) => setGoalInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleGoalApply()}
        />
        <button className={styles.goalGo} onClick={handleGoalApply}>Go</button>
      </div>

      <p className={styles.welcome}>{welcomeMessage}</p>

      <div className={styles.cardArea}>
        <Flashcard
          word={currentWord}
          isFlipped={isFlipped}
          onFlip={handleFlip}
          onSwipeLeft={handleNext}
          onSwipeRight={handlePrev}
        />
      </div>

      <div className={styles.dots}>
        <CardDots
          total={dailyWords.length}
          currentIndex={currentIndex}
          flippedIndices={flippedCards}
        />
      </div>

      <CardNav
        onPrev={handlePrev}
        onNext={handleNext}
        hasPrev={true}
        hasNext={true}
      />

      <div className={styles.quizButton}>
        <Button
          onClick={handleStartQuiz}
          fullWidth
          style={{ opacity: hasFlippedAny ? 1 : 0.7 }}
        >
          Start Quiz
        </Button>
      </div>
    </div>
  );
}
