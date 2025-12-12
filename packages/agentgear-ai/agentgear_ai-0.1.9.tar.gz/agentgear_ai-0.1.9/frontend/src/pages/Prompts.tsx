import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { DataTable } from "../components/DataTable";
import { Layout } from "../components/Layout";
import { api } from "../lib/api";

type Prompt = { id: string; name: string; project_id: string };

export const PromptsPage = () => {
  const [prompts, setPrompts] = useState<Prompt[]>([]);

  const load = async () => {
    const res = await api.get<Prompt[]>("/api/prompts");
    setPrompts(res.data);
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <Layout>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Prompts</h1>
          <p className="text-sm text-slate-600">Manage prompt registry and versions.</p>
        </div>
      </div>
      <div className="mt-4">
        <DataTable
          data={prompts}
          columns={[
            { key: "name", header: "Name", render: (row) => <Link to={`/prompts/${row.id}`}>{row.name}</Link> },
            { key: "project_id", header: "Project" }
          ]}
        />
      </div>
    </Layout>
  );
};
