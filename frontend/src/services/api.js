import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

function getCsrfToken() {
  const match = document.cookie.match(/(?:^|; )csrf_token=([^;]*)/);
  return match ? decodeURIComponent(match[1]) : null;
}

api.interceptors.request.use((config) => {
  const token = getCsrfToken();

  if (
    token &&
    ["post", "put", "patch", "delete"].includes(
      config.method?.toLowerCase()
    )
  ) {
    config.headers["X-CSRF-Token"] = token;
  }

  return config;
});

export default api;