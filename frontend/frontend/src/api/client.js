const API_BASE = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(
  /\/$/,
  ""
);
const API_KEY = import.meta.env.VITE_API_KEY || "";

/**
 * Monta URL absoluta para o backend (ex.: `/api/listas/previsao/`).
 */
export function apiUrl(path) {
  const p = path.startsWith("/") ? path : `/${path}`;
  return `${API_BASE}${p}`;
}

/**
 * fetch com headers padrão (JSON + API key opcional).
 */
export function apiFetch(path, options = {}) {
  const headers = new Headers(options.headers || {});

  if (
    options.body != null &&
    typeof options.body === "string" &&
    !headers.has("Content-Type")
  ) {
    headers.set("Content-Type", "application/json");
  }

  if (API_KEY) {
    headers.set("X-API-KEY", API_KEY);
  }

  return fetch(apiUrl(path), { ...options, headers });
}

/**
 * Lê corpo de erro (DRF costuma usar `detail`, throttling, etc.).
 */
export async function readApiError(response) {
  const text = await response.text();
  try {
    const data = JSON.parse(text);
    if (typeof data === "string") return data;
    if (data?.detail) {
      if (typeof data.detail === "string") return data.detail;
      if (Array.isArray(data.detail)) {
        return data.detail
          .map((d) => (typeof d === "string" ? d : d?.message || JSON.stringify(d)))
          .join("; ");
      }
    }
    if (data?.erro) return String(data.erro);
    if (data?.message) return String(data.message);
    if (data?.non_field_errors) return String(data.non_field_errors);
    return text?.slice(0, 400) || `HTTP ${response.status}`;
  } catch {
    return text?.slice(0, 400) || `HTTP ${response.status}`;
  }
}
