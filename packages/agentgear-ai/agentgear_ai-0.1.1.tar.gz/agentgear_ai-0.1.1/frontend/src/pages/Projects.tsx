import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";
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
    await load();
  };

  return (
    <Layout>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Projects</h1>
          <p className="text-sm text-slate-600">Manage AgentGear projects and API tokens.</p>
        </div>
      </div>
      <div className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-[1.2fr_1fr]">
        <div>
          <DataTable
            data={projects}
            columns={[
              { key: "name", header: "Name", render: (row) => <Link to={`/projects/${row.id}`}>{row.name}</Link> },
              { key: "description", header: "Description" },
              { key: "created_at", header: "Created" }
            ]}
          />
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">Create Project</h2>
          <div className="mt-4 space-y-3">
            <div>
              <label className="text-sm font-medium text-slate-700">Name</label>
              <input
                className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div>
              <label className="text-sm font-medium text-slate-700">Description</label>
              <textarea
                className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>
            <button
              className="w-full rounded bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
              onClick={createProject}
            >
              Create
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
};
