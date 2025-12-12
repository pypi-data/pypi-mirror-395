import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Layout } from "../components/Layout";
import { api } from "../lib/api";
import { DataTable } from "../components/DataTable";

type Project = {
    id: string;
    name: string;
    description?: string;
};

export const ApiManagementPage = () => {
    const [projects, setProjects] = useState<Project[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const load = async () => {
            try {
                const res = await api.get<Project[]>("/api/projects");
                setProjects(res.data);
            } catch (error) {
                console.error("Failed to load projects", error);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, []);

    return (
        <Layout>
            <div className="mb-6">
                <h1 className="text-2xl font-semibold text-slate-900">API Management</h1>
                <p className="text-sm text-slate-600">Select a project to manage its API keys and tokens.</p>
            </div>

            <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                {loading ? (
                    <div className="py-4 text-sm text-slate-500">Loading...</div>
                ) : projects.length > 0 ? (
                    <DataTable
                        data={projects}
                        columns={[
                            {
                                key: "name",
                                header: "Project Name",
                                render: (row) => <span className="font-medium text-slate-900">{row.name}</span>,
                            },
                            { key: "description", header: "Description" },
                            {
                                key: "id", // Using ID as key for the action column
                                header: "Actions",
                                render: (row) => (
                                    <Link
                                        to={`/projects/${row.id}/tokens`}
                                        className="inline-flex items-center rounded bg-brand-50 px-3 py-2 text-xs font-medium text-brand-700 hover:bg-brand-100"
                                    >
                                        Manage Keys
                                    </Link>
                                ),
                            },
                        ]}
                    />
                ) : (
                    <div className="py-8 text-center">
                        <p className="text-sm text-slate-500">No projects found.</p>
                        <Link
                            to="/projects"
                            className="mt-2 inline-block text-sm font-medium text-brand-600 hover:text-brand-700"
                        >
                            Create a project first
                        </Link>
                    </div>
                )}
            </div>
        </Layout>
    );
};
