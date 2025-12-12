import { useEffect, useState } from "react";
import { Layout } from "../components/Layout";
import { api } from "../lib/api";
import { DataTable } from "../components/DataTable";

type LLMModel = {
    id: string;
    name: string;
    provider: string;
    base_url?: string;
    created_at: string;
};

export const ModelsPage = () => {
    const [models, setModels] = useState<LLMModel[]>([]);
    const [loading, setLoading] = useState(true);

    // Form
    const [name, setName] = useState("");
    const [provider, setProvider] = useState("openai");
    const [apiKey, setApiKey] = useState("");
    const [baseUrl, setBaseUrl] = useState("");

    const [showForm, setShowForm] = useState(false);

    const load = async () => {
        try {
            const res = await api.get<LLMModel[]>("/api/models");
            setModels(res.data);
        } catch (error) {
            console.error("Failed to load models", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        load();
    }, []);

    const createModel = async () => {
        if (!name || !provider) return;
        try {
            await api.post("/api/models", { name, provider, api_key: apiKey, base_url: baseUrl });
            setName("");
            setApiKey("");
            setBaseUrl("");
            setShowForm(false);
            load();
        } catch (e) {
            alert("Failed to add model");
        }
    };

    const deleteModel = async (id: string) => {
        if (!confirm("Are you sure?")) return;
        await api.delete(`/api/models/${id}`);
        load();
    }

    return (
        <Layout>
            <div className="mb-6 flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-semibold text-slate-900">Model Management</h1>
                    <p className="text-sm text-slate-600">Centralized configuration for LLM providers.</p>
                </div>
                <button
                    onClick={() => setShowForm(!showForm)}
                    className="rounded bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700 shadow-sm"
                >
                    {showForm ? "Cancel" : "+ New Model"}
                </button>
            </div>

            {/* Tip */}
            <div className="mb-6 rounded-lg border border-purple-100 bg-purple-50 p-4">
                <div className="flex items-start gap-3">
                    <span className="text-purple-500">🧠</span>
                    <div className="text-sm text-purple-800">
                        <strong>Did you know?</strong> Models configured here can be automatically fetched by the AgentGear SDK. This allows you to rotate keys or switch providers without redeploying your agents.
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 gap-6">
                {showForm && (
                    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm max-w-lg mb-6 animate-slide-up">
                        <h2 className="text-lg font-semibold text-slate-900 mb-4">Add Model</h2>
                        <div className="space-y-4">
                            <div>
                                <label className="text-sm font-medium text-slate-700">Model Name</label>
                                <input
                                    placeholder="e.g. gpt-4-turbo"
                                    className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                />
                            </div>
                            <div>
                                <label className="text-sm font-medium text-slate-700">Provider</label>
                                <select
                                    className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                                    value={provider}
                                    onChange={(e) => setProvider(e.target.value)}
                                >
                                    <option value="openai">OpenAI</option>
                                    <option value="anthropic">Anthropic</option>
                                    <option value="google">Google Vertex/Gemini</option>
                                    <option value="azure">Azure OpenAI</option>
                                    <option value="custom">Custom / Local</option>
                                </select>
                            </div>
                            <div>
                                <label className="text-sm font-medium text-slate-700">API Key</label>
                                <input
                                    type="password"
                                    placeholder="sk-..."
                                    className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                                    value={apiKey}
                                    onChange={(e) => setApiKey(e.target.value)}
                                />
                            </div>
                            <div>
                                <label className="text-sm font-medium text-slate-700">Base URL (Optional)</label>
                                <input
                                    placeholder="https://api.openai.com/v1"
                                    className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                                    value={baseUrl}
                                    onChange={(e) => setBaseUrl(e.target.value)}
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
                                    onClick={createModel}
                                >
                                    Save Configuration
                                </button>
                            </div>
                        </div>
                    </div>
                )}

                <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
                    <div className="p-4 border-b border-slate-100 bg-slate-50/50">
                        <h3 className="font-medium text-slate-900">Configured Models</h3>
                    </div>
                    {loading ? (
                        <div className="p-4 text-sm text-slate-500">Loading...</div>
                    ) : (
                        <DataTable
                            data={models}
                            columns={[
                                { key: "name", header: "Name" },
                                { key: "provider", header: "Provider" },
                                { key: "base_url", header: "Base URL" },
                                {
                                    key: "id", header: "", render: (row) => (
                                        <button onClick={() => deleteModel(row.id)} className="text-red-600 hover:text-red-800 text-xs font-semibold">Delete</button>
                                    )
                                }
                            ]}
                        />
                    )}
                </div>
            </div>
        </Layout>
    );
};
