import { useEffect, useState } from "react";
import { Layout } from "../components/Layout";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";

type Tab = "general" | "email" | "alerts" | "roles";

// --- GENERAL COMPONENT ---
const DatabaseInfo = () => {
    const [dbInfo, setDbInfo] = useState<{ url: string, type: string } | null>(null);
    useEffect(() => {
        api.get("/api/settings/database").then(res => setDbInfo(res.data));
    }, []);

    if (!dbInfo) return <div className="text-sm text-slate-400">Loading DB info...</div>;

    return (
        <div className="space-y-2">
            <div>
                <label className="block text-xs font-semibold text-slate-500 uppercase">Connection URL</label>
                <code className="text-sm bg-slate-100 px-2 py-1 rounded block mt-1 break-all">
                    {dbInfo.url}
                </code>
            </div>
            <div>
                <label className="block text-xs font-semibold text-slate-500 uppercase">Type</label>
                <div className="text-sm text-slate-700 font-medium capitalize">{dbInfo.type}</div>
            </div>
            <div className="text-xs text-orange-600 mt-2 bg-orange-50 p-2 rounded">
                To change the database, update the <code>AGENTGEAR_DATABASE_URL</code> environment variable and restart the server.
            </div>
        </div>
    );
}

// --- SMTP COMPONENT ---
const SmtpSettings = ({ projectId }: { projectId: string }) => {
    const [config, setConfig] = useState({ host: "", port: 587, username: "", password: "", sender_email: "", enabled: false });
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!projectId) return;
        api.get(`/api/settings/smtp?project_id=${projectId}`).then(res => setConfig(res.data)).catch(() => { });
    }, [projectId]);

    const save = async () => {
        setLoading(true);
        try {
            await api.post(`/api/settings/smtp?project_id=${projectId}`, config);
            alert("SMTP Settings Saved");
        } catch (e) {
            alert("Failed to save");
        }
        setLoading(false);
    };

    return (
        <div className="max-w-xl space-y-4">
            <h3 className="text-lg font-medium text-slate-900">Email Configuration (SMTP)</h3>
            <div className="grid grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-slate-700">Host</label>
                    <input className="mt-1 w-full rounded border px-3 py-2 text-sm" value={config.host} onChange={e => setConfig({ ...config, host: e.target.value })} placeholder="smtp.gmail.com" />
                </div>
                <div>
                    <label className="block text-sm font-medium text-slate-700">Port</label>
                    <input className="mt-1 w-full rounded border px-3 py-2 text-sm" value={config.port} onChange={e => setConfig({ ...config, port: parseInt(e.target.value) })} type="number" />
                </div>
                <div>
                    <label className="block text-sm font-medium text-slate-700">Username</label>
                    <input className="mt-1 w-full rounded border px-3 py-2 text-sm" value={config.username || ""} onChange={e => setConfig({ ...config, username: e.target.value })} />
                </div>
                <div>
                    <label className="block text-sm font-medium text-slate-700">Password</label>
                    <input className="mt-1 w-full rounded border px-3 py-2 text-sm" value={config.password || ""} onChange={e => setConfig({ ...config, password: e.target.value })} type="password" />
                </div>
                <div className="col-span-2">
                    <label className="block text-sm font-medium text-slate-700">Sender Email</label>
                    <input className="mt-1 w-full rounded border px-3 py-2 text-sm" value={config.sender_email || ""} onChange={e => setConfig({ ...config, sender_email: e.target.value })} placeholder="alerts@agentgear.ai" />
                </div>
            </div>
            <div className="flex items-center gap-2">
                <input type="checkbox" id="enabled" checked={config.enabled} onChange={e => setConfig({ ...config, enabled: e.target.checked })} />
                <label htmlFor="enabled" className="text-sm text-slate-700">Enable Email Notifications</label>
            </div>
            <button
                className="rounded bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-50"
                onClick={save}
                disabled={loading}
            >
                {loading ? "Saving..." : "Save Configuration"}
            </button>
            <button
                className="rounded text-brand-600 px-4 py-2 text-sm font-semibold hover:bg-brand-50"
                onClick={async () => {
                    const email = prompt("Enter recipient email:");
                    if (email) {
                        try {
                            await api.post(`/api/settings/smtp/test?project_id=${projectId}&recipient=${email}`, config);
                            alert("Test email sent!");
                        } catch (e) {
                            alert("Failed to send test email");
                        }
                    }
                }}
            >
                Test Email
            </button>
        </div>
    );
};

// --- ALERTS COMPONENT ---
const AlertsSettings = ({ projectId }: { projectId: string }) => {
    const [alerts, setAlerts] = useState<any[]>([]);
    const [newAlert, setNewAlert] = useState({ metric: "token_usage", threshold: 1000, recipients: "" });

    const load = () => api.get(`/api/settings/alerts?project_id=${projectId}`).then(res => setAlerts(res.data));

    useEffect(() => {
        if (projectId) load();
    }, [projectId]);

    const addAlert = async () => {
        if (!projectId) return;
        const recipientsList = newAlert.recipients.split(",").map(s => s.trim());
        await api.post("/api/settings/alerts", { ...newAlert, recipients: recipientsList, project_id: projectId });
        load();
    }

    const deleteAlert = async (id: string) => {
        await api.delete(`/api/settings/alerts/${id}`);
        load();
    }

    return (
        <div className="space-y-6">
            <div className="rounded-lg bg-orange-50 p-4 border border-orange-100 text-orange-800 text-sm">
                <strong>Alerts System:</strong> Define thresholds to get notified when your agents consume too many tokens or have high latency. Similar to LangFuse metrics.
            </div>

            <div className="rounded-lg border border-slate-200 bg-white p-4">
                <h4 className="font-medium text-slate-900 mb-4">Create New Alert</h4>
                <div className="grid grid-cols-4 gap-4 items-end">
                    <div>
                        <label className="block text-xs font-semibold text-slate-500 uppercase">Metric</label>
                        <select className="mt-1 w-full rounded border px-2 py-2 text-sm" value={newAlert.metric} onChange={e => setNewAlert({ ...newAlert, metric: e.target.value })}>
                            <option value="token_usage">Token Usage (Total)</option>
                            <option value="cost">Cost ($)</option>
                            <option value="latency">Latency (ms)</option>
                            <option value="error_rate">Error Rate (%)</option>
                        </select>
                    </div>
                    <div>
                        <label className="block text-xs font-semibold text-slate-500 uppercase">Threshold</label>
                        <input type="number" className="mt-1 w-full rounded border px-2 py-2 text-sm" value={newAlert.threshold} onChange={e => setNewAlert({ ...newAlert, threshold: parseFloat(e.target.value) })} />
                    </div>
                    <div>
                        <label className="block text-xs font-semibold text-slate-500 uppercase">Recipients (comma sep)</label>
                        <input className="mt-1 w-full rounded border px-2 py-2 text-sm" placeholder="admin@example.com" value={newAlert.recipients} onChange={e => setNewAlert({ ...newAlert, recipients: e.target.value })} />
                    </div>
                    <button onClick={addAlert} className="rounded bg-slate-900 text-white px-4 py-2 text-sm font-medium hover:bg-slate-800">Add Alert</button>
                </div>
            </div>

            <div className="space-y-2">
                {alerts.map(alert => (
                    <div key={alert.id} className="flex items-center justify-between p-4 bg-white border border-slate-200 rounded-lg shadow-sm">
                        <div className="text-sm">
                            <span className="font-bold text-slate-700 uppercase">{alert.metric}</span>
                            <span className="mx-2 text-slate-400">&gt;</span>
                            <span className="font-mono text-slate-900">{alert.threshold}</span>
                            <div className="text-xs text-slate-500 mt-1">Recipients: {alert.recipients?.join(", ")}</div>
                        </div>
                        <button onClick={() => deleteAlert(alert.id)} className="text-red-500 hover:text-red-700 text-sm font-medium">Delete</button>
                    </div>
                ))}
                {alerts.length === 0 && <div className="text-center text-sm text-slate-500 py-4">No active alerts.</div>}
            </div>
        </div>
    );
};

// --- ROLES COMPONENT ---
const RolesSettings = () => {
    const [roles, setRoles] = useState<any[]>([]);
    const [newRoleName, setNewRoleName] = useState("");

    useEffect(() => {
        api.get("/api/settings/roles").then(res => setRoles(res.data));
    }, []);

    const createRole = async () => {
        // Mock create
        const newRole = { name: newRoleName, permissions: ["read"] };
        setRoles([...roles, newRole]);
        setNewRoleName("");
    }

    return (
        <div className="space-y-6">
            <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex gap-4 mb-6">
                    <input className="flex-1 rounded border px-3 py-2 text-sm" placeholder="Role Name (e.g. Lead Auditor)" value={newRoleName} onChange={e => setNewRoleName(e.target.value)} />
                    <button onClick={createRole} className="rounded bg-brand-600 px-4 py-2 text-sm text-white font-medium">Create Role</button>
                </div>

                <div className="grid gap-4">
                    {roles.map((role, i) => (
                        <div key={i} className="flex justify-between items-center p-3 border rounded bg-slate-50">
                            <div>
                                <div className="font-medium text-slate-900">{role.name}</div>
                                <div className="text-xs text-slate-500">Permissions: {role.permissions.join(", ")}</div>
                            </div>
                            <button className="text-sm text-brand-600 hover:underline">Edit Permissions</button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

// --- GIT COMPONENT ---
const GitSettings = () => {
    const [status, setStatus] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [commitMsg, setCommitMsg] = useState("");
    const [remoteUrl, setRemoteUrl] = useState("");
    const [userName, setUserName] = useState("");
    const [userEmail, setUserEmail] = useState("");

    const loadStatus = async () => {
        try {
            const res = await api.get("/api/git/status");
            setStatus(res.data);
        } catch (e) {
            console.error(e);
        }
    };

    useEffect(() => {
        loadStatus();
    }, []);

    const initRepo = async () => {
        setLoading(true);
        try {
            await api.post("/api/git/init");
            loadStatus();
        } catch (e) {
            alert("Init failed");
        }
        setLoading(false);
    };

    const saveConfig = async () => {
        setLoading(true);
        try {
            await api.post("/api/git/config", { remote_url: remoteUrl, user_name: userName, user_email: userEmail });
            alert("Config saved");
        } catch (e) {
            alert("Config save failed");
        }
        setLoading(false);
    };

    const commit = async () => {
        if (!commitMsg) return alert("Message required");
        setLoading(true);
        try {
            const res = await api.post("/api/git/commit", { message: commitMsg });
            alert(res.data.message);
            setCommitMsg("");
            loadStatus();
        } catch (e) {
            alert("Commit failed");
        }
        setLoading(false);
    };

    const push = async () => {
        setLoading(true);
        try {
            const res = await api.post("/api/git/push");
            alert("Push successful");
        } catch (e: any) {
            const msg = e.response?.data?.detail || "Push failed";
            alert("Push failed: " + msg);
        }
        setLoading(false);
    };

    if (!status) return <div>Loading...</div>;

    return (
        <div className="space-y-6">
            <div className="rounded-lg bg-blue-50 p-4 border border-blue-100 text-blue-800 text-sm">
                <strong>Version Control:</strong> Sync your Prompts and Datasets to a Git repository.
            </div>

            {!status.initialized ? (
                <div className="rounded border p-6 bg-white text-center">
                    <p className="mb-4 text-slate-600">No git repository detected in the server root.</p>
                    <button onClick={initRepo} disabled={loading} className="rounded bg-brand-600 px-4 py-2 text-white text-sm font-medium">Initialize Git Repo</button>
                </div>
            ) : (
                <div className="space-y-6">
                    <div className="rounded border bg-white p-6">
                        <h3 className="text-lg font-medium mb-4">Repository Status</h3>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                            <div>Branch: <span className="font-mono">{status.branch || "HEAD"}</span></div>
                            <div>Changes pending: <span className={status.changed ? "text-orange-600 font-bold" : "text-green-600"}>{status.changed ? "Yes" : "No"}</span></div>
                        </div>
                        {status.status_text && <pre className="mt-4 p-2 bg-slate-100 rounded text-xs overflow-auto max-h-40">{status.status_text}</pre>}
                    </div>

                    <div className="rounded border bg-white p-6">
                        <h3 className="text-lg font-medium mb-4">Configuration</h3>
                        <div className="grid grid-cols-1 gap-4 mb-4">
                            <input className="border rounded px-3 py-2 text-sm" placeholder="Remote URLs (e.g. https://github.com/user/repo.git)" value={remoteUrl} onChange={e => setRemoteUrl(e.target.value)} />
                            <div className="grid grid-cols-2 gap-4">
                                <input className="border rounded px-3 py-2 text-sm" placeholder="Git Username" value={userName} onChange={e => setUserName(e.target.value)} />
                                <input className="border rounded px-3 py-2 text-sm" placeholder="Git Email" value={userEmail} onChange={e => setUserEmail(e.target.value)} />
                            </div>
                        </div>
                        <button onClick={saveConfig} disabled={loading} className="rounded border border-slate-300 px-4 py-2 text-sm font-medium hover:bg-slate-50">Update Config</button>
                    </div>

                    <div className="rounded border bg-white p-6">
                        <h3 className="text-lg font-medium mb-4">Sync</h3>
                        <div className="flex gap-4 items-end">
                            <input className="flex-1 border rounded px-3 py-2 text-sm" placeholder="Commit message (e.g. Updated prompts)" value={commitMsg} onChange={e => setCommitMsg(e.target.value)} />
                            <button onClick={commit} disabled={loading} className="rounded bg-slate-900 text-white px-4 py-2 text-sm font-medium">Backup & Commit</button>
                            <button onClick={push} disabled={loading} className="rounded bg-brand-600 text-white px-4 py-2 text-sm font-medium">Push to Remote</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

// --- MAIN PAGE ---
export const SettingsPage = () => {
    const { projectId, role } = useAuth();
    const isAdmin = role === "admin";
    const [activeTab, setActiveTab] = useState<Tab | "git">("general");

    const tabs = [
        { id: "general", label: "General" },
        { id: "roles", label: "Roles & Permissions" },
        { id: "email", label: "Email / SMTP" },
        { id: "alerts", label: "Alerts & Notifications" },
    ];

    if (isAdmin) {
        tabs.push({ id: "git", label: "Version Control" });
    }

    return (
        <Layout>
            <div className="mb-6">
                <h1 className="text-2xl font-semibold text-slate-900">Organization Settings</h1>
                <p className="text-sm text-slate-600">Manage global configuration, alerts, and roles.</p>
            </div>

            <div className="flex border-b border-slate-200 mb-6">
                {tabs.map(tab => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id as Tab | "git")}
                        className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${activeTab === tab.id ? "border-brand-600 text-brand-700" : "border-transparent text-slate-500 hover:text-slate-700"
                            }`}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            <div className="animate-fade-in">
                {activeTab === "general" && (
                    <div className="space-y-6">
                        <div className="rounded-lg border border-slate-200 bg-white p-6">
                            <h3 className="text-lg font-medium text-slate-900 mb-4">Database Configuration</h3>
                            <DatabaseInfo />
                        </div>
                    </div>
                )}
                {activeTab === "roles" && <RolesSettings />}
                {activeTab === "email" && projectId && <SmtpSettings projectId={projectId} />}
                {activeTab === "alerts" && projectId && <AlertsSettings projectId={projectId} />}
                {activeTab === "git" && isAdmin && <GitSettings />}
            </div>
        </Layout>
    );
};
