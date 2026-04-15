import React, { createContext, useContext, useReducer, useCallback } from 'react';
import type { QuizState, WordEntry, QuizHistoryEntry } from '../types';
import { seededShuffle } from '../utils/shuffle';
import { getTodayISO, isYesterday, isToday } from '../utils/dates';
import { storage } from '../services/storage';

type QuizAction =
  | { type: 'START_QUIZ'; words: WordEntry[] }
  | { type: 'SELECT_JP'; wordId: string }
  | { type: 'DESELECT_JP' }
  | { type: 'MATCH_CORRECT'; jpId: string; transId: string }
  | { type: 'MATCH_INCORRECT'; transId: string; correctId: string }
  | { type: 'CLEAR_FEEDBACK' }
  | { type: 'COMPLETE_QUIZ'; elapsedSeconds: number; words: WordEntry[] }
  | { type: 'RESET_QUIZ' };

const initialQuizState: QuizState = {
  phase: 'idle',
  selectedJpId: null,
  matchedPairs: new Map(),
  mistakes: new Set(),
  correctFirstTry: 0,
  startTime: null,
  elapsedSeconds: 0,
  shuffledTranslationIds: [],
  incorrectTransId: null,
  revealCorrectId: null,
};

function quizReducer(state: QuizState, action: QuizAction): QuizState {
  switch (action.type) {
    case 'START_QUIZ': {
      const today = getTodayISO();
      const shuffled = seededShuffle(
        action.words.map((w) => w.id),
        `quiz-trans-${today}`
      );
      return {
        ...initialQuizState,
        phase: 'active',
        startTime: Date.now(),
        shuffledTranslationIds: shuffled,
      };
    }
    case 'SELECT_JP':
      return { ...state, selectedJpId: action.wordId };
    case 'DESELECT_JP':
      return { ...state, selectedJpId: null };
    case 'MATCH_CORRECT': {
      const newMatched = new Map(state.matchedPairs);
      newMatched.set(action.jpId, action.transId);
      const wasAlreadyMistake = state.mistakes.has(action.jpId);
      return {
        ...state,
        matchedPairs: newMatched,
        selectedJpId: null,
        correctFirstTry: wasAlreadyMistake
          ? state.correctFirstTry
          : state.correctFirstTry + 1,
      };
    }
    case 'MATCH_INCORRECT': {
      const newMistakes = new Set(state.mistakes);
      if (state.selectedJpId) {
        newMistakes.add(state.selectedJpId);
      }
      return {
        ...state,
        mistakes: newMistakes,
        incorrectTransId: action.transId,
        revealCorrectId: action.correctId,
      };
    }
    case 'CLEAR_FEEDBACK':
      return {
        ...state,
        selectedJpId: null,
        incorrectTransId: null,
        revealCorrectId: null,
      };
    case 'COMPLETE_QUIZ': {
      // Compute final score inside reducer to avoid stale closure issues
      const today = getTodayISO();
      const entry: QuizHistoryEntry = {
        date: today,
        score: state.correctFirstTry,
        totalWords: action.words.length,
        mistakes: Array.from(state.mistakes),
        timeSeconds: action.elapsedSeconds,
      };
      storage.addQuizEntry(entry);

      // Update words studied
      const wordsStudied = storage.getWordsStudied();
      for (const word of action.words) {
        const existing = wordsStudied.find((w) => w.wordId === word.id);
        if (existing) {
          existing.lastStudiedDate = today;
          existing.timesStudied += 1;
        } else {
          wordsStudied.push({
            wordId: word.id,
            lastStudiedDate: today,
            timesStudied: 1,
          });
        }
      }
      storage.setWordsStudied(wordsStudied);

      // Update streak
      const streak = storage.getStreak();
      if (!isToday(streak.lastActiveDate)) {
        if (isYesterday(streak.lastActiveDate)) {
          streak.currentStreak += 1;
        } else if (streak.lastActiveDate === '') {
          streak.currentStreak = 1;
        } else {
          streak.currentStreak = 1;
        }
        streak.lastActiveDate = today;
        if (streak.currentStreak > streak.longestStreak) {
          streak.longestStreak = streak.currentStreak;
        }
        storage.setStreak(streak);
      }

      return {
        ...state,
        phase: 'complete',
        elapsedSeconds: action.elapsedSeconds,
      };
    }
    case 'RESET_QUIZ':
      return initialQuizState;
    default:
      return state;
  }
}

interface QuizContextValue {
  state: QuizState;
  dispatch: React.Dispatch<QuizAction>;
  startQuiz: (words: WordEntry[]) => void;
  selectJp: (wordId: string) => void;
  selectTrans: (transWordId: string, words: WordEntry[]) => void;
  completeQuiz: (elapsedSeconds: number, words: WordEntry[]) => void;
  resetQuiz: () => void;
}

const QuizContext = createContext<QuizContextValue | null>(null);

export function QuizProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(quizReducer, initialQuizState);

  const startQuiz = useCallback(
    (words: WordEntry[]) => {
      dispatch({ type: 'START_QUIZ', words });
    },
    []
  );

  const selectJp = useCallback(
    (wordId: string) => {
      if (state.matchedPairs.has(wordId)) return;
      if (state.selectedJpId === wordId) {
        dispatch({ type: 'DESELECT_JP' });
      } else {
        dispatch({ type: 'SELECT_JP', wordId });
      }
    },
    [state.selectedJpId, state.matchedPairs]
  );

  const selectTrans = useCallback(
    (transWordId: string, _words: WordEntry[]) => {
      if (!state.selectedJpId) return;
      // Check if this translation is already matched
      const matchedTransIds = new Set(state.matchedPairs.values());
      if (matchedTransIds.has(transWordId)) return;

      if (state.selectedJpId === transWordId) {
        // Correct match
        dispatch({
          type: 'MATCH_CORRECT',
          jpId: state.selectedJpId,
          transId: transWordId,
        });
      } else {
        // Incorrect match - find the correct translation ID for the selected JP word
        dispatch({
          type: 'MATCH_INCORRECT',
          transId: transWordId,
          correctId: state.selectedJpId,
        });
        // Clear feedback after 2 seconds
        setTimeout(() => {
          dispatch({ type: 'CLEAR_FEEDBACK' });
        }, 2000);
      }
    },
    [state.selectedJpId, state.matchedPairs]
  );

  const completeQuiz = useCallback(
    (elapsedSeconds: number, words: WordEntry[]) => {
      dispatch({ type: 'COMPLETE_QUIZ', elapsedSeconds, words });
    },
    []
  );

  const resetQuiz = useCallback(() => {
    dispatch({ type: 'RESET_QUIZ' });
  }, []);

  return (
    <QuizContext.Provider
      value={{ state, dispatch, startQuiz, selectJp, selectTrans, completeQuiz, resetQuiz }}
    >
      {children}
    </QuizContext.Provider>
  );
}

export function useQuiz() {
  const ctx = useContext(QuizContext);
  if (!ctx) throw new Error('useQuiz must be used within QuizProvider');
  return ctx;
}
