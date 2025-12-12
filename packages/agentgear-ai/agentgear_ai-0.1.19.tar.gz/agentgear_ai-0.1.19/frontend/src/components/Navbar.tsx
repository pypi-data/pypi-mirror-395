import { ReactNode } from "react";
import { useAuth } from "../lib/auth";
import { useLocation } from "react-router-dom";

export const Navbar = ({ right }: { right?: ReactNode }) => {
  const { username, logout } = useAuth();
  const location = useLocation();

  const getTitle = () => {
    const path = location.pathname;
    if (path === "/") return "Dashboard";
    if (path.startsWith("/projects")) return "Project Workspace";
    if (path.startsWith("/runs")) return "Trace Explorer";
    if (path.startsWith("/prompts")) return "Prompt Registry";
    if (path.startsWith("/api")) return "Settings";
    if (path.startsWith("/guide")) return "Documentation";
    return "AgentGear";
  };

  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-3 shadow-sm z-10 relative">
      <div className="flex items-center gap-2">
        <h1 className="text-lg font-semibold text-slate-800 tracking-tight">{getTitle()}</h1>
      </div>
      <div className="flex items-center gap-3">
        {right}
        {username ? (
          <div className="flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3 py-1">
            <span className="h-2 w-2 rounded-full bg-green-500"></span>
            <span className="text-xs font-medium text-slate-600">Welcome, {username}</span>
          </div>
        ) : null}
        <button
          className="rounded-md bg-white border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-50 hover:text-slate-900 transition-colors"
          onClick={logout}
        >
          Logout
        </button>
      </div>
    </header>
  );
};
