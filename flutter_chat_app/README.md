# Flutter Frontend - Jules AI Chat Application

**Note:** The primary and recommended way to run this Flutter web application along with the entire application (backend, database) is by using Docker Compose. Please refer to the [main project README.md](../../README.md) for setup and execution instructions.

This document provides information specific to the Flutter frontend for development purposes.

## Overview

This Flutter application provides the web-based user interface for the Jules AI Chat Application. It communicates with the FastAPI backend to send messages and receive AI-generated replies.

## Accessing the Application

When the application is running via `docker-compose up`, the Flutter web app is typically accessible at:

*   `http://localhost:8080`

## Backend URL Configuration

*   When built and run via Docker Compose (as defined in `docker-compose.yml` and `flutter_chat_app/Dockerfile`), the `BACKEND_URL` is automatically passed to the Flutter build process using the `--dart-define` flag. It is set to `http://backend:8000`, which is the Docker network address for the backend service.
*   For local development outside of Docker (see below), the application defaults to `http://localhost:8000`. This can be seen in `lib/src/services/api_service.dart`.

## Technology Stack

*   **Flutter SDK**: For building the cross-platform web application.
*   **Dart**: Programming language for Flutter.
*   **http package**: For making API calls to the backend.
*   **Provider (or other state management)**: (Assumed, though not explicitly detailed in current files - good to mention if used).

## Key Components (Illustrative)

*   **`lib/main.dart`**: Entry point of the application, sets up the main app widget.
*   **`lib/src/screens/chat_screen.dart`**: Main UI for displaying chat messages and input.
*   **`lib/src/services/api_service.dart`**: Handles communication with the backend API.
*   **`lib/src/widgets/message_bubble.dart`**: Widget for displaying individual chat messages.
*   **`lib/src/models/chat_message.dart`**: Data model for chat messages (if used beyond simple strings).

## Running Standalone (for Development - Not Recommended for Full App)

While Docker Compose is the recommended way, if you need to run the Flutter frontend standalone for specific development or testing tasks (e.g., for faster UI iteration with hot reload):

1.  **Ensure Flutter SDK is installed:** See [Flutter installation guide](https://flutter.dev/docs/get-started/install).
2.  **Navigate to the Flutter app directory:**
    ```bash
    cd flutter_chat_app
    ```
3.  **Get Flutter dependencies:**
    ```bash
    flutter pub get
    ```
4.  **Ensure the backend service is running and accessible.**
    *   You might run the backend via Docker Compose while working on the Flutter app standalone. In this case, the backend would be at `http://localhost:8000`.
    *   The `api_service.dart` defaults to `http://localhost:8000` which should work if the backend is exposed on that port.
5.  **Run the Application:**
    *   For web:
        ```bash
        flutter run -d chrome 
        ```
    *   Ensure an emulator is running or a device is connected if targeting mobile.

This setup is primarily for focused frontend development. For running the full application, always refer to the root `README.md`.

## Building for Web Manually (Not needed for Docker setup)

If you wanted to build the web app manually without Docker:
```bash
flutter build web --release --dart-define=BACKEND_URL=http://your_backend_url:8000
```
The output would be in `build/web`. You would then need to serve these static files using a web server. The Docker setup handles this automatically with Nginx.
