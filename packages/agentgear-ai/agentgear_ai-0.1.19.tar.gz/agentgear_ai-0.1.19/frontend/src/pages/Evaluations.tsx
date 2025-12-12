import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { DataTable } from "../components/DataTable";
import { Layout } from "../components/Layout";
import { api } from "../lib/api";

type Evaluator = {
    id: string;
    name: string;
    model: string;
    prompt_template: string;
    created_at: string
};

export const EvaluationsPage = () => {
    const [evaluators, setEvaluators] = useState<Evaluator[]>([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);

    // Form State
    const [name, setName] = useState("");
    const [model, setModel] = useState("gpt-4-turbo"); // Default
    const [prompt, setPrompt] = useState("You are an expert judge. Review the following interaction:\nInput: {{input}}\nOutput: {{output}}\n\nRate the output on a scale of 0 to 1 based on accuracy. Respond with the number only.");

    const load = async () => {
        try {
            const res = await api.get<Evaluator[]>("/api/evaluators");
            setEvaluators(res.data);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        load();
    }, []);

    const createEvaluator = async () => {
        if (!name || !prompt) return;
        try {
            await api.post("/api/evaluators", {
                name,
                model,
                prompt_template: prompt,
                config: { temperature: 0 }
            });
            setShowModal(false);
            setName("");
            load();
        } catch (e) {
            alert("Failed to create evaluator");
        }
    };

    return (
        <Layout>
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-2xl font-semibold text-slate-900">Evaluators</h1>
                    <p className="text-sm text-slate-600">Manage LLM-as-a-Judge templates for automated testing.</p>
                </div>
                <button
                    onClick={() => setShowModal(true)}
                    className="rounded-md bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
                >
                    New Evaluator 🤖
                </button>
            </div>

            <div className="rounded-lg border border-slate-200 bg-white shadow-sm">
                <DataTable
                    data={evaluators}
                    isLoading={loading}
                    columns={[
                        { key: "name", header: "Name", render: (e) => <div className="font-medium text-slate-900">{e.name}</div> },
                        { key: "model", header: "Model" },
                        { key: "prompt_template", header: "Prompt Template", render: (e) => <div className="truncate max-w-xs text-xs font-mono text-slate-500">{e.prompt_template}</div> },
                        { key: "created_at", header: "Created" },
                    ]}
                />
            </div>

            {showModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
                    <div className="w-full max-w-2xl rounded-lg bg-white p-6 shadow-xl">
                        <h2 className="mb-4 text-lg font-semibold">New LLM Judge</h2>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-700">Name</label>
                                <input
                                    className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
                                    placeholder="Hallucination Detector"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700">Model</label>
                                <select
                                    className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
                                    value={model}
                                    onChange={(e) => setModel(e.target.value)}
                                >
                                    <option value="gpt-4-turbo">GPT-4 Turbo</option>
                                    <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                                    <option value="claude-3-opus">Claude 3 Opus</option>
                                    <option value="claude-3-sonnet">Claude 3 Sonnet</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700">Prompt Template</label>
                                <p className="text-xs text-slate-500 mb-2">Use <code>{`{{input}}`}</code> and <code>{`{{output}}`}</code> variables.</p>
                                <textarea
                                    className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm font-mono h-40"
                                    value={prompt}
                                    onChange={(e) => setPrompt(e.target.value)}
                                />
                            </div>
                        </div>
                        <div className="mt-6 flex justify-end gap-3">
                            <button
                                onClick={() => setShowModal(false)}
                                className="rounded-md px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-50"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={createEvaluator}
                                disabled={!name || !prompt}
                                className="rounded-md bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-50"
                            >
                                Create Evaluator
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </Layout>
    );
};
