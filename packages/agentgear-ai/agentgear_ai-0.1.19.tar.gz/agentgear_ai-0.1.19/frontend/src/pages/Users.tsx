import { useEffect, useState } from "react";
import { Layout } from "../components/Layout";
import { api } from "../lib/api";
import { DataTable } from "../components/DataTable";

type User = {
    id: string;
    username: string;
    email?: string;
    role: string;
    created_at: string;
};

export const UsersPage = () => {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("user");

    const [showForm, setShowForm] = useState(false);

    const load = async () => {
        try {
            const res = await api.get<User[]>("/api/users");
            setUsers(res.data);
        } catch (error) {
            console.error("Failed to load users", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        load();
    }, []);

    const createUser = async () => {
        if (!username || !password) return;
        try {
            await api.post("/api/users", { username, password, role });
            setUsername("");
            setPassword("");
            setShowForm(false);
            load();
        } catch (e) {
            alert("Failed to create user");
        }
    };

    return (
        <Layout>
            <div className="mb-6 flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-semibold text-slate-900">User Management</h1>
                    <p className="text-sm text-slate-600">Manage users and their access.</p>
                </div>
                <button
                    onClick={() => setShowForm(!showForm)}
                    className="rounded bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700 shadow-sm"
                >
                    {showForm ? "Cancel" : "+ New User"}
                </button>
            </div>

            {/* Tip */}
            <div className="mb-6 rounded-lg border border-amber-100 bg-amber-50 p-4">
                <div className="flex items-start gap-3">
                    <span className="text-amber-500">💡</span>
                    <div className="text-sm text-amber-800">
                        <strong>Admin Tip:</strong> Users created here can log in to the dashboard. You can assign them roles to restrict their access.
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 gap-6">
                {showForm && (
                    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm max-w-lg mb-6 animate-slide-up">
                        <h2 className="text-lg font-semibold text-slate-900 mb-4">Add User</h2>
                        <div className="space-y-4">
                            <div>
                                <label className="text-sm font-medium text-slate-700">Username</label>
                                <input
                                    className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                />
                            </div>
                            <div>
                                <label className="text-sm font-medium text-slate-700">Password</label>
                                <input
                                    type="password"
                                    className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                />
                            </div>
                            <div>
                                <label className="text-sm font-medium text-slate-700">Role</label>
                                <select
                                    className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                                    value={role}
                                    onChange={(e) => setRole(e.target.value)}
                                >
                                    <option value="user">User</option>
                                    <option value="admin">Admin</option>
                                </select>
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
                                    onClick={createUser}
                                >
                                    Create User
                                </button>
                            </div>
                        </div>
                    </div>
                )}

                <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
                    <div className="p-4 border-b border-slate-100 bg-slate-50/50">
                        <h3 className="font-medium text-slate-900">All Users</h3>
                    </div>
                    {loading ? (
                        <div className="p-4 text-sm text-slate-500">Loading...</div>
                    ) : (
                        <DataTable
                            data={users}
                            columns={[
                                { key: "username", header: "Username" },
                                { key: "role", header: "Role", render: (r) => <span className="uppercase text-xs font-bold text-slate-500">{r.role}</span> },
                                { key: "created_at", header: "Created" },
                                {
                                    key: "actions", header: "Actions", render: (u) => (
                                        <div className="flex gap-2">
                                            <button
                                                className="text-xs font-medium text-blue-600 hover:text-blue-800"
                                                onClick={() => {
                                                    const newPass = prompt(`Enter new password for ${u.username}:`);
                                                    if (newPass) {
                                                        api.put(`/api/users/${u.id}/password`, { password: newPass })
                                                            .then(() => alert("Password updated"))
                                                            .catch(() => alert("Failed to update password"));
                                                    }
                                                }}
                                            >
                                                Reset Password
                                            </button>
                                            <button
                                                className="text-xs font-medium text-red-600 hover:text-red-800"
                                                onClick={() => {
                                                    if (confirm(`Are you sure you want to delete ${u.username}?`)) {
                                                        api.delete(`/api/users/${u.id}`)
                                                            .then(() => load())
                                                            .catch(() => alert("Failed to delete user"));
                                                    }
                                                }}
                                            >
                                                Delete
                                            </button>
                                        </div>
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
