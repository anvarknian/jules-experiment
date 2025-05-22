# Flutter Chat Application

This Flutter application provides a mobile chat interface that connects to a FastAPI backend to interact with the OpenRouter API.

## Prerequisites

-   **Flutter SDK:** Ensure you have Flutter installed. See [Flutter installation guide](https://flutter.dev/docs/get-started/install).
-   **FastAPI Backend Running:** This Flutter app requires the companion FastAPI backend to be running and accessible.
    -   Follow the setup instructions in the main `README.md` of this repository to run the backend (it typically runs on `http://127.0.0.1:8000`).

## Getting Started

1.  **Navigate to the Flutter app directory:**
    ```bash
    cd flutter_chat_app
    ```

2.  **Get Flutter dependencies:**
    ```bash
    flutter pub get
    ```

3.  **Configure Backend URL (if necessary):**
    The application is configured by default to connect to the backend at `http://10.0.2.2:8000`. This is standard for Android emulators accessing the host machine's localhost.
    -   **iOS Simulator:** If you are running on an iOS simulator, `http://localhost:8000` or `http://127.0.0.1:8000` should work.
    -   **Physical Device:** If running on a physical Android or iOS device, you must use your computer's local network IP address (e.g., `http://192.168.1.X:8000`). Ensure your device is on the same Wi-Fi network as your computer and that your firewall allows connections to port 8000.

    To change the URL, modify the `_baseUrl` constant in `lib/src/services/api_service.dart`:
    ```dart
    // lib/src/services/api_service.dart
    // ...
    static const String _baseUrl = 'http://YOUR_BACKEND_IP_OR_HOSTNAME:8000'; 
    // ...
    ```
    Rebuild the app after changing the URL.

4.  **Run the Application:**
    -   Ensure an emulator is running or a device is connected.
    -   Execute the following command:
        ```bash
        flutter run
        ```
    -   For a release build, use `flutter run --release`.

## Manual Testing Checklist

Once the app is running and the FastAPI backend is active and accessible:

1.  **Launch the App:**
    -   [ ] Does the app launch successfully?
    -   [ ] Do you see the initial message "Connected to FastAPI backend! Send a message."?

2.  **Send a Message (Happy Path):**
    -   [ ] Type a message (e.g., "Hello") into the input field and press send.
    -   [ ] Does your message appear in the chat list, styled as a user message?
    -   [ ] Does a loading indicator appear briefly while waiting for the backend?
    -   [ ] Does a response from the AI assistant appear shortly after, styled as an assistant message? (Requires a VALID `OPENROUTER_API_KEY` in the backend's `.env` file).

3.  **Backend Not Running:**
    -   Stop the FastAPI backend server.
    -   [ ] Send a message from the app.
    -   [ ] Does an error message appear in the chat UI (e.g., "Error: Failed to connect to the chat service...")?
    -   Restart the backend server.

4.  **Invalid Backend API Key (Simulated):**
    -   If your backend's `OPENROUTER_API_KEY` is invalid or missing, the backend should return an error.
    -   [ ] Send a message.
    -   [ ] Does the app display an error message from the server (e.g., "Error: Error from server: Authentication error..." or "OpenRouter API key not configured.")?

5.  **Input Validation:**
    -   [ ] Try to send an empty message. Does the app prevent it or handle it gracefully? (Currently, the send button does nothing if the field is empty, which is acceptable).

6.  **UI & Styling:**
    -   [ ] Do chat bubbles look good on different length messages?
    -   [ ] Is the text input area clear and usable?
    -   [ ] Does scrolling work correctly, especially with many messages? Is the scrollbar visible?
    -   [ ] If you change your device theme (light/dark), does the app's theme adapt?

7.  **Loading State:**
    -   [ ] Is the loading indicator clear when sending a message?
    -   [ ] Is the input field and send button disabled during loading?
