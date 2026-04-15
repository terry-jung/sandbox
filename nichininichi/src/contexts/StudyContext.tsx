import React, { createContext, useContext, useReducer, useEffect, useMemo } from 'react';
import type { WordEntry, StudyState } from '../types';
import { storage } from '../services/storage';
import { selectDailyWords, getWordById } from '../services/wordSelection';
import { getTodayISO } from '../utils/dates';

type StudyAction =
  | { type: 'SET_DAILY_WORDS'; words: WordEntry[]; allWordsCovered: boolean }
  | { type: 'SET_INDEX'; index: number }
  | { type: 'FLIP_CARD'; index: number }
  | { type: 'NEXT_CARD' }
  | { type: 'PREV_CARD' };

const initialState: StudyState = {
  dailyWords: [],
  currentIndex: 0,
  flippedCards: new Set(),
  isFirstVisit: true,
  dayNumber: 1,
  allWordsCovered: false,
};

function studyReducer(state: StudyState, action: StudyAction): StudyState {
  switch (action.type) {
    case 'SET_DAILY_WORDS':
      return {
        ...state,
        dailyWords: action.words,
        allWordsCovered: action.allWordsCovered,
        currentIndex: 0,
        flippedCards: new Set(),
      };
    case 'SET_INDEX':
      return { ...state, currentIndex: action.index };
    case 'FLIP_CARD': {
      const newFlipped = new Set(state.flippedCards);
      newFlipped.add(action.index);
      return { ...state, flippedCards: newFlipped };
    }
    case 'NEXT_CARD': {
      const next = (state.currentIndex + 1) % state.dailyWords.length;
      return { ...state, currentIndex: next };
    }
    case 'PREV_CARD': {
      const prev = (state.currentIndex - 1 + state.dailyWords.length) % state.dailyWords.length;
      return { ...state, currentIndex: prev };
    }
    default:
      return state;
  }
}

interface StudyContextValue {
  state: StudyState;
  dispatch: React.Dispatch<StudyAction>;
}

const StudyContext = createContext<StudyContextValue | null>(null);

export function StudyProvider({ children }: { children: React.ReactNode }) {
  const quizHistory = storage.getQuizHistory();
  const streak = storage.getStreak();

  const computedInitial = useMemo(() => {
    const distinctDays = new Set(quizHistory.map((q) => q.date)).size;
    const isFirst = quizHistory.length === 0 && streak.currentStreak === 0;
    return {
      ...initialState,
      isFirstVisit: isFirst,
      dayNumber: distinctDays + 1,
    };
  }, [quizHistory, streak]);

  const [state, dispatch] = useReducer(studyReducer, computedInitial);

  useEffect(() => {
    const today = getTodayISO();
    const cached = storage.getDailyWords();
    const goal = storage.getSettings().dailyGoal ?? 10;

    if (cached && cached.date === today && (cached.goal ?? 10) === goal) {
      // Use cached daily words
      const words = cached.wordIds
        .map((id) => getWordById(id))
        .filter((w): w is WordEntry => w !== undefined);
      if (words.length > 0) {
        dispatch({ type: 'SET_DAILY_WORDS', words, allWordsCovered: false });
        return;
      }
    }

    // Compute new daily words
    const wordsStudied = storage.getWordsStudied();
    const result = selectDailyWords(wordsStudied, today, goal);
    dispatch({
      type: 'SET_DAILY_WORDS',
      words: result.words,
      allWordsCovered: result.allWordsCovered,
    });

    // Cache them
    storage.setDailyWords({
      date: today,
      wordIds: result.words.map((w) => w.id),
      goal,
    });
  }, []);

  return (
    <StudyContext.Provider value={{ state, dispatch }}>
      {children}
    </StudyContext.Provider>
  );
}

export function useStudy() {
  const ctx = useContext(StudyContext);
  if (!ctx) throw new Error('useStudy must be used within StudyProvider');
  return ctx;
}
