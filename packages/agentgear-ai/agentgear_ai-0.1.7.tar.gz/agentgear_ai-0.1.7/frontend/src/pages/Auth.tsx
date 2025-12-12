import { FormEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth, fetchAuthStatus, performLogin, performSetup } from "../lib/auth";

type Mode = "loading" | "setup" | "login";

export const AuthPage = () => {
  const { login, ready } = useAuth();
  const [mode, setMode] = useState<Mode>("loading");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [configuredByEnv, setConfiguredByEnv] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const load = async () => {
      try {
        const status = await fetchAuthStatus();
        setConfiguredByEnv(status.mode === "env");
        if (!status.configured) {
          setMode("setup");
        } else {
          setMode("login");
          if (status.username) {
            setUsername(status.username);
          }
        }
      } catch (err) {
        setMode("login");
      }
    };
    load();
  }, []);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const res =
        mode === "setup" ? await performSetup(username, password) : await performLogin(username, password);
      login(res.token, res.project_id, res.username);
      navigate("/projects");
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Unable to authenticate");
    }
  };

  const title = mode === "setup" ? "Create admin account" : "Sign in";
  const subtitle =
    mode === "setup"
      ? "Set a username and password for your AgentGear dashboard."
      : configuredByEnv
        ? "Credentials are controlled by the environment (.env)."
        : "Enter your admin credentials.";

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-100 px-4">
      <div className="w-full max-w-md rounded-xl border border-slate-200 bg-white p-8 shadow-md">
        <div className="mb-6 text-center">
          <div className="text-2xl font-semibold text-slate-900">AgentGear Dashboard</div>
          <div className="mt-2 text-sm text-slate-600">{subtitle}</div>
        </div>
        {!ready && mode === "loading" ? (
          <div className="text-center text-sm text-slate-600">Loading...</div>
        ) : (
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label className="text-sm font-medium text-slate-700">Username</label>
              <input
                className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div>
              <label className="text-sm font-medium text-slate-700">Password</label>
              <input
                type="password"
                className="mt-1 w-full rounded border border-slate-200 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            {error ? <div className="text-sm text-red-600">{error}</div> : null}
            <button
              type="submit"
              className="w-full rounded bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
            >
              {mode === "setup" ? "Create account" : "Sign in"}
            </button>
            {mode === "setup" ? (
              <p className="text-xs text-slate-500">
                You can later override credentials via environment variables AGENTGEAR_ADMIN_USERNAME and
                AGENTGEAR_ADMIN_PASSWORD if you need to reset access.
              </p>
            ) : null}
          </form>
        )}
      </div>
    </div>
  );
};
