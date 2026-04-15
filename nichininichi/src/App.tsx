import { HashRouter, Routes, Route } from 'react-router-dom';
import { StudyProvider } from './contexts/StudyContext';
import { QuizProvider } from './contexts/QuizContext';
import { AppShell } from './components/layout/AppShell';
import { TodayScreen } from './screens/TodayScreen';
import { QuizScreen } from './screens/QuizScreen';
import { ResultsScreen } from './screens/ResultsScreen';
import { ProgressScreen } from './screens/ProgressScreen';

export default function App() {
  return (
    <HashRouter>
      <StudyProvider>
        <QuizProvider>
          <Routes>
            <Route element={<AppShell />}>
              <Route path="/" element={<TodayScreen />} />
              <Route path="/quiz" element={<QuizScreen />} />
              <Route path="/results" element={<ResultsScreen />} />
              <Route path="/progress" element={<ProgressScreen />} />
            </Route>
          </Routes>
        </QuizProvider>
      </StudyProvider>
    </HashRouter>
  );
}
