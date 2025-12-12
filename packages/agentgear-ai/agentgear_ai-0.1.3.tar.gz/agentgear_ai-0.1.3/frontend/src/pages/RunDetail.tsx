import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { DataTable } from "../components/DataTable";
import { Layout } from "../components/Layout";
import { api } from "../lib/api";

type Run = {
  id: string;
  name?: string;
  input_text?: string;
  output_text?: string;
  latency_ms?: number;
  cost?: number;
  created_at: string;
};

type Span = {
  id: string;
  name: string;
  parent_id?: string;
  latency_ms?: number;
  metadata?: Record<string, any>;
};

export const RunDetailPage = () => {
  const { id } = useParams();
  const [run, setRun] = useState<Run | null>(null);
  const [spans, setSpans] = useState<Span[]>([]);

  const load = async () => {
    if (!id) return;
    const [rRes, sRes] = await Promise.all([
      api.get<Run>(`/api/runs/${id}`),
      api.get<Span[]>(`/api/spans`, { params: { run_id: id } })
    ]);
    setRun(rRes.data);
    setSpans(sRes.data);
  };

  useEffect(() => {
    load();
  }, [id]);

  if (!run) return <Layout>Loading...</Layout>;

  return (
    <Layout>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">{run.name || run.id}</h1>
          <p className="text-sm text-slate-600">Run ID: {run.id}</p>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
        <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <h2 className="text-sm font-semibold text-slate-800">Input</h2>
          <pre className="mt-2 whitespace-pre-wrap text-sm text-slate-700">
            {run.input_text || "N/A"}
          </pre>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <h2 className="text-sm font-semibold text-slate-800">Output</h2>
          <pre className="mt-2 whitespace-pre-wrap text-sm text-slate-700">
            {run.output_text || "N/A"}
          </pre>
        </div>
      </div>

      <div className="mt-4 rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <h3 className="text-sm font-semibold text-slate-800">Spans</h3>
        <div className="mt-2">
          <DataTable
            data={spans}
            columns={[
              { key: "name", header: "Name" },
              { key: "parent_id", header: "Parent" },
              { key: "latency_ms", header: "Latency (ms)" },
              { key: "metadata", header: "Metadata", render: (row) => JSON.stringify(row.metadata || {}) }
            ]}
          />
        </div>
      </div>
    </Layout>
  );
};
