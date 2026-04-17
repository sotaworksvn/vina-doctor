import type { ApiError } from "@/shared/types/api";

const DISABLE_AUTH = process.env.NEXT_PUBLIC_DISABLE_AUTH === "true";

function getBaseUrl(): string {
  if (typeof window !== "undefined") {
    return `${window.location.protocol}//${window.location.host}`;
  }
  return process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8001";
}

let _token: string | null = null;

export function setAuthToken(token: string | null) {
  _token = token;
}

export function getAuthToken(): string | null {
  return _token;
}

export class ApiRequestError extends Error {
  constructor(
    public status: number,
    public body: ApiError,
  ) {
    super(body.detail);
    this.name = "ApiRequestError";
  }
}

async function request<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(options.headers);

  if (_token && _token !== "auth-disabled") {
    headers.set("Authorization", `Bearer ${_token}`);
  }

  if (
    !headers.has("Content-Type") &&
    !(options.body instanceof FormData)
  ) {
    headers.set("Content-Type", "application/json");
  }

  const res = await fetch(`${getBaseUrl()}/api/v1${path}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    if (res.status === 401 && !DISABLE_AUTH && typeof window !== "undefined") {
      setAuthToken(null);
      window.location.href = "/login";
      throw new ApiRequestError(401, { detail: "Session expired" });
    }
    const body: ApiError = await res.json().catch(() => ({
      detail: res.statusText,
    }));
    throw new ApiRequestError(res.status, body);
  }

  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export const api = {
  get: <T>(path: string) => request<T>(path),

  post: <T>(path: string, body?: unknown) =>
    request<T>(path, {
      method: "POST",
      body: body instanceof FormData ? body : JSON.stringify(body),
    }),

  patch: <T>(path: string, body: unknown) =>
    request<T>(path, {
      method: "PATCH",
      body: JSON.stringify(body),
    }),

  put: <T>(path: string, body: unknown) =>
    request<T>(path, {
      method: "PUT",
      body: JSON.stringify(body),
    }),

  delete: <T>(path: string) =>
    request<T>(path, { method: "DELETE" }),
};
