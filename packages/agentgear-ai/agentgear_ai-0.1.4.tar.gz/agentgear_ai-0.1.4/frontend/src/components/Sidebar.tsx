import { NavLink } from "react-router-dom";
import { ReactNode } from "react";
import clsx from "clsx";

const links = [
  { to: "/projects", label: "Projects" },
  { to: "/runs", label: "Runs" },
  { to: "/prompts", label: "Prompts" }
];

export const Sidebar = () => {
  return (
    <aside className="w-60 border-r border-slate-200 bg-white">
      <div className="px-4 py-4 text-lg font-semibold text-brand-700">AgentGear</div>
      <nav className="mt-2 space-y-1">
        {links.map((link) => (
          <NavItem key={link.to} to={link.to}>
            {link.label}
          </NavItem>
        ))}
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
