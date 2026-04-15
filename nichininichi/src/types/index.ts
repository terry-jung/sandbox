// ============================================================
// WORD DATA (static dataset)
// ============================================================

export interface WordEntry {
  id: string;
  kanji: string | null;
  reading: string;
  partOfSpeech: PartOfSpeech;
  translations: {
    en: string;
    it: string;
    ko: string;
  };
  example: {
    ja: string;
    en: string;
    furigana?: string; // Format: "{漢字|かんじ}を{食|た}べます。" — kanji with reading in brackets
  };
}

export type PartOfSpeech =
  | 'noun'
  | 'i-adjective'
  | 'na-adjective'
  | 'ru-verb'
  | 'u-verb'
  | 'suru-verb'
  | 'adverb'
  | 'particle'
  | 'counter'
  | 'conjunction'
  | 'interjection'
  | 'prefix'
  | 'suffix'
  | 'pronoun'
  | 'expression';

export type DisplayWord = {
  primary: string;
  furigana: string | null;
};

// ============================================================
// STUDY PROGRESS (persisted in localStorage)
// ============================================================

export interface WordStudyRecord {
  wordId: string;
  lastStudiedDate: string;
  timesStudied: number;
}

export interface QuizHistoryEntry {
  date: string;
  score: number;
  totalWords: number;
  mistakes: string[];
  timeSeconds: number;
}

export interface StreakData {
  currentStreak: number;
  longestStreak: number;
  lastActiveDate: string;
}

export interface DailyWordsCache {
  date: string;
  wordIds: string[];
  goal?: number;
}

export interface AppSettings {
  dailyGoal?: number;
}

export interface PersistedState {
  wordsStudied: WordStudyRecord[];
  quizHistory: QuizHistoryEntry[];
  streak: StreakData;
  dailyWords: DailyWordsCache;
  settings: AppSettings;
}

// ============================================================
// QUIZ STATE (in-memory only)
// ============================================================

export type QuizPhase = 'idle' | 'active' | 'complete';

export interface QuizState {
  phase: QuizPhase;
  selectedJpId: string | null;
  matchedPairs: Map<string, string>;
  mistakes: Set<string>;
  correctFirstTry: number;
  startTime: number | null;
  elapsedSeconds: number;
  shuffledTranslationIds: string[];
  incorrectTransId: string | null;
  revealCorrectId: string | null;
}

// ============================================================
// STUDY STATE (in-memory)
// ============================================================

export interface StudyState {
  dailyWords: WordEntry[];
  currentIndex: number;
  flippedCards: Set<number>;
  isFirstVisit: boolean;
  dayNumber: number;
  allWordsCovered: boolean;
}
