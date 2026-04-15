import type {
  WordStudyRecord,
  QuizHistoryEntry,
  StreakData,
  DailyWordsCache,
  AppSettings,
} from '../types';

const PREFIX = 'nichininichi_';

const KEYS = {
  wordsStudied: `${PREFIX}words_studied`,
  quizHistory: `${PREFIX}quiz_history`,
  streak: `${PREFIX}streak`,
  dailyWords: `${PREFIX}daily_words`,
  settings: `${PREFIX}settings`,
} as const;

const DEFAULT_STREAK: StreakData = {
  currentStreak: 0,
  longestStreak: 0,
  lastActiveDate: '',
};

class StorageService {
  private available: boolean;

  constructor() {
    this.available = this.checkAvailability();
  }

  private checkAvailability(): boolean {
    try {
      const test = '__storage_test__';
      localStorage.setItem(test, test);
      localStorage.removeItem(test);
      return true;
    } catch {
      return false;
    }
  }

  isAvailable(): boolean {
    return this.available;
  }

  private get<T>(key: string, fallback: T): T {
    if (!this.available) return fallback;
    try {
      const raw = localStorage.getItem(key);
      if (raw === null) return fallback;
      return JSON.parse(raw) as T;
    } catch {
      return fallback;
    }
  }

  private set<T>(key: string, value: T): void {
    if (!this.available) return;
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch {
      // quota exceeded or other error - silently fail
    }
  }

  getWordsStudied(): WordStudyRecord[] {
    return this.get<WordStudyRecord[]>(KEYS.wordsStudied, []);
  }

  setWordsStudied(records: WordStudyRecord[]): void {
    this.set(KEYS.wordsStudied, records);
  }

  getQuizHistory(): QuizHistoryEntry[] {
    return this.get<QuizHistoryEntry[]>(KEYS.quizHistory, []);
  }

  addQuizEntry(entry: QuizHistoryEntry): void {
    const history = this.getQuizHistory();
    history.push(entry);
    this.set(KEYS.quizHistory, history);
  }

  getStreak(): StreakData {
    return this.get<StreakData>(KEYS.streak, DEFAULT_STREAK);
  }

  setStreak(streak: StreakData): void {
    this.set(KEYS.streak, streak);
  }

  getDailyWords(): DailyWordsCache | null {
    return this.get<DailyWordsCache | null>(KEYS.dailyWords, null);
  }

  setDailyWords(cache: DailyWordsCache): void {
    this.set(KEYS.dailyWords, cache);
  }

  getSettings(): AppSettings {
    return this.get<AppSettings>(KEYS.settings, {});
  }

  setSettings(settings: AppSettings): void {
    this.set(KEYS.settings, settings);
  }

  clearAll(): void {
    if (!this.available) return;
    Object.values(KEYS).forEach((key) => {
      try {
        localStorage.removeItem(key);
      } catch {
        // ignore
      }
    });
  }
}

export const storage = new StorageService();
