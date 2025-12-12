import { Route, Routes, Navigate } from "react-router-dom";
import { ProjectsPage } from "./pages/Projects";
import { ProjectDetailPage } from "./pages/ProjectDetail";
import { TokensPage } from "./pages/Tokens";
import { RunsPage } from "./pages/Runs";
import { RunDetailPage } from "./pages/RunDetail";
import { PromptsPage } from "./pages/Prompts";
import { PromptDetailPage } from "./pages/PromptDetail";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/projects" replace />} />
      <Route path="/projects" element={<ProjectsPage />} />
      <Route path="/projects/:id" element={<ProjectDetailPage />} />
      <Route path="/projects/:id/tokens" element={<TokensPage />} />
      <Route path="/runs" element={<RunsPage />} />
      <Route path="/runs/:id" element={<RunDetailPage />} />
      <Route path="/prompts" element={<PromptsPage />} />
      <Route path="/prompts/:id" element={<PromptDetailPage />} />
    </Routes>
  );
}

export default App;
