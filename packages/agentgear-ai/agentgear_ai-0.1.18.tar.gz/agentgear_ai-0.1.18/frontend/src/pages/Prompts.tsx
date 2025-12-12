import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { DataTable } from "../components/DataTable";
import { Layout } from "../components/Layout";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";

type Prompt = { id: string; name: string; project_id: string; scope: string };

export const PromptsPage = () => {
  const { role } = useAuth();
  const isAdmin = role === "admin";

  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [projects, setProjects] = useState<{ id: string, name: string }[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [scope, setScope] = useState("project");
  const [content, setContent] = useState("");
  const [tags, setTags] = useState("");

  const load = async () => {
    const [promptsRes, projectsRes] = await Promise.all([
      api.get<Prompt[]>("/api/prompts"),
      api.get<{ id: string, name: string }[]>("/api/projects")
    ]);
    setPrompts(promptsRes.data);
    setProjects(projectsRes.data);
    if (!selectedProjectId && projectsRes.data.length > 0) {
      setSelectedProjectId(projectsRes.data[0].id);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const createPrompt = async () => {
    if (!name || !selectedProjectId || !content) return;
    try {
      const tagsList = tags.split(",").map(t => t.trim()).filter(Boolean);
      await api.post("/api/prompts", { name, description, project_id: selectedProjectId, scope, content, tags: tagsList });
      setName("");
      setDescription("");
      setContent("");
      setTags("");
      setScope("project");
      setShowForm(false);
      load();
    } catch (e) {
      alert("Failed to create prompt");
    }
  };

  return (
    <Layout>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Prompt Registry</h1>
          <p className="text-sm text-slate-600">Manage prompt registry and versions.</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="rounded bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700 shadow-sm transition-colors"
        >
          {showForm ? "Cancel" : "📝 New Prompt"}
        </button>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {showForm && (
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm max-w-lg mb-6 animate-slide-up">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">Create Prompt</h2>
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-slate-700">Project</label>
                <select
                  className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                  value={selectedProjectId}
                  onChange={(e) => setSelectedProjectId(e.target.value)}
                >
                  {projects.map(p => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
              </div>

              {isAdmin && (
                <div>
                  <label className="text-sm font-medium text-slate-700">Scope</label>
                  <select
                    className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                    value={scope}
                    onChange={(e) => setScope(e.target.value)}
                  >
                    <option value="project">Project (Private)</option>
                    <option value="global">Global (All Projects)</option>
                  </select>
                </div>
              )}

              <div>
                <label className="text-sm font-medium text-slate-700">Name</label>
                <input
                  className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. customer_support_agent"
                />
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700">Description</label>
                <textarea
                  className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Purpose of this prompt..."
                  rows={2}
                />
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700">Content <span className="text-red-500">*</span></label>
                <textarea
                  className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm font-mono focus:border-brand-500 focus:outline-none bg-slate-50"
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  placeholder="You are a helpful assistant..."
                  rows={5}
                />
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700">Tags (comma separated)</label>
                <input
                  className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                  value={tags}
                  onChange={(e) => setTags(e.target.value)}
                  placeholder="support, chat, v1"
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
                  onClick={createPrompt}
                >
                  Create Prompt
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="p-4 border-b border-slate-100 bg-slate-50/50">
            <h3 className="font-medium text-slate-900">Prompt Registry</h3>
          </div>
          <DataTable
            data={prompts}
            columns={[
              { key: "name", header: "Name", render: (row) => <Link to={`/prompts/${row.id}`} className="font-medium text-brand-600 hover:text-brand-800">{row.name}</Link> },
              {
                key: "scope", header: "Scope", render: (row) => (
                  <span className={`text-xs font-bold uppercase px-2 py-1 rounded ${row.scope === 'global' ? 'bg-purple-100 text-purple-700' : 'bg-slate-100 text-slate-600'}`}>{row.scope}</span>
                )
              },
              { key: "project_id", header: "Project", render: (row) => projects.find(p => p.id === row.project_id)?.name || row.project_id }
            ]}
          />
        </div>
      </div>
    </Layout>
  );
};
