import { NavLink } from "react-router-dom";
import { ReactNode, useEffect, useState } from "react";
import clsx from "clsx";
import { useAuth } from "../lib/auth";
import { api } from "../lib/api";

export const Sidebar = () => {
  const { role } = useAuth();
  const isAdmin = role === "admin";
  const [version, setVersion] = useState<string | null>(null);

  useEffect(() => {
    api
      .get<{ version?: string }>("/api/health")
      .then((response) => setVersion(response.data?.version ?? null))
      .catch(() => setVersion(null));
  }, []);

  return (
    <aside className="w-60 border-r border-slate-200 bg-white">
      <div className="px-4 py-4">
        <div className="text-lg font-semibold text-brand-700 flex items-center gap-2">
          <span>⚙️</span> AgentGear
        </div>
        <div className="text-xs text-slate-500 font-medium ml-8">v{version ?? "dev"}</div>
      </div>
      <nav className="mt-2 space-y-1">
        <NavItem to="/">Dashboard</NavItem>
        <NavItem to="/projects">Projects</NavItem>
        <NavItem to="/runs">Runs</NavItem>
        <NavItem to="/prompts">Prompt Registry</NavItem>
        <NavItem to="/datasets">Datasets</NavItem>
        <NavItem to="/evaluators">Evaluators</NavItem>

        {isAdmin && (
          <>
            <NavItem to="/api-management">API Management</NavItem>
            <NavItem to="/users">Users</NavItem>
            <NavItem to="/models">Models</NavItem>
          </>
        )}

        <NavItem to="/guide">Documentation</NavItem>
      </nav>
    </aside>
  );
};

const NavItem = ({ to, children }: { to: string; children: ReactNode }) => (
  <NavLink
    to={to}
    className={({ isActive }) =>
      clsx(
        "block px-4 py-2 text-sm font-medium transition hover:bg-slate-100",
        isActive ? "text-brand-700 bg-slate-100" : "text-slate-700"
      )
    }
  >
    {children}
  </NavLink>
);
