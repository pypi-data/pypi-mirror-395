import axios from "axios";

const baseURL = import.meta.env.VITE_AGENTGEAR_API ?? "http://localhost:8000";

export const api = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json"
  }
});

export const setApiKey = (token?: string) => {
  if (token) {
    api.defaults.headers.common["X-AgentGear-Key"] = token;
  } else {
    delete api.defaults.headers.common["X-AgentGear-Key"];
  }
};
