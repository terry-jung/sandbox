import type { WordEntry, WordStudyRecord } from '../types';
import wordsData from '../data/words.json';
import { daysBetween } from '../utils/dates';

const DEFAULT_WORDS_PER_DAY = 10;
const RECYCLE_DAYS = 14;

const allWords: WordEntry[] = wordsData as WordEntry[];

export function getAllWords(): WordEntry[] {
  return allWords;
}

export function getWordById(id: string): WordEntry | undefined {
  return allWords.find((w) => w.id === id);
}

export function selectDailyWords(
  wordsStudied: WordStudyRecord[],
  today: string,
  count: number = DEFAULT_WORDS_PER_DAY
): { words: WordEntry[]; allWordsCovered: boolean } {
  const studiedMap = new Map<string, WordStudyRecord>();
  for (const record of wordsStudied) {
    studiedMap.set(record.wordId, record);
  }

  // Filter eligible words: never studied OR last studied > 14 days ago
  const eligible = allWords.filter((word) => {
    const record = studiedMap.get(word.id);
    if (!record) return true;
    return daysBetween(record.lastStudiedDate, today) > RECYCLE_DAYS;
  });

  // Sort by dataset order (ID ascending) for determinism
  eligible.sort((a, b) => a.id.localeCompare(b.id));

  if (eligible.length >= count) {
    return {
      words: eligible.slice(0, count),
      allWordsCovered: false,
    };
  }

  // All words covered recently -- pick the oldest-studied
  const allSorted = [...allWords].sort((a, b) => {
    const recA = studiedMap.get(a.id);
    const recB = studiedMap.get(b.id);
    if (!recA && !recB) return a.id.localeCompare(b.id);
    if (!recA) return -1;
    if (!recB) return 1;
    return recA.lastStudiedDate.localeCompare(recB.lastStudiedDate);
  });

  return {
    words: allSorted.slice(0, count),
    allWordsCovered: true,
  };
}
