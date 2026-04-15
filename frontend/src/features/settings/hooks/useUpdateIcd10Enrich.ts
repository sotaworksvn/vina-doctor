import { useMutation, useQueryClient } from "@tanstack/react-query";
import { updateIcd10Enrich } from "@/features/settings/api/settings-api";
import type { UpdateIcd10EnrichRequest } from "@/features/settings/types";

export function useUpdateIcd10Enrich() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: UpdateIcd10EnrichRequest) =>
      updateIcd10Enrich(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin-config"] });
    },
  });
}
