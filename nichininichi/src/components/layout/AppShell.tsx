import { Outlet } from 'react-router-dom';
import { TopNav } from './TopNav';
import { BottomNav } from './BottomNav';
import styles from './AppShell.module.css';

export function AppShell() {
  return (
    <div className={styles.shell}>
      <TopNav />
      <main className={styles.content}>
        <div className={styles.container}>
          <Outlet />
        </div>
      </main>
      <BottomNav />
    </div>
  );
}
