import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { DataTable } from "../components/DataTable";
import { Layout } from "../components/Layout";
import { api } from "../lib/api";

type Dataset = { id: string; name: string; description?: string };
type Example = { id: string; input_text: string; expected_output: string; created_at: string };

export const DatasetDetailPage = () => {
    const { id } = useParams();
    const [dataset, setDataset] = useState<Dataset | null>(null);
    const [examples, setExamples] = useState<Example[]>([]);

    // Add Example State
    const [input, setInput] = useState("");
    const [output, setOutput] = useState("");

    const load = async () => {
        if (!id) return;
        const [dRes, eRes] = await Promise.all([
            api.get<Dataset>(`/api/datasets/${id}`),
            api.get<Example[]>(`/api/datasets/${id}/examples`)
        ]);
        setDataset(dRes.data);
        setExamples(eRes.data);
    };

    useEffect(() => {
        load();
    }, [id]);

    const addExample = async () => {
        if (!id || !input) return;
        await api.post(`/api/datasets/${id}/examples`, { input_text: input, expected_output: output });
        setInput("");
        setOutput("");
        load();
    };

    const deleteExample = async (exampleId: string) => {
        if (!id) return;
        if (!confirm("Delete this example?")) return;
        await api.delete(`/api/datasets/${id}/examples/${exampleId}`);
        load();
    }

    if (!dataset) return <Layout>Loading...</Layout>;

    return (
        <Layout>
            <div className="mb-6">
                <h1 className="text-2xl font-bold text-slate-900">{dataset.name}</h1>
                <p className="text-slate-600">{dataset.description}</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-[1fr_350px] gap-8">
                <div>
                    <div className="bg-white rounded-lg border border-slate-200">
                        <DataTable
                            data={examples}
                            columns={[
                                { key: "input_text", header: "Input", render: (e) => <pre className="text-xs whitespace-pre-wrap font-mono">{e.input_text}</pre> },
                                { key: "expected_output", header: "Expected Output", render: (e) => <pre className="text-xs whitespace-pre-wrap font-mono">{e.expected_output}</pre> },
                                {
                                    key: "id", header: "Actions", render: (e) => (
                                        <button onClick={(ev) => { ev.stopPropagation(); deleteExample(e.id); }} className="text-red-600 hover:text-red-800 text-xs">Delete</button>
                                    )
                                }
                            ]}
                        />
                    </div>
                </div>

                <div className="bg-white p-4 rounded-lg border border-slate-200 h-fit">
                    <h3 className="font-semibold mb-4">Add Example</h3>
                    <div className="space-y-4">
                        <div>
                            <label className="block text-xs font-medium text-slate-500 uppercase mb-1">Input</label>
                            <textarea
                                className="w-full rounded border border-slate-200 px-3 py-2 text-sm h-24"
                                value={input}
                                onChange={e => setInput(e.target.value)}
                                placeholder="User: Hello?"
                            />
                        </div>
                        <div>
                            <label className="block text-xs font-medium text-slate-500 uppercase mb-1">Expected Output</label>
                            <textarea
                                className="w-full rounded border border-slate-200 px-3 py-2 text-sm h-24"
                                value={output}
                                onChange={e => setOutput(e.target.value)}
                                placeholder="Assistant: Hi there! How can I help?"
                            />
                        </div>
                        <button
                            onClick={addExample}
                            className="w-full bg-slate-900 text-white py-2 rounded font-medium text-sm hover:bg-slate-800"
                        >
                            Add Example
                        </button>
                    </div>
                </div>
            </div>
        </Layout>
    );
}
