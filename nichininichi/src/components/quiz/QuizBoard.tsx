import type { WordEntry } from '../../types';
import { QuizCardJp } from './QuizCardJp';
import { QuizCardTrans } from './QuizCardTrans';
import styles from './QuizBoard.module.css';

interface QuizBoardProps {
  words: WordEntry[];
  shuffledTranslationOrder: string[];
  selectedJpId: string | null;
  matchedPairs: Map<string, string>;
  onSelectJp: (wordId: string) => void;
  onSelectTrans: (wordId: string) => void;
  incorrectTransId: string | null;
  revealCorrectId: string | null;
}

export function QuizBoard({
  words,
  shuffledTranslationOrder,
  selectedJpId,
  matchedPairs,
  onSelectJp,
  onSelectTrans,
  incorrectTransId,
  revealCorrectId,
}: QuizBoardProps) {
  const matchedTransIds = new Set(matchedPairs.values());
  const wordsMap = new Map(words.map((w) => [w.id, w]));

  function getJpState(wordId: string) {
    if (matchedPairs.has(wordId)) return 'matched' as const;
    if (wordId === selectedJpId) return 'selected' as const;
    if (selectedJpId && wordId !== selectedJpId) return 'dimmed' as const;
    return 'default' as const;
  }

  function getTransState(wordId: string) {
    if (matchedTransIds.has(wordId)) return 'matched' as const;
    if (wordId === incorrectTransId) return 'incorrect' as const;
    if (wordId === revealCorrectId && incorrectTransId) return 'reveal' as const;
    return 'default' as const;
  }

  return (
    <div
      className={styles.board}
      role="application"
      aria-label="Matching quiz. Select a Japanese word, then select its translation."
    >
      <div className={styles.column}>
        <h3 className={styles.columnLabel}>Japanese</h3>
        {words.map((word) => (
          <QuizCardJp
            key={word.id}
            word={word}
            state={getJpState(word.id)}
            onSelect={() => onSelectJp(word.id)}
          />
        ))}
      </div>
      <div className={styles.column}>
        <h3 className={styles.columnLabel}>Translation</h3>
        {shuffledTranslationOrder.map((id) => {
          const word = wordsMap.get(id);
          if (!word) return null;
          return (
            <QuizCardTrans
              key={word.id}
              word={word}
              state={getTransState(word.id)}
              onSelect={() => onSelectTrans(word.id)}
            />
          );
        })}
      </div>
    </div>
  );
}
