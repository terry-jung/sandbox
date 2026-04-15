import styles from './LangBadge.module.css';

interface LangBadgeProps {
  lang: 'en' | 'it' | 'ko';
}

const LABELS = { en: 'EN', it: 'IT', ko: 'KO' };

export function LangBadge({ lang }: LangBadgeProps) {
  return (
    <span className={`${styles.badge} ${styles[lang]}`}>
      {LABELS[lang]}
    </span>
  );
}
