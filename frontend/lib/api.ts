import { auth } from "@clerk/nextjs/server";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const { getToken } = await auth();
  const token = await getToken();
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {"Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}), ...(init?.headers ?? {})},
    cache: "no-store",
  });
  if (!response.ok) throw new Error(await response.text());
  return response.json() as Promise<T>;
}
