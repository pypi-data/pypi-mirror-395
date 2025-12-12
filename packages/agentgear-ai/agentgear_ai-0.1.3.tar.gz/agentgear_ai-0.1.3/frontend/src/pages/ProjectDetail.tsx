import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Layout } from "../components/Layout";
import { StatCards } from "../components/StatCards";
import { api } from "../lib/api";

type Project = { id: string; name: string; description?: string };
type Token = { id: string; revoked: boolean; last_used_at?: string };
type Prompt = { id: string; name: string };
type Run = { id: string; name?: string; created_at: string };

export const ProjectDetailPage = () => {
  const { id } = useParams();
  const [project, setProject] = useState<Project | null>(null);
  const [tokens, setTokens] = useState<Token[]>([]);
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [runs, setRuns] = useState<Run[]>([]);

  const load = async () => {
    if (!id) return;
    const [pRes, tRes, prRes, rRes] = await Promise.all([
      api.get<Project>(`/api/projects/${id}`),
      api.get<Token[]>(`/api/projects/${id}/tokens`),
      api.get<Prompt[]>(`/api/prompts`, { params: { project_id: id } }),
      api.get<Run[]>(`/api/runs`, { params: { project_id: id } })
    ]);
    setProject(pRes.data);
    setTokens(tRes.data);
    setPrompts(prRes.data);
    setRuns(rRes.data);
  };

  useEffect(() => {
    load();
  }, [id]);

  if (!project) return <Layout>Loading...</Layout>;

  return (
    <Layout>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">{project.name}</h1>
          <p className="text-sm text-slate-600">{project.description}</p>
        </div>
        <Link
          to={`/projects/${project.id}/tokens`}
          className="rounded bg-brand-600 px-3 py-2 text-sm font-semibold text-white hover:bg-brand-700"
        >
          Manage Tokens
        </Link>
      </div>

      <div className="mt-6">
        <StatCards
          stats={[
            { label: "Prompts", value: prompts.length },
            { label: "Runs", value: runs.length },
            { label: "Tokens", value: tokens.length },
            {
              label: "Active Tokens",
              value: tokens.filter((t) => !t.revoked).length
            }
          ]}
        />
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-2">
        <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <div className="mb-2 text-sm font-semibold text-slate-800">Prompts</div>
          <ul className="space-y-2 text-sm">
            {prompts.map((p) => (
              <li key={p.id}>
                <Link to={`/prompts/${p.id}`} className="text-brand-700 hover:underline">
                  {p.name}
                </Link>
              </li>
            ))}
            {!prompts.length && <li className="text-slate-500">No prompts yet.</li>}
          </ul>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <div className="mb-2 text-sm font-semibold text-slate-800">Recent Runs</div>
          <ul className="space-y-2 text-sm">
            {runs.slice(0, 5).map((r) => (
              <li key={r.id}>
                <Link to={`/runs/${r.id}`} className="text-brand-700 hover:underline">
                  {r.name || r.id}
                </Link>
                <div className="text-xs text-slate-500">{r.created_at}</div>
              </li>
            ))}
            {!runs.length && <li className="text-slate-500">No runs yet.</li>}
          </ul>
        </div>
      </div>
    </Layout>
  );
};
