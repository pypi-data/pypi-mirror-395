import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { DataTable } from "../components/DataTable";
import { Layout } from "../components/Layout";
import { api } from "../lib/api";

type Dataset = { id: string; name: string; description?: string; tags?: string[]; created_at: string };

export const DatasetsPage = () => {
    const [datasets, setDatasets] = useState<Dataset[]>([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [newName, setNewName] = useState("");
    const [newDesc, setNewDesc] = useState("");

    const load = async () => {
        try {
            const res = await api.get<Dataset[]>("/api/datasets");
            setDatasets(res.data);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        load();
    }, []);

    const createDataset = async () => {
        if (!newName) return;
        await api.post("/api/datasets", { name: newName, description: newDesc });
        setShowModal(false);
        setNewName("");
        setNewDesc("");
        load();
    };

    return (
        <Layout>
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-semibold text-slate-900">Datasets</h1>
                    <p className="text-sm text-slate-600">Manage test datasets for your prompts and models.</p>
                </div>
                <button
                    onClick={() => setShowModal(true)}
                    className="rounded-md bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
                >
                    New Dataset 📚
                </button>
            </div>

            <div className="mt-6 rounded-lg border border-slate-200 bg-white shadow-sm">
                <DataTable
                    data={datasets}
                    isLoading={loading}
                    onRowClick={(row) => window.location.href = `/datasets/${row.id}`}
                    columns={[
                        { key: "name", header: "Name", render: (d) => <Link to={`/datasets/${d.id}`} className="font-medium text-brand-600 hover:underline">{d.name}</Link> },
                        { key: "description", header: "Description" },
                        { key: "tags", header: "Tags", render: (d) => d.tags?.join(", ") },
                        { key: "created_at", header: "Created" },
                    ]}
                />
            </div>

            {/* Simple Modal */}
            {showModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
                    <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-xl">
                        <h2 className="mb-4 text-lg font-semibold">New Dataset</h2>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-700">Name</label>
                                <input
                                    className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                                    value={newName}
                                    onChange={(e) => setNewName(e.target.value)}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700">Description</label>
                                <textarea
                                    className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                                    value={newDesc}
                                    onChange={(e) => setNewDesc(e.target.value)}
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
                                onClick={createDataset}
                                disabled={!newName}
                                className="rounded-md bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-50"
                            >
                                Create
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </Layout>
    );
};
