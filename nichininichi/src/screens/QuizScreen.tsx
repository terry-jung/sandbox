import { useEffect, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useStudy } from '../contexts/StudyContext';
import { useQuiz } from '../contexts/QuizContext';
import { useTimer } from '../hooks/useTimer';
import { QuizHeader } from '../components/quiz/QuizHeader';
import { QuizBoard } from '../components/quiz/QuizBoard';
import { Button } from '../components/shared/Button';
import styles from './QuizScreen.module.css';

export function QuizScreen() {
  const navigate = useNavigate();
  const { state: studyState } = useStudy();
  const { state: quizState, startQuiz, selectJp, selectTrans, completeQuiz, resetQuiz } =
    useQuiz();
  const { elapsedSeconds, start: timerStart, stop: timerStop, reset: timerReset } = useTimer();
  const hasCompletedRef = useRef(false);

  const { dailyWords } = studyState;
  const { phase, matchedPairs, selectedJpId, shuffledTranslationIds, incorrectTransId, revealCorrectId } =
    quizState;

  // Reset quiz state on mount (handles re-entry after previous quiz)
  useEffect(() => {
    hasCompletedRef.current = false;
    resetQuiz();
    timerReset();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Start quiz when reset is done and we're idle with words
  useEffect(() => {
    if (phase === 'idle' && dailyWords.length > 0) {
      startQuiz(dailyWords);
      timerStart();
    }
  }, [phase, dailyWords, startQuiz, timerStart]);

  // Check completion — use ref guard to prevent double-fire
  useEffect(() => {
    if (
      phase === 'active' &&
      matchedPairs.size === dailyWords.length &&
      dailyWords.length > 0 &&
      !hasCompletedRef.current
    ) {
      hasCompletedRef.current = true;
      timerStop();
      completeQuiz(elapsedSeconds, dailyWords);
    }
  }, [matchedPairs.size, dailyWords.length, phase, timerStop, elapsedSeconds, completeQuiz, dailyWords]);

  // Navigate to results when complete
  useEffect(() => {
    if (phase === 'complete') {
      navigate('/results');
    }
  }, [phase, navigate]);

  const handleSelectTrans = useCallback(
    (transWordId: string) => {
      selectTrans(transWordId, dailyWords);
    },
    [selectTrans, dailyWords]
  );

  if (dailyWords.length === 0) {
    return (
      <div className={styles.screen}>
        <p className={styles.empty}>
          No words loaded yet. Go to Today to study first.
        </p>
        <Button onClick={() => navigate('/')}>Go to Today</Button>
      </div>
    );
  }

  return (
    <div className={styles.screen}>
      <QuizHeader
        score={matchedPairs.size}
        total={dailyWords.length}
      />
      <QuizBoard
        words={dailyWords}
        shuffledTranslationOrder={shuffledTranslationIds}
        selectedJpId={selectedJpId}
        matchedPairs={matchedPairs}
        onSelectJp={selectJp}
        onSelectTrans={handleSelectTrans}
        incorrectTransId={incorrectTransId}
        revealCorrectId={revealCorrectId}
      />
    </div>
  );
}
