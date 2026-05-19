# Project Manifest: Multi-Agent OSINT Workflow MVP

## 1. System Overview
- **Frontend:** Streamlit (`app.py`) with secure user authentication.
- **Backend API:** FastAPI (`main.py`) for orchestrating workflow requests.
- **Task Queue:** Celery workers backed by Redis for asynchronous execution.
- **Database:** PostgreSQL (using SQLAlchemy) for storing users and OSINT reports.
- **Deployment:** Docker Compose (`docker-compose.yml`) containerizing all 5 services.
- **AI & Data APIs:** Google Gemini SDK (`google-generativeai`) and Tavily Search API (`tavily-python`).

## 2. Current Project State
- **Frontend (`app.py`):** Includes SQLite (mocking Postgres) login, sign-up, session state, and a REST call to backend.
- **Backend (`main.py`):** Defines the REST endpoint (`/api/v1/run_osint`) but currently has a mock response instead of the full `run_agent_workflow` import.
- **Testing (`test_e2e.py`):** Script created to simulate POST requests to the backend.
- **Orchestration (`docker-compose.yml`):** Defined all services, environment variables, and ports.

## 3. Assessment & Update Checklist (For AI Assistant)
- [ ] **Code Integration:** Merge the multi-agent `run_agent_workflow` (Scout, Critic, Reporter nodes) into a separate `agents.py` file and import it properly into `main.py`.
- [ ] **Dependency Audit:** Generate a complete `requirements.txt` encompassing `fastapi`, `uvicorn`, `streamlit`, `celery`, `redis`, `sqlalchemy`, `passlib`, `bcrypt`, `google-generativeai`, `tavily-python`, and `psycopg2-binary`.
- [ ] **Environment Variables:** Extract hardcoded SQLite URIs and missing API keys into a secure `.env` file schema.
- [ ] **Docker Network Verification:** Ensure `app.py` hits the backend at `http://backend:8000` instead of `localhost:8000` when running inside Docker.
- [ ] **Security Review:** Verify password hashing implementations and check for exposed ports in production.

## 4. Project Status & Goals
**Note:** This is a work in progress. I am actively looking for suggestions and architectural reviews to make this project cheap to run but highly efficient.
