export type TaskKey = "scribe" | "clinical";

export interface ModelOption {
  id: string;
  label: string;
  description: string;
  icon: string;
}

export interface ModelPreferenceConfig {
  scribe: string;
  clinical: string;
}

export const PRESET_MODELS: readonly ModelOption[] = [
  {
    id: "qwen3-asr-flash",
    label: "Optimized Speed",
    description: "Real-time transcription for busy walk-ins.",
    icon: "⚡",
  },
  {
    id: "qwen3.5-omni-flash",
    label: "Maximum Accuracy",
    description: "Deep clinical reasoning. Best for complex cases.",
    icon: "🎯",
  },
] as const;

export const TASK_LABELS: Record<TaskKey, string> = {
  scribe: "Transcription Model",
  clinical: "Clinical Analysis Model",
} as const;

export const TASK_DESCRIPTIONS: Record<TaskKey, string> = {
  scribe: "Step 3 — audio → transcript",
  clinical: "Step 5 — transcript → medical report",
} as const;

export const DEFAULT_MODELS: Record<TaskKey, string> = {
  scribe: "qwen3-asr-flash",
  clinical: "qwen3.5-omni-flash",
} as const;
