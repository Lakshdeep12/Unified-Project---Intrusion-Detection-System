export const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export function getToken() {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("sentinel_token");
}

export function getUsername() {
  if (typeof window === "undefined") return "Operator";
  return localStorage.getItem("sentinel_username") || "Operator";
}

export function saveSession(token: string, username: string) {
  localStorage.setItem("sentinel_token", token);
  localStorage.setItem("sentinel_username", username);
}

export function clearSession() {
  localStorage.removeItem("sentinel_token");
  localStorage.removeItem("sentinel_username");
}
