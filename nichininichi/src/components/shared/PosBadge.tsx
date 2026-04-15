import type { PartOfSpeech } from '../../types';
import styles from './PosBadge.module.css';

const DISPLAY: Record<PartOfSpeech, string> = {
  noun: 'noun',
  'i-adjective': 'i-adj',
  'na-adjective': 'na-adj',
  'ru-verb': 'ru-verb',
  'u-verb': 'u-verb',
  'suru-verb': 'suru-verb',
  adverb: 'adverb',
  particle: 'particle',
  counter: 'counter',
  conjunction: 'conj.',
  interjection: 'interj.',
  prefix: 'prefix',
  suffix: 'suffix',
  pronoun: 'pronoun',
  expression: 'expr.',
};

interface PosBadgeProps {
  pos: PartOfSpeech;
}

export function PosBadge({ pos }: PosBadgeProps) {
  return <span className={styles.badge}>{DISPLAY[pos]}</span>;
}
