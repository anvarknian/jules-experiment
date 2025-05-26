# Backend Service - Jules AI Chat Application

**Note:** The primary and recommended way to run this backend service along with the entire application (frontend, database) is by using Docker Compose. Please refer to the [main project README.md](../../README.md) for setup and execution instructions.

This document provides information specific to the backend service for development purposes.

## Overview

This FastAPI application serves as the backend for the Jules AI Chat Application. It handles:

*   Chat logic and communication with an external AI model provider (OpenRouter).
*   User management (basic).
*   Chat history storage.
*   Usage tracking and logging.
*   Database interactions via SQLAlchemy with a PostgreSQL database.
*   Database migrations using Alembic.

## API Documentation

When the backend service is running (typically via `docker-compose up`), the automatically generated API documentation (Swagger UI) can be accessed at:

*   `http://localhost:8000/docs`

The main chat endpoint is:

*   `POST /api/v1/chat`

## Technology Stack

*   **Python 3.9+**
*   **FastAPI**: For building the RESTful API.
*   **SQLAlchemy**: For ORM and database interaction.
*   **PostgreSQL**: As the database.
*   **Alembic**: For database schema migrations.
*   **Uvicorn**: As the ASGI server.
*   **python-dotenv**: For managing environment variables.

## Environment Variables

The backend service requires the following environment variables:

*   `OPENROUTER_API_KEY`: Your API key for OpenRouter. This is typically set in a `.env` file in the project root when using Docker Compose.
*   `DATABASE_URL`: The connection string for the PostgreSQL database. When running via Docker Compose, this is automatically configured in the `docker-compose.yml` file to connect to the `postgres` service.
*   `OPENROUTER_API_URL`: (Optional) Defaults to `https://openrouter.ai/api/v1/chat/completions`.
*   `DEFAULT_MODEL`: (Optional) Defaults to a pre-configured model like `gryphe/mythomax-l2-13b`.

## Database Migrations

Database schema migrations are managed using Alembic.

*   Migration scripts are located in the `backend/alembic/versions` directory.
*   When the backend service starts up within the Docker Compose environment, Alembic migrations are automatically applied to bring the database schema to the latest version (`alembic upgrade head`).

### Working with Migrations (Development)

If you make changes to the SQLAlchemy models in `backend/models.py`, you will need to generate a new migration script:

1.  **Ensure you have a local Python environment set up with all dependencies from `requirements.txt` installed.** (This is for migration generation, not for running the app if using Docker).
    ```bash
    # Example:
    # python -m venv venv
    # source venv/bin/activate
    # pip install -r backend/requirements.txt
    ```
2.  **Ensure your `DATABASE_URL` environment variable is set locally and points to a running PostgreSQL instance if you need to test the migration.** (Often, you can generate migrations without a live DB connection, but autogenerate might need it for reflection).
3.  **Navigate to the `backend` directory:**
    ```bash
    cd backend
    ```
4.  **Generate the migration script:**
    ```bash
    # Ensure your local .env file (if any) or environment has DATABASE_URL set
    # Or ensure alembic.ini refers to an env var that is set
    alembic revision -m "your_migration_message" --autogenerate
    ```
5.  **Inspect the generated script** in `backend/alembic/versions/` and make any necessary adjustments.
6.  The new migration will be applied automatically the next time the application starts via Docker Compose. To apply it manually (e.g., to a local dev database):
    ```bash
    alembic upgrade head
    ```

## Running Standalone (for Development - Not Recommended for Full App)

While Docker Compose is the recommended way, if you need to run the backend standalone for specific development or testing tasks:

1.  **Set up a Python virtual environment** and install dependencies from `requirements.txt`.
2.  **Ensure you have a PostgreSQL database running** and accessible.
3.  **Set the required environment variables:**
    *   Create a `.env` file in the `backend/` directory (or set them in your shell):
        ```dotenv
        OPENROUTER_API_KEY="YOUR_ACTUAL_OPENROUTER_API_KEY"
        DATABASE_URL="postgresql://jules_user:jules_password@localhost:5432/chat_db" 
        # Adjust DB URL as per your local PostgreSQL setup
        ```
4.  **Apply database migrations:**
    ```bash
    cd backend
    alembic upgrade head
    ```
5.  **Run the FastAPI application using Uvicorn:**
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

This setup is more complex than using Docker Compose and is generally only needed for focused backend development tasks. Always refer to the root `README.md` for the standard way to run the entire application.