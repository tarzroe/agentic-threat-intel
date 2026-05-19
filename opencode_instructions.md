# Opencode Setup Instructions

Welcome to the Multi-Agent OSINT Workflow MVP! This guide will help you set up the environment and launch the application.

## Prerequisites
Before you begin, ensure you have the following API keys:
1. **Google Gemini API Key:** Get it from Google AI Studio.
2. **Tavily API Key:** Get it from Tavily.

## Environment Setup
Create a `.env` file in the root directory and add your API keys:
```
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Launching the Application
We use Docker Compose to run the PostgreSQL database, Redis message broker, FastAPI backend, Celery worker, and Streamlit frontend.

1. Make sure you have Docker and Docker Compose installed.
2. Run the following command in the root directory where your `docker-compose.yml` is located:
```bash
docker-compose up --build -d
```
3. Access the Streamlit frontend at `http://localhost:8501`.
4. The FastAPI backend is accessible at `http://localhost:8000`.
5. To stop the application, run:
```bash
docker-compose down
```
