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
        : "Sign in to access your agent observability dashboard.";

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#eef2ff] to-[#f0f9ff] animate-gradient-slow flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="mb-6 text-center text-xs text-slate-500 tracking-wide">AgentGear v0.1 — Observability for AI Agents</div>
        <div className="w-full rounded-2xl border border-white/20 bg-white/70 backdrop-blur-md shadow-xl p-8 md:p-10">
          <div className="mb-6 text-center">
            <div className="text-2xl font-semibold text-slate-900 tracking-tight">Welcome to AgentGear</div>
            <div className="mt-2 text-sm text-slate-600">{subtitle}</div>
          </div>
          {!ready && mode === "loading" ? (
            <div className="text-center text-sm text-slate-600">Loading...</div>
          ) : (
            <form className="space-y-4" onSubmit={handleSubmit}>
              <div>
                <label className="text-sm font-medium text-slate-700">Admin Username</label>
                <div className="relative mt-1">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M16 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                      <circle cx="12" cy="7" r="4" />
                    </svg>
                  </span>
                  <input
                    className="w-full rounded-xl border border-white/40 bg-white/80 px-10 py-3 text-sm shadow-inner focus:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-100"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700">Password</label>
                <div className="relative mt-1">
                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                      <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                    </svg>
                  </span>
                  <input
                    type="password"
                    className="w-full rounded-xl border border-white/40 bg-white/80 px-10 py-3 text-sm shadow-inner focus:border-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-100"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
              </div>
              {error ? <div className="text-sm text-red-600">{error}</div> : null}
              <button
                type="submit"
                className="w-full rounded-xl bg-gradient-to-r from-blue-600 to-blue-500 px-4 py-3 text-sm font-semibold text-white shadow-md transition-all hover:from-blue-500 hover:to-blue-400 hover:shadow-lg"
              >
                {mode === "setup" ? "Create Account" : "Log In"}
              </button>
              <div className="text-center text-xs text-slate-500">
                <a className="hover:text-slate-700" href="#">
                  Forgot password?
                </a>
              </div>
              {mode === "setup" ? (
                <p className="text-xs text-slate-500 text-center">
                  You can later override credentials via environment variables AGENTGEAR_ADMIN_USERNAME and
                  AGENTGEAR_ADMIN_PASSWORD if you need to reset access.
                </p>
              ) : null}
            </form>
          )}
        </div>
        <div className="mt-6 text-center text-[11px] text-slate-500">
          © 2025 AgentGear — AI Observability &amp; Tracing Platform
        </div>
      </div>
    </div>
  );
};
