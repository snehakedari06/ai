# Aevor AI TODO

## Completed

- [x] Repository inspection (Empty workspace analyzed and git initialized)
- [x] Architecture definition (Defined in README.md, AGENTS.md, & ROADMAP.md)
- [x] Base configuration and dependencies (.gitignore, .env.example, requirements.txt, Dockerfile)
- [x] Service foundation (app package, config settings loader, main.py entry with lifespan manager)
- [x] API foundation (/health and /ready endpoints)
- [x] Model Abstraction Layer (Abstract BaseModel interface and DummyModel)
- [x] Basic Inference API (Versioned POST /api/v1/inference with validation and unavailable fallback logic)
- [x] Testing framework setup and test execution (conftest.py client, pytest validation/unavailable test suites)

- [x] Repository Scanner & File Classification heuristics (IngestionService scanning, filtering, and role classification)
- [x] Code Chunking logic (Sliding window and structural code chunker)
- [x] Embeddings layer & Vector Store integration (Deterministic cosine similarity vector store with persistence)
- [x] Repository Ingestion and Grounded Q&A Endpoints (`/api/v1/repository/ingest` and `/api/v1/repository/query`)

## Currently Working On

- [ ] Phase 2 — Codebase Intelligence & Structural Symbol Extraction

## Blocked

- None

## Next

- [ ] AST parsing & symbol extraction (Functions, classes, imports, dependencies)
- [ ] Cross-file reference and call-graph mapping
- [ ] Integration with external LLM / embedding providers (e.g., OpenAI, Ollama, HuggingFace)
- [ ] PR ingestion & diff intelligence (Phase 4)

## Notes

- Environment configurations are loaded dynamically using Pydantic Settings.
- Lifespan context handlers and SettingsConfigDict are implemented to resolve all legacy deprecation warnings.
