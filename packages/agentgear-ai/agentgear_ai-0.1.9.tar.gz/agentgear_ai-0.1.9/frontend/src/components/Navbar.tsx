import { ReactNode } from "react";
import { useAuth } from "../lib/auth";

export const Navbar = ({ right }: { right?: ReactNode }) => {
  const { username, logout } = useAuth();
  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-3">
      <div className="text-sm font-medium text-slate-700">LLM Observability Dashboard</div>
      <div className="flex items-center gap-3">
        {right}
        {username ? <div className="text-sm text-slate-600">Signed in as {username}</div> : null}
        <button
          className="rounded border border-slate-200 px-3 py-1 text-xs font-semibold text-slate-700 hover:bg-slate-100"
          onClick={logout}
        >
          Logout
        </button>
      </div>
    </header>
  );
};
