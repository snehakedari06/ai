# AGENTS.md — Agent & Contributor Workflow Guidelines

This document outlines the guidelines, architecture, and coding rules for human developers and AI coding agents working on the Aevor AI microservice.

---

## 1. Repository Purpose & Architecture

`Aevor/ai` is the dedicated, independent AI microservice for the Aevor ecosystem. It must remain decoupled from `Aevor/platform`.

### Core Architectural Rules
- **Decoupling**: Do not place AI implementation code inside `Aevor/platform`.
- **HTTP boundaries**: The platform interacts with the AI service exclusively via defined HTTP API contracts.
- **Layered Design**:
  - **API Layer (`app/api/`)**: Request validation, routing, response formatting, and error handling.
  - **Service Layer (`app/services/`)**: Orchestrates data flow and calls preprocessing/inference.
  - **Inference/Preprocessing Layer (`app/inference/` / `app/preprocessing/`)**: Deep ML code execution, tokenization, scaling, model inference.
- **Preloaded Models**: Load models during service startup, not on every request.

---

## 2. Directory Structure

Ensure code resides in its correct layer:
```
c:\aveora\
├── app/
│   ├── api/          # Route definitions, validation schemas, and middlewares
│   ├── services/     # High level orchestrating service logic
│   ├── models/       # ML models serialization/storing scripts
│   ├── inference/    # Model loading and forward-pass inference logic
│   ├── preprocessing/# Preprocessing & tokenization logic
│   ├── config/       # Pydantic configuration settings
│   └── main.py       # Application initialization
├── tests/            # Test suites (unit and integration tests)
├── Dockerfile        # Container recipe
├── README.md         # Developer instructions
├── AGENTS.md         # Contributor guidelines
├── TODO.md           # Project tasks source of truth
└── .env.example      # Environment variables template
```

---

## 3. Development and Verification Commands

### Dependencies Setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Local Dev Run
```powershell
uvicorn app.main:app --reload --port 8000
```

### Run Tests
```powershell
pytest
```

---

## 4. Security Rules

- **No Secrets**: Never commit credentials, tokens, API keys, passwords, or private files to Git. Add them to `.env` (which must remain in `.gitignore`).
- **No Untrusted Models**: Do not load model weights from untrusted serialized file formats (e.g. arbitrary pickles). Use safe formats like `.safetensors` or ONNX.

---

## 5. Contributor and Agent Workflow

Every agent/developer MUST follow this lifecycle:

1. **Read `AGENTS.md` and `TODO.md`** first to check current tasks.
2. **Inspect the existing implementation** in the repository.
3. **Identify the next unfinished task** in the `TODO.md`. Do not start on future phases or implement unlisted features.
4. **Implement only that task**. Follow clean, well-tested, self-documenting code.
5. **Run tests** and verify that everything compiles and all tests pass.
6. **Update `TODO.md`** by marking completed items and modifying lists if needed.
7. **Update `AGENTS.md`** if any architecture or development guidelines changed.
8. **Report the work** detailing files changed, tests run, results, blockers, and architectural concerns.
