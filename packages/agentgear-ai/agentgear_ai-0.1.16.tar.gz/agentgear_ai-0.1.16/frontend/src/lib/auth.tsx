import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { api, setApiKey, tokenStorageKey } from "./api";

type AuthState = {
  token?: string;
  projectId?: string;
  username?: string;
  role?: string;
};

type AuthContextValue = AuthState & {
  ready: boolean;
  login: (token: string, projectId: string, username?: string, role?: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue>({
  ready: false,
  login: () => undefined,
  logout: () => undefined
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [auth, setAuth] = useState<AuthState>(() => {
    const token = typeof localStorage !== "undefined" ? localStorage.getItem(tokenStorageKey) : undefined;
    const projectId = typeof localStorage !== "undefined" ? localStorage.getItem("agentgear_project") : undefined;
    const username = typeof localStorage !== "undefined" ? localStorage.getItem("agentgear_username") : undefined;
    const role = typeof localStorage !== "undefined" ? localStorage.getItem("agentgear_role") : undefined;
    return { token: token || undefined, projectId: projectId || undefined, username: username || undefined, role: role || undefined };
  });
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (auth.token) {
      setApiKey(auth.token);
    } else {
      setApiKey(undefined);
    }
    setReady(true);
  }, [auth.token]);

  const value = useMemo<AuthContextValue>(
    () => ({
      ...auth,
      ready,
      login: (token: string, projectId: string, username?: string, role?: string) => {
        setApiKey(token);
        localStorage.setItem("agentgear_project", projectId);
        if (username) {
          localStorage.setItem("agentgear_username", username);
        }
        if (role) {
          localStorage.setItem("agentgear_role", role);
        }
        setAuth({ token, projectId, username, role });
      },
      logout: () => {
        setApiKey(undefined);
        localStorage.removeItem("agentgear_project");
        localStorage.removeItem("agentgear_username");
        localStorage.removeItem("agentgear_role");
        setAuth({ token: undefined, projectId: undefined, username: undefined, role: undefined });
        window.location.href = "/auth";
      }
    }),
    [auth, ready]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);

export const fetchAuthStatus = async () => {
  const res = await api.get("/api/auth/status");
  return res.data as {
    configured: boolean;
    mode: "none" | "env" | "db";
    username?: string | null;
  };
};

export const performLogin = async (username: string, password: string) => {
  const res = await api.post("/api/auth/login", { username, password });
  return res.data as { token: string; project_id: string; username: string; role: string };
};

export const performSetup = async (username: string, password: string) => {
  const res = await api.post("/api/auth/setup", { username, password });
  return res.data as { token: string; project_id: string; username: string; role: string };
};
