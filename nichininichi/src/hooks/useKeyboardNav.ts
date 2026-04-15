import { useEffect } from 'react';

interface KeyboardNavOptions {
  onLeft?: () => void;
  onRight?: () => void;
  onFlip?: () => void;
  onEnter?: () => void;
  enabled?: boolean;
}

export function useKeyboardNav({
  onLeft,
  onRight,
  onFlip,
  onEnter,
  enabled = true,
}: KeyboardNavOptions): void {
  useEffect(() => {
    if (!enabled) return;

    function handleKeyDown(e: KeyboardEvent) {
      const tag = (e.target as HTMLElement).tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;

      switch (e.key) {
        case 'ArrowLeft':
          e.preventDefault();
          onLeft?.();
          break;
        case 'ArrowRight':
          e.preventDefault();
          onRight?.();
          break;
        case 'ArrowUp':
        case 'ArrowDown':
        case ' ':
          e.preventDefault();
          onFlip?.();
          break;
        case 'Enter':
          e.preventDefault();
          onEnter?.();
          break;
      }
    }

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onLeft, onRight, onFlip, onEnter, enabled]);
}
