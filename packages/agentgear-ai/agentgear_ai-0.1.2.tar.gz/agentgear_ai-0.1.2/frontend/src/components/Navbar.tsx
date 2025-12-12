import { ReactNode } from "react";

export const Navbar = ({ right }: { right?: ReactNode }) => {
  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-3">
      <div className="text-sm font-medium text-slate-700">LLM Observability Dashboard</div>
      <div>{right}</div>
    </header>
  );
};
