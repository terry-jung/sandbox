import { NavLink } from 'react-router-dom';
import { BookOpen, Brain, BarChart3 } from 'lucide-react';
import styles from './BottomNav.module.css';

const tabs = [
  { to: '/', icon: BookOpen, label: 'Today' },
  { to: '/quiz', icon: Brain, label: 'Quiz' },
  { to: '/progress', icon: BarChart3, label: 'Progress' },
];

export function BottomNav() {
  return (
    <nav className={styles.nav} aria-label="Main navigation">
      {tabs.map(({ to, icon: Icon, label }) => (
        <NavLink
          key={to}
          to={to}
          className={({ isActive }) =>
            `${styles.tab} ${isActive ? styles.active : ''}`
          }
          end={to === '/'}
        >
          <Icon size={24} strokeWidth={1.5} />
          <span className={styles.label}>{label}</span>
        </NavLink>
      ))}
    </nav>
  );
}
