# jules-experiment

## FastAPI Chat Backend for Flutter App

This project contains the FastAPI backend that will serve as the API for a Flutter-based chat application. It connects to OpenRouter to provide chat completion services.

### Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API Key:**
    Create a file named `.env` in the root directory of the project. Copy the format from `.env.example`:
    ```
    OPENROUTER_API_KEY="YOUR_ACTUAL_OPENROUTER_API_KEY"
    ```
    Replace `"YOUR_ACTUAL_OPENROUTER_API_KEY"` with your valid OpenRouter API key.

5.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    The application will typically be available at `http://127.0.0.1:8000`. You can access the API documentation at `http://127.0.0.1:8000/docs`.