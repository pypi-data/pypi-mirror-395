import { Route, Routes, Navigate } from "react-router-dom";
import { ProjectsPage } from "./pages/Projects";
import { ProjectDetailPage } from "./pages/ProjectDetail";
import { TokensPage } from "./pages/Tokens";
import { RunsPage } from "./pages/Runs";
import { RunDetailPage } from "./pages/RunDetail";
import { PromptsPage } from "./pages/Prompts";
import { PromptDetailPage } from "./pages/PromptDetail";
import { AuthPage } from "./pages/Auth";
import { useAuth } from "./lib/auth";

const RequireAuth = ({ children }: { children: JSX.Element }) => {
  const { token, ready } = useAuth();
  if (!ready) return <div className="p-6 text-sm text-slate-700">Loading...</div>;
  if (!token) return <Navigate to="/auth" replace />;
  return children;
};

function App() {
  return (
    <Routes>
      <Route path="/auth" element={<AuthPage />} />
      <Route
        path="/"
        element={
          <RequireAuth>
            <Navigate to="/projects" replace />
          </RequireAuth>
        }
      />
      <Route
        path="/projects"
        element={
          <RequireAuth>
            <ProjectsPage />
          </RequireAuth>
        }
      />
      <Route
        path="/projects/:id"
        element={
          <RequireAuth>
            <ProjectDetailPage />
          </RequireAuth>
        }
      />
      <Route
        path="/projects/:id/tokens"
        element={
          <RequireAuth>
            <TokensPage />
          </RequireAuth>
        }
      />
      <Route
        path="/runs"
        element={
          <RequireAuth>
            <RunsPage />
          </RequireAuth>
        }
      />
      <Route
        path="/runs/:id"
        element={
          <RequireAuth>
            <RunDetailPage />
          </RequireAuth>
        }
      />
      <Route
        path="/prompts"
        element={
          <RequireAuth>
            <PromptsPage />
          </RequireAuth>
        }
      />
      <Route
        path="/prompts/:id"
        element={
          <RequireAuth>
            <PromptDetailPage />
          </RequireAuth>
        }
      />
    </Routes>
  );
}

export default App;
