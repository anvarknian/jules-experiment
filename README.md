# Jules AI Chat Application

Jules is a full-stack chat application powered by a FastAPI backend using PostgreSQL for data storage and a Flutter web frontend. The entire application is containerized using Docker and managed with Docker Compose for easy setup and deployment.

## Project Overview

The application consists of three main services:

*   **`frontend`**: A Flutter web application that provides the user interface for chatting.
*   **`backend`**: A FastAPI Python application that handles chat logic, interacts with an external AI model provider (OpenRouter), and manages user data, chat history, and logs in a PostgreSQL database.
*   **`postgres`**: A PostgreSQL database service for storing all application data.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Docker**: [Installation Guide](https://docs.docker.com/get-docker/)
*   **Docker Compose**: [Installation Guide](https://docs.docker.com/compose/install/) (Often included with Docker Desktop)

## Getting Started

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Configure Environment Variables:**
    *   This project requires an API key for OpenRouter to connect to AI models.
    *   Copy the root-level `.env.example` file to a new file named `.env`:
        ```bash
        cp .env.example .env
        ```
    *   Open the `.env` file and replace `"YOUR_ACTUAL_OPENROUTER_API_KEY_HERE"` with your actual OpenRouter API key.
        ```dotenv
        OPENROUTER_API_KEY="your_real_openrouter_api_key"
        ```
    *   The `DATABASE_URL` for the backend is automatically configured in `docker-compose.yml` when running within Docker.

3.  **Build and Run the Application:**
    *   Use Docker Compose to build the images and start all services:
        ```bash
        docker-compose up --build
        ```
    *   The `--build` flag ensures images are rebuilt if there are changes (e.g., in Dockerfiles or application code). For subsequent runs, `docker-compose up` is usually sufficient.

4.  **Accessing the Application:**
    *   **Frontend (Flutter Web App):** Open your web browser and navigate to `http://localhost:8080`
    *   **Backend API (FastAPI Docs):** The backend API documentation (Swagger UI) is available at `http://localhost:8000/docs`. The main chat endpoint is `http://localhost:8000/api/v1/chat`.

## Services

*   **`postgres` (Database):**
    *   Uses the official `postgres:13-alpine` image.
    *   Database credentials and name (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`) are defined in `docker-compose.yml`.
    *   Data is persisted in a Docker named volume called `postgres_data`. This means your chat history and user data will remain even if you stop and restart the containers. To remove the data, you would need to remove the volume (e.g., `docker volume rm <project_name>_postgres_data`).

*   **`backend` (FastAPI Application):**
    *   Builds from the `./backend/Dockerfile`.
    *   Connects to the `postgres` service. The `DATABASE_URL` is set in `docker-compose.yml` to point to the Docker internal network name of the PostgreSQL service.
    *   Requires `OPENROUTER_API_KEY` from the `.env` file to function.
    *   Uses Alembic for database migrations, which are applied automatically on startup.
    *   Code from the local `./backend` directory is mounted into the container, allowing for hot-reloading on code changes during development (Uvicorn needs to be running in reload mode for this, which is typical for development).

*   **`frontend` (Flutter Web Application):**
    *   Builds from the `./flutter_chat_app/Dockerfile`.
    *   The `BACKEND_URL` is passed as a build argument (`--dart-define`) during the Docker build process, configured in `docker-compose.yml` to be `http://backend:8000`. This allows the Flutter app to communicate with the backend service over the Docker network.
    *   Served by an Nginx web server.

## Development

*   For details on backend-specific development, see `backend/README.md`.
*   For details on frontend-specific development, see `flutter_chat_app/README.md`.

## Stopping the Application

*   To stop all running services, press `Ctrl+C` in the terminal where `docker-compose up` is running.
*   To stop and remove the containers (but not the `postgres_data` volume):
    ```bash
    docker-compose down
    ```

## Troubleshooting

*   **View Logs:** To see logs from a specific service:
    ```bash
    docker-compose logs <service_name>
    ```
    For example, to see backend logs:
    ```bash
    docker-compose logs backend
    ```
    To follow logs in real-time:
    ```bash
    docker-compose logs -f <service_name>
    ```

*   **Port Conflicts:** If you have other services running on ports `8080` (frontend) or `8000` (backend), you may need to stop them or change the port mappings in `docker-compose.yml`.

*   **OpenRouter API Key:** Ensure your `OPENROUTER_API_KEY` in the `.env` file is correct and has sufficient credits/access.

*   **Database Issues:** If the backend fails to connect to the database, check the logs for both the `backend` and `postgres` services. Ensure the `postgres_data` volume is healthy. If you need to start fresh with the database (losing all data), you can stop the services, remove the volume (`docker volume rm <your_project_directory_name>_postgres_data`), and then run `docker-compose up --build` again.

*   **Flutter Build Issues:** If the frontend fails to build, check the logs from the build process (`docker-compose build frontend`). Ensure Flutter and Dart versions are compatible if you've made changes to the Flutter app.

This README provides a comprehensive guide to setting up and running the application using Docker Compose.
