import { Route, Routes, Navigate } from "react-router-dom";
import { ProjectsPage } from "./pages/Projects";
import { ProjectDetailPage } from "./pages/ProjectDetail";
import { TokensPage } from "./pages/Tokens";
import { RunsPage } from "./pages/Runs";
import { RunDetailPage } from "./pages/RunDetail";
import { PromptsPage } from "./pages/Prompts";
import { PromptDetailPage } from "./pages/PromptDetail";
import { DashboardPage } from "./pages/Dashboard";
import { ApiManagementPage } from "./pages/ApiManagement";
import { GuidePage } from "./pages/Guide";
import { UsersPage } from "./pages/Users";
import { ModelsPage } from "./pages/Models";
import { SettingsPage } from "./pages/Settings";
import { AuthPage } from "./pages/Auth";
import { DatasetsPage } from "./pages/Datasets";
import { DatasetDetailPage } from "./pages/DatasetDetail";
import { EvaluationsPage } from "./pages/Evaluations";
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
            <DashboardPage />
          </RequireAuth>
        }
      />
      <Route
        path="/api-management"
        element={
          <RequireAuth>
            <ApiManagementPage />
          </RequireAuth>
        }
      />
      <Route
        path="/guide"
        element={
          <RequireAuth>
            <GuidePage />
          </RequireAuth>
        }
      />
      <Route
        path="/users"
        element={
          <RequireAuth>
            <UsersPage />
          </RequireAuth>
        }
      />
      <Route
        path="/models"
        element={
          <RequireAuth>
            <ModelsPage />
          </RequireAuth>
        }
      />
      <Route
        path="/settings"
        element={
          <RequireAuth>
            <SettingsPage />
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
      <Route
        path="/datasets"
        element={
          <RequireAuth>
            <DatasetsPage />
          </RequireAuth>
        }
      />
      <Route
        path="/datasets/:id"
        element={
          <RequireAuth>
            <DatasetDetailPage />
          </RequireAuth>
        }
      />
      <Route
        path="/evaluators"
        element={
          <RequireAuth>
            <EvaluationsPage />
          </RequireAuth>
        }
      />
    </Routes>
  );
}

export default App;
