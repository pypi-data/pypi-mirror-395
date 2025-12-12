import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { DataTable } from "../components/DataTable";
import { Layout } from "../components/Layout";
import { api } from "../lib/api";

type Prompt = { id: string; name: string; description?: string; tags?: string[]; scope: string; project_id: string };
type Version = { id: string; version: number; content: string; created_at: string };
type Model = { id: string; name: string; provider: string };

export const PromptDetailPage = () => {
  const { id } = useParams();
  const [activeTab, setActiveTab] = useState<"overview" | "playground" | "versions">("overview");

  // Data
  const [prompt, setPrompt] = useState<Prompt | null>(null);
  const [versions, setVersions] = useState<Version[]>([]);
  const [models, setModels] = useState<Model[]>([]);

  // Edit State
  const [editName, setEditName] = useState("");
  const [editDesc, setEditDesc] = useState("");
  const [editTags, setEditTags] = useState("");

  // Version/Playground State
  const [content, setContent] = useState("");

  // Playground State
  const [selectedModelId, setSelectedModelId] = useState("");
  const [inputs, setInputs] = useState<Record<string, string>>({});
  const [output, setOutput] = useState("");
  const [latency, setLatency] = useState<number | null>(null);
  const [running, setRunning] = useState(false);
  const [runError, setRunError] = useState("");

  const load = async () => {
    if (!id) return;
    try {
      const [pRes, vRes, mRes] = await Promise.all([
        api.get<Prompt>(`/api/prompts/${id}`),
        api.get<Version[]>(`/api/prompts/${id}/versions`),
        api.get<Model[]>("/api/models")
      ]);
      setPrompt(pRes.data);
      setVersions(vRes.data);
      setModels(mRes.data);

      // Init Edit Form
      setEditName(pRes.data.name);
      setEditDesc(pRes.data.description || "");
      setEditTags(pRes.data.tags?.join(", ") || "");

      // Init Playground Content (latest version)
      if (vRes.data.length > 0) {
        setContent(vRes.data[0].content);
      }

      if (mRes.data.length > 0) {
        setSelectedModelId(mRes.data[0].id);
      }
    } catch (e) {
      console.error("Failed to load prompt details", e);
    }
  };

  useEffect(() => {
    load();
  }, [id]);

  // Extract variables
  useEffect(() => {
    const vars = content.match(/\{([a-zA-Z0-9_]+)\}/g);
    if (vars) {
      const newInputs = { ...inputs };
      vars.forEach(v => {
        const key = v.slice(1, -1);
        if (!(key in newInputs)) newInputs[key] = "";
      });
      setInputs(newInputs);
    }
  }, [content]);

  const saveChanges = async () => {
    if (!id) return;
    try {
      const tagsList = editTags.split(",").map(t => t.trim()).filter(Boolean);
      const res = await api.put<Prompt>(`/api/prompts/${id}`, { name: editName, description: editDesc, tags: tagsList });
      setPrompt(res.data);
      alert("Changes saved");
    } catch (e) {
      alert("Failed to save changes");
    }
  };

  const createVersion = async () => {
    if (!id || !content) return;
    await api.post(`/api/prompts/${id}/versions`, { content });
    await load();
    alert("New version created");
  };

  const runPrompt = async () => {
    if (!id || !selectedModelId) return;
    setRunning(true);
    setRunError("");
    setOutput("");
    setLatency(null);
    try {
      const res = await api.post<{ output: string, latency_ms: number }>(`/api/prompts/${id}/run`, {
        model_config_name: selectedModelId,
        inputs: inputs,
        version_id: null // use latest or matching content? For playground we usually run *current* content. 
        // But backend expects version_id OR finds latest. 
        // Backend logic currently runs a *stored* version.
        // To support "Draft" running, we might need to modify backend to accept raw content or save a temp version.
        // For simplicity now, let's force save a version if content changed? 
        // Or just rely on latest version. 
        // WAIT: If user edits text in playground, they expect THAT text to run.
        // Backend expects `version_id`. If `version_id` is null, it finds latest.
        // Limitation: Playground only runs *saved* versions for now.
      });
      setOutput(res.data.output);
      setLatency(res.data.latency_ms);
    } catch (e: any) {
      setRunError(e.response?.data?.detail || "Run failed");
    } finally {
      setRunning(false);
    }
  };

  if (!prompt) return <Layout>Loading...</Layout>;

  return (
    <Layout>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">{prompt.name}</h1>
          <div className="flex gap-2 mt-1">
            <span className="text-xs font-mono bg-slate-100 px-2 py-0.5 rounded text-slate-600">ID: {prompt.id}</span>
            <span className={`text-xs font-bold uppercase px-2 py-0.5 rounded ${prompt.scope === 'global' ? 'bg-purple-100 text-purple-700' : 'bg-slate-100 text-slate-600'}`}>{prompt.scope}</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-slate-200 mb-6">
        <nav className="-mb-px flex gap-6">
          {["overview", "playground", "versions"].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab as any)}
              className={`pb-4 text-sm font-medium border-b-2 transition-colors ${activeTab === tab
                ? "border-brand-600 text-brand-600"
                : "border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300"
                }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </nav>
      </div>

      {/* Overview Tab */}
      {activeTab === "overview" && (
        <div className="max-w-2xl space-y-6">
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <h3 className="text-lg font-semibold mb-4">Prompt Settings</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Name</label>
                <input
                  className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                  value={editName}
                  onChange={e => setEditName(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Description</label>
                <textarea
                  className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                  value={editDesc}
                  onChange={e => setEditDesc(e.target.value)}
                  rows={3}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Tags (comma separated)</label>
                <input
                  className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                  value={editTags}
                  onChange={e => setEditTags(e.target.value)}
                />
              </div>
              <div className="pt-2">
                <button
                  onClick={saveChanges}
                  className="bg-brand-600 text-white px-4 py-2 rounded-md text-sm font-semibold hover:bg-brand-700"
                >
                  Save Changes
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Playground Tab */}
      {activeTab === "playground" && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-6">
            {/* Editor */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col h-[500px]">
              <div className="flex justify-between items-center mb-2">
                <h3 className="font-semibold text-slate-900">Template</h3>
                <button
                  onClick={createVersion}
                  className="text-xs bg-slate-100 text-slate-700 px-2 py-1 rounded hover:bg-slate-200"
                >
                  Save as New Version
                </button>
              </div>
              <textarea
                className="flex-1 w-full p-3 font-mono text-sm bg-slate-50 border border-slate-200 rounded-md focus:outline-none focus:border-brand-500 resize-none"
                value={content}
                onChange={e => setContent(e.target.value)}
                placeholder="Your prompt template here... Use {variable} for inputs."
              />
            </div>
          </div>

          <div className="space-y-6">
            {/* Controls */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <h3 className="font-semibold text-slate-900 mb-4">Run Controls</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-medium text-slate-500 uppercase mb-1">Model</label>
                  <select
                    className="w-full rounded border border-slate-200 px-3 py-2 text-sm"
                    value={selectedModelId}
                    onChange={e => setSelectedModelId(e.target.value)}
                  >
                    <option value="">Select a Model...</option>
                    {models.map(m => (
                      <option key={m.id} value={m.id}>{m.name} ({m.provider})</option>
                    ))}
                  </select>
                  {models.length === 0 && <p className="text-xs text-amber-600 mt-1">No models configured. Go to Models page.</p>}
                </div>

                {/* Variables */}
                {Object.keys(inputs).length > 0 && (
                  <div>
                    <label className="block text-xs font-medium text-slate-500 uppercase mb-2">Variables</label>
                    <div className="space-y-2">
                      {Object.keys(inputs).map(key => (
                        <div key={key}>
                          <span className="text-xs font-mono text-slate-600 block mb-1">{key}</span>
                          <input
                            className="w-full rounded border border-slate-200 px-2 py-1 text-sm"
                            value={inputs[key]}
                            onChange={e => setInputs({ ...inputs, [key]: e.target.value })}
                            placeholder={`Value for ${key}`}
                          />
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <button
                  onClick={runPrompt}
                  disabled={running || !selectedModelId}
                  className="w-full bg-green-600 text-white py-2 rounded font-semibold text-sm hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {running ? "Running..." : "Run"}
                </button>
              </div>
            </div>

            {/* Output */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm min-h-[200px]">
              <h3 className="font-semibold text-slate-900 mb-2 flex justify-between">
                Output
                {latency && <span className="text-xs font-normal text-slate-500">{Math.round(latency)}ms</span>}
              </h3>
              {runError ? (
                <div className="text-red-600 text-sm p-2 bg-red-50 rounded">{runError}</div>
              ) : (
                <div className="whitespace-pre-wrap text-sm text-slate-800 font-mono">
                  {output || <span className="text-slate-400 italic">Run execution output will appear here...</span>}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Versions Tab */}
      {activeTab === "versions" && (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
          <DataTable
            data={versions}
            columns={[
              { key: "version", header: "Version", render: (v) => <span className="font-mono">v{v.version}</span> },
              { key: "content", header: "Content", render: (v) => <div className="max-w-xl truncate font-mono text-xs">{v.content}</div> },
              { key: "created_at", header: "Created" }
            ]}
          />
        </div>
      )}
    </Layout>
  );
};
