import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { DataTable } from "../components/DataTable";
import { Layout } from "../components/Layout";
import { TokenModal } from "../components/TokenModal";
import { api } from "../lib/api";

type Token = {
  id: string;
  revoked: boolean;
  scopes: string[];
  created_at: string;
  last_used_at?: string;
};

export const TokensPage = () => {
  const { id } = useParams();
  const [tokens, setTokens] = useState<Token[]>([]);
  const [newToken, setNewToken] = useState<string | null>(null);
  const [scopes, setScopes] = useState("runs.write prompts.read");

  const load = async () => {
    if (!id) return;
    const res = await api.get<Token[]>(`/api/projects/${id}/tokens`);
    setTokens(res.data);
  };

  useEffect(() => {
    load();
  }, [id]);

  const createToken = async () => {
    if (!id) return;
    const scopesList = scopes.split(" ").filter(Boolean);
    const res = await api.post(`/api/projects/${id}/tokens`, { scopes: scopesList });
    setNewToken(res.data.token);
    await load();
  };

  const revoke = async (tokenId: string) => {
    if (!id) return;
    await api.delete(`/api/projects/${id}/tokens/${tokenId}`);
    await load();
  };

  return (
    <Layout>
      <TokenModal token={newToken} onClose={() => setNewToken(null)} />
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">API Tokens</h1>
          <p className="text-sm text-slate-600">Generate and revoke project API keys.</p>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-1 gap-6 md:grid-cols-[1.2fr_1fr]">
        <DataTable
          data={tokens}
          columns={[
            { key: "id", header: "Token ID" },
            { key: "scopes", header: "Scopes", render: (row) => row.scopes.join(", ") },
            { key: "created_at", header: "Created" },
            { key: "last_used_at", header: "Last Used" },
            {
              key: "revoked",
              header: "Status",
              render: (row) =>
                row.revoked ? (
                  <span className="rounded bg-slate-200 px-2 py-1 text-xs text-slate-700">Revoked</span>
                ) : (
                  <button
                    className="text-sm font-medium text-red-600 hover:underline"
                    onClick={() => revoke(row.id)}
                  >
                    Revoke
                  </button>
                )
            }
          ]}
        />

        <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">Create Token</h2>
          <p className="mt-1 text-sm text-slate-600">
            Provide space-separated scopes (e.g. runs.write prompts.read).
          </p>
          <div className="mt-3 space-y-3">
            <input
              className="w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
              value={scopes}
              onChange={(e) => setScopes(e.target.value)}
            />
            <button
              className="w-full rounded bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
              onClick={createToken}
            >
              Generate Token
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
};
