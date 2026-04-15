import { api } from "@/shared/lib/api-client";
import type { UpdateApiKeyRequest } from "@/features/settings/types";

/**
 * POST /api/v1/admin/config/dashscope-api-key
 * Proxies the new key to ai_engine; returns void on success (204).
 */
export async function updateDashscopeApiKey(
  payload: UpdateApiKeyRequest,
): Promise<void> {
  return api.post<void>("/admin/config/dashscope-api-key", payload);
}
