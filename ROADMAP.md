# Aevor AI — Codebase Intelligence & Open-Source Contribution Assistant Feature Roadmap

> Repository: `Aevor/ai`
> Parent Project: `Aevor`
> Service Type: AI / ML Microservice
> Primary Owner: Sneha
> Overall Project Owner: Sanjeev
> Status: Proposed / Under Development

---

## 1. Purpose

Aevor AI is a dedicated AI microservice within the Aevor ecosystem. It is a codebase-aware engineering intelligence system that understands an entire software repository and helps developers throughout the software-development lifecycle.

Aevor AI should understand:
- Repository structure
- Source code, functions, classes, packages, services, and APIs
- Database models and schemas
- Configuration and dependencies
- Tests and documentation
- Git history, issues, and pull requests
- Project architecture and existing conventions

The core principle is:
> Aevor AI should understand the repository before attempting to generate, modify, or review code.

---

## 2. Aevor Architecture Context

Aevor is being developed as a microservice-based platform:
- `platform`: Core Aevor platform / API / application services
- `ai`: Aevor AI microservice
- `infra`: Infrastructure / deployment / operational components
- `docs`: Product requirements / architecture / technical documentation

The AI implementation should remain modular so that model providers, embedding providers, vector stores, repository analysis components, and AI workflows can evolve independently.

---

## 3. Core Product Vision

```
    Repository
        ↓
    Repository Ingestion
        ↓
    Codebase Understanding
        ↓
    Semantic / Structural Indexing
        ↓
    Context Retrieval
        ↓
    AI Reasoning
        ↓
    Developer Assistance
        ↓
    Implementation
        ↓
    Testing
        ↓
    Pull Request
        ↓
    PR Analysis
        ↓
    Human Review
        ↓
    Maintainer Feedback
        ↓
    Fixes
        ↓
    Re-analysis
        ↓
    Merge
```

---

## 4. Human Control

Aevor AI assists developers and does not replace repository maintainers. The AI must NOT automatically merge pull requests, approve its own pull requests, bypass branch protection, or perform force pushes or deployments without explicit authorization.

---

## 5. Repository Ingestion

Aevor AI should ingest and classify repository files to understand their roles (e.g., source code, tests, documentation, configuration, Docker, migrations, etc.) and discover project architecture dynamically.

---

## 6. Codebase Indexing

Split repositories into meaningful structural scopes (Repository -> Service -> Package -> File -> Class -> Function/Method/Symbol) for context-aware retrieval.

---

## 7. Semantic Repository Search

Combine keyword search, semantic similarity search, and symbol/structure indexing to locate relevant code components and explain relationships.

---

## 8. Repository Question Answering

Support grounded codebase Q&A (e.g., "Explain how authentication works", "Where is MongoDB initialized?") by passing query-relevant files and symbols in context.

---

## 9. Codebase Architecture Understanding

Derive and explain request flows, service boundaries, data flows, and database relationships from the source files.

---

## 10. Codebase-Aware Debugging

Investigate errors (e.g., "Login returning 401 after OAuth callback") by tracing components, state transitions, configuration, and logs, returning evidence-based causes and fixes.

---

## 11. Implementation Planning & Code Generation

Propose structured plans and generate code extending existing patterns, directories, naming conventions, error handling, and test conventions.

---

## 12. Patch & Diff Generation

Propose git diffs rather than directly committing edits, keeping developers in control of accepting, modifying, or rejecting changes.

---

## 13. Pull Request Intelligence

Analyze descriptions, diffs, issues, and histories to generate:
- **PR Summaries**: Concise purpose and list of backend/frontend/test changes.
- **Architectural Impact**: Service flows and downstream side-effects.
- **Correctness/Security Analyses**: Incorrect state flows, token handling, SQL/Command injections, or exposed credentials.
- **Test Coverage Analysis**: Detecting modified logic lacking tests.

Review findings use a structured format:
```
Finding: [Name]
Severity: [Low/Medium/High]
Confidence: [Low/Medium/High]
Location: [File:Line]
Problem: [Description]
Why it matters: [Impact]
Suggested solution: [Code/Action]
Suggested test: [Verification]
```

---

## 14. Open-Source Contribution Assistant

A flagship onboarding experience for beginners:
- **New Contributor Mode**: Tech stack, setup explanation, and contribution onboarding.
- **Good First Issue Matching**: Analyzing open issues and difficulty ranking (Beginner, Intermediate, Advanced).
- **PR Writing Assistant**: Drafting titles/descriptions linking issues.
- **Maintainer Comment Explanations**: Clarifying code review feedback and automating fix updates.

---

## 15. Development Phases

### Phase 1 — AI Foundation (In Progress/Refinement)
- Repository ingestion
- File processing
- Code chunking
- Embeddings
- Semantic indexing
- Retrieval
- Basic repository Q&A

### Phase 2 — Codebase Intelligence
- Symbol extraction
- Code relationships
- Architecture understanding
- Dependency understanding
- Issue-to-code mapping
- Git history understanding

### Phase 3 — Engineering Assistant
- Debugging & Root-cause analysis
- Implementation planning
- Code/test/patch generation

### Phase 4 — Pull Request Intelligence
- PR ingestion & diff analysis
- Correctness, security, and test reviews

### Phase 5 — Open-Source Contribution Assistant
- Good-first-issue matching
- Contribution guides & PR drafting
- Maintainer feedback explanation

### Phase 6 — Advanced Engineering Intelligence
- Repository health analysis
- Workspace recommendations
- Learning assistance
