import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Layout } from "../components/Layout";
import { api } from "../lib/api";
import { DataTable } from "../components/DataTable";

type Project = {
    id: string;
    name: string;
};

type Run = {
    id: string;
    name?: string;
    created_at: string;
    latency_ms?: number;
    cost?: number;
};

type Prompt = {
    id: string;
    name: string;
};

export const DashboardPage = () => {
    const [stats, setStats] = useState({
        projects: 0,
        runs: 0,
        prompts: 0,
    });
    const [recentRuns, setRecentRuns] = useState<Run[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const load = async () => {
            try {
                const [projectsRes, runsRes, promptsRes] = await Promise.all([
                    api.get<Project[]>("/api/projects"),
                    api.get<Run[]>("/api/runs"),
                    api.get<Prompt[]>("/api/prompts"),
                ]);

                setStats({
                    projects: projectsRes.data.length,
                    runs: runsRes.data.length,
                    prompts: promptsRes.data.length,
                });

                // Use the fetched runs directly since we have them
                setRecentRuns(runsRes.data.slice(0, 5));
            } catch (error) {
                console.error("Failed to load dashboard data", error);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, []);

    return (
        <Layout>
            <div className="mb-8">
                <h1 className="text-2xl font-semibold text-slate-900">Dashboard</h1>
                <p className="text-sm text-slate-600">Overview of your AgentGear workspace.</p>
            </div>

            <div className="grid grid-cols-1 gap-6 sm:grid-cols-3 mb-8">
                <StatCard label="Projects" value={stats.projects} to="/projects" />
                <StatCard label="Total Runs" value={stats.runs} to="/runs" />
                <StatCard label="Prompts" value={stats.prompts} to="/prompts" />
            </div>

            {/* Tip of the day */}
            <div className="mb-8 rounded-xl border border-blue-100 bg-blue-50 p-4 animate-slide-up" style={{ animationDelay: "0.2s" }}>
                <div className="flex items-center justify-between">
                    <div className="flex items-start gap-3">
                        <div className="flex-shrink-0 text-blue-600 mt-0.5">
                            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        </div>
                        <div>
                            <h3 className="text-sm font-semibold text-blue-900">Pro Tip</h3>
                            <p className="text-sm text-blue-700 mt-1">
                                Did you know you can version your prompts? Use the SDK to register prompt versions.
                                Check out the <Link to="/guide" className="underline hover:text-blue-900">Documentation</Link>.
                            </p>
                        </div>
                    </div>
                    {stats.projects === 0 && (
                        <button
                            onClick={async () => {
                                api.post("/api/seed");
                                window.location.reload();
                            }}
                            className="hidden sm:block whitespace-nowrap rounded bg-blue-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-blue-700 shadow-sm transition-colors"
                        >
                            + Load Example Data
                        </button>
                    )}
                </div>
            </div>

            <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold text-slate-900">Recent Runs</h2>
                    <Link to="/runs" className="text-sm font-medium text-brand-600 hover:text-brand-700">
                        View all
                    </Link>
                </div>
                {loading ? (
                    <div className="py-4 text-sm text-slate-500">Loading...</div>
                ) : recentRuns.length > 0 ? (
                    <DataTable
                        data={recentRuns}
                        columns={[
                            {
                                key: "name",
                                header: "Name",
                                render: (row) => <Link to={`/runs/${row.id}`}>{row.name || row.id}</Link>,
                            },
                            { key: "latency_ms", header: "Latency (ms)" },
                            { key: "cost", header: "Cost" },
                            { key: "created_at", header: "Created" },
                        ]}
                    />
                ) : (
                    <div className="py-4 text-center text-sm text-slate-500">
                        No runs recorded yet.
                    </div>
                )}
            </div>
        </Layout>
    );
};

const StatCard = ({ label, value, to }: { label: string; value: number; to: string }) => (
    <Link
        to={to}
        className="block rounded-lg border border-slate-200 bg-white p-6 shadow-sm transition hover:border-brand-300 hover:shadow-md"
    >
        <dt className="truncate text-sm font-medium text-slate-500">{label}</dt>
        <dd className="mt-1 text-3xl font-semibold tracking-tight text-slate-900">{value}</dd>
    </Link>
);
