import axios from "axios";

const baseURL = import.meta.env.VITE_AGENTGEAR_API ?? "http://localhost:8000";
const TOKEN_KEY = "agentgear_token";

export const api = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json"
  }
});

export const setApiKey = (token?: string) => {
  if (token) {
    api.defaults.headers.common["X-AgentGear-Key"] = token;
    localStorage.setItem(TOKEN_KEY, token);
  } else {
    delete api.defaults.headers.common["X-AgentGear-Key"];
    localStorage.removeItem(TOKEN_KEY);
  }
};

const existing = typeof localStorage !== "undefined" ? localStorage.getItem(TOKEN_KEY) : null;
if (existing) {
  setApiKey(existing);
}

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401) {
      setApiKey(undefined);
      window.location.href = "/auth";
    }
    return Promise.reject(error);
  }
);

export const tokenStorageKey = TOKEN_KEY;
