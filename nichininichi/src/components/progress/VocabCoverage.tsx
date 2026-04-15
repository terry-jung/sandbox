import { ProgressBar } from '../shared/ProgressBar';
import styles from './VocabCoverage.module.css';

interface VocabCoverageProps {
  studied: number;
  total: number;
}

export function VocabCoverage({ studied, total }: VocabCoverageProps) {
  return (
    <div className={styles.wrapper}>
      <h3 className={styles.title}>Vocabulary Coverage</h3>
      <div className={styles.bigNumber}>
        <span className={styles.current}>{studied}</span>
        <span className={styles.sep}> / </span>
        <span className={styles.total}>{total}</span>
      </div>
      <p className={styles.subtitle}>words studied</p>
      <ProgressBar current={studied} total={total} />
    </div>
  );
}
