import { NavLink } from 'react-router-dom';
import { StreakCounter } from '../shared/StreakCounter';
import { storage } from '../../services/storage';
import styles from './TopNav.module.css';

export function TopNav() {
  const streak = storage.getStreak();

  return (
    <header className={styles.header}>
      <div className={styles.inner}>
        <span className={styles.logo} lang="ja">
          NichiNichi
        </span>
        <nav className={styles.nav} aria-label="Main navigation">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `${styles.link} ${isActive ? styles.active : ''}`
            }
            end
          >
            Today
          </NavLink>
          <NavLink
            to="/quiz"
            className={({ isActive }) =>
              `${styles.link} ${isActive ? styles.active : ''}`
            }
          >
            Quiz
          </NavLink>
          <NavLink
            to="/progress"
            className={({ isActive }) =>
              `${styles.link} ${isActive ? styles.active : ''}`
            }
          >
            Progress
          </NavLink>
        </nav>
        <StreakCounter count={streak.currentStreak} />
      </div>
    </header>
  );
}
