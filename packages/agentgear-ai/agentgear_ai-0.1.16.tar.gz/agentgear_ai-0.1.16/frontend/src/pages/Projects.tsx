import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";
import { DataTable } from "../components/DataTable";
import { Layout } from "../components/Layout";

type Project = {
  id: string;
  name: string;
  description?: string;
  created_at: string;
};

export const ProjectsPage = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const [showForm, setShowForm] = useState(false);

  const load = async () => {
    const res = await api.get<Project[]>("/api/projects");
    setProjects(res.data);
  };

  useEffect(() => {
    load();
  }, []);

  const createProject = async () => {
    if (!name) return;
    await api.post("/api/projects", { name, description });
    setName("");
    setDescription("");
    setShowForm(false);
    await load();
  };

  const { role } = useAuth();
  const isAdmin = role === "admin";

  return (
    <Layout>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Projects</h1>
          <p className="text-sm text-slate-600">Manage AgentGear projects and API tokens.</p>
        </div>
        {isAdmin && (
          <button
            onClick={() => setShowForm(!showForm)}
            className="rounded bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700 shadow-sm transition-colors"
          >
            {showForm ? "Cancel" : "📂 New Project"}
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 gap-6">
        {showForm && (
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm max-w-lg mb-6 animate-slide-up">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">Create Project</h2>
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-slate-700">Name</label>
                <input
                  className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="My GenAI Agent"
                />
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700">Description</label>
                <textarea
                  className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Short description of the project..."
                  rows={3}
                />
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button
                  className="rounded px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-50"
                  onClick={() => setShowForm(false)}
                >
                  Cancel
                </button>
                <button
                  className="rounded bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
                  onClick={createProject}
                >
                  Create Project
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="p-4 border-b border-slate-100 bg-slate-50/50">
            <h3 className="font-medium text-slate-900">All Projects</h3>
          </div>
          <DataTable
            data={projects}
            columns={[
              { key: "name", header: "Name", render: (row) => <Link to={`/projects/${row.id}`} className="font-medium text-brand-600 hover:text-brand-800">{row.name}</Link> },
              { key: "description", header: "Description", render: (row) => <span className="text-slate-500 text-sm truncate max-w-xs block">{row.description || "-"}</span> },
              { key: "created_at", header: "Created" }
            ]}
          />
        </div>
      </div>
    </Layout>
  );
};
