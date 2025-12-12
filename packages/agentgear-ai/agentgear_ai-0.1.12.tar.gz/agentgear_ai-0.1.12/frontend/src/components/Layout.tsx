import { ReactNode } from "react";
import { Navbar } from "./Navbar";
import { Sidebar } from "./Sidebar";

export const Layout = ({ children, right }: { children: ReactNode; right?: ReactNode }) => (
  <div className="flex min-h-screen bg-slate-50">
    <Sidebar />
    <div className="flex flex-1 flex-col">
      <Navbar right={right} />
      <main className="flex-1 p-6">{children}</main>
    </div>
  </div>
);
