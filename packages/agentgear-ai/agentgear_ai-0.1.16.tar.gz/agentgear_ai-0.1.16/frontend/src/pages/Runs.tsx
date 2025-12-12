import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { DataTable } from "../components/DataTable";
import { Layout } from "../components/Layout";
import { api } from "../lib/api";

type Run = {
  id: string;
  name?: string;
  project_id: string;
  latency_ms?: number;
  cost?: number;
  created_at: string;
};

export const RunsPage = () => {
  const [runs, setRuns] = useState<Run[]>([]);

  const load = async () => {
    const res = await api.get<Run[]>("/api/runs");
    setRuns(res.data);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <Layout>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Runs</h1>
          <p className="text-sm text-slate-600">Observability for LLM calls and agent workflows.</p>
        </div>
      </div>
      <div className="mt-4">
        <DataTable
          data={runs}
          columns={[
            { key: "name", header: "Name", render: (row) => <Link to={`/runs/${row.id}`}>{row.name || row.id}</Link> },
            { key: "project_id", header: "Project" },
            { key: "latency_ms", header: "Latency (ms)" },
            { key: "cost", header: "Cost" },
            { key: "created_at", header: "Created" }
          ]}
        />
      </div>
    </Layout>
  );
};
