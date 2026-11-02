# Aevor AI Microservice

Dedicated AI microservice for the Aevor platform. This is an independent microservice responsible for AI/ML capabilities, model inference, and AI-related utilities.

## Architecture

The service is built on Python and FastAPI, designed with a clean boundary. The platform layer communicates with this service via HTTP REST APIs.

```
       Aevor Platform
              |
              | HTTP REST API
              v
          Aevor AI (FastAPI)
              |
              v
       AI Service Layer
              |
              v
       Inference Layer
              |
              v
            Model
```

## Quick Start

### Prerequisites

- Python 3.8+ (Tested on Python 3.8.10)
- Pip (Python Package Installer)
- Docker (optional, for containerized execution)

### Local Setup

1. **Clone & Navigate** to the repository:
   ```bash
   cd c:\aveora
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv .venv
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   # Windows (CMD)
   .\.venv\Scripts\activate.bat
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Configuration**:
   ```bash
   copy .env.example .env
   ```
   Modify `.env` to suit your local setup.

### Running the Application

Start the FastAPI application locally using Uvicorn:
```bash
uvicorn app.main:app --reload --port 8000
```
The server will start at `http://localhost:8000`.

### Running Tests

Execute unit and integration tests using `pytest`:
```bash
pytest
```

---

## API Endpoints

- **Health Check**: `GET /health`
  - Returns service status (`{"status": "ok"}`). Used to monitor process lifecycle.
- **Readiness Check**: `GET /ready`
  - Returns whether models are loaded and requests can be processed (`{"status": "ready"}` or `{"status": "not_ready"}`).

All versioned inference endpoints will be prefix-routed with `/api/v1/`.

---

## Docker Usage

### Build the Image
```bash
docker build -t aevor-ai:latest .
```

### Run the Container
```bash
docker run -p 8000:8000 --env-file .env aevor-ai:latest
```
