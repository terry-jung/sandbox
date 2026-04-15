export function getEncouragementMessage(score: number, total: number): string {
  const ratio = score / total;
  if (ratio === 1) return 'Perfect score! You nailed every single one.';
  if (ratio >= 0.8) return 'Great job! You really know these words.';
  if (ratio >= 0.6) return 'Good effort! Keep practicing and you\'ll get there.';
  if (ratio >= 0.4) return 'Nice try! Review the missed words and try again tomorrow.';
  return 'Don\'t worry -- every attempt builds your memory. Keep going!';
}
