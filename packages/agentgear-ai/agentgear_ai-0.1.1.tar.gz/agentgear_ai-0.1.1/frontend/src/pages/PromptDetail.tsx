import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { DataTable } from "../components/DataTable";
import { Layout } from "../components/Layout";
import { api } from "../lib/api";

type Prompt = { id: string; name: string; description?: string };
type Version = { id: string; version: number; content: string; created_at: string };

export const PromptDetailPage = () => {
  const { id } = useParams();
  const [prompt, setPrompt] = useState<Prompt | null>(null);
  const [versions, setVersions] = useState<Version[]>([]);
  const [content, setContent] = useState("");

  const load = async () => {
    if (!id) return;
    const [pRes, vRes] = await Promise.all([
      api.get<Prompt>(`/api/prompts/${id}`),
      api.get<Version[]>(`/api/prompts/${id}/versions`)
    ]);
    setPrompt(pRes.data);
    setVersions(vRes.data);
  };

  useEffect(() => {
    load();
  }, [id]);

  const createVersion = async () => {
    if (!id || !content) return;
    await api.post(`/api/prompts/${id}/versions`, { content });
    setContent("");
    await load();
  };

  if (!prompt) return <Layout>Loading...</Layout>;

  return (
    <Layout>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">{prompt.name}</h1>
          <p className="text-sm text-slate-600">{prompt.description}</p>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-1 gap-6 md:grid-cols-[1.1fr_1fr]">
        <div>
          <DataTable
            data={versions}
            columns={[
              { key: "version", header: "Version" },
              { key: "content", header: "Content" },
              { key: "created_at", header: "Created" }
            ]}
          />
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">Add Version</h2>
          <textarea
            className="mt-3 h-40 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Enter prompt content"
          />
          <button
            className="mt-3 w-full rounded bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
            onClick={createVersion}
          >
            Save Version
          </button>
        </div>
      </div>
    </Layout>
  );
};
