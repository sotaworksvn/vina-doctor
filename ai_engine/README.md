ai_engine/
├── prompts/
│   ├── __init__.py            <-- (Quản lý các bộ xử lý thô (Audio và Text)
│   ├── scribe_prompts.py   <-- Chứa Master Medical Scribe Prompt (Dán vào module Audio)
│   └── clinical_prompts.py <-- Chứa Master Clinical Agent Prompt (Dán vào module Agents)
├── processors/
│   ├── audio.py            <-- Import scribe_prompts
│   └── text_cleaner.py
├── agents/
│   └── clinical_agent.py   <-- Import clinical_prompts
├── __init__.py                <-- (Quản lý các tác nhân thông minh).
└── orchestrator.py         <-- Điều phối toàn bộ
