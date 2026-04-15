import { useMutation } from "@tanstack/react-query";
import { updateDashscopeApiKey } from "@/features/settings/api/settings-api";
import type { UpdateApiKeyRequest } from "@/features/settings/types";

export function useUpdateApiKey() {
  return useMutation({
    mutationFn: (payload: UpdateApiKeyRequest) =>
      updateDashscopeApiKey(payload),
  });
}
