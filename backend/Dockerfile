# Start from a suitable Python base image
FROM python:3.9-slim

# Set a working directory
WORKDIR /app

# Copy the requirements.txt file from the backend directory into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy all files from the backend directory into the container's working directory
COPY . .

# Specify the command to run the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
