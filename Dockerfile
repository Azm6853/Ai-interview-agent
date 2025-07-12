# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional, but useful for resume parsing or tesseract if needed)
RUN apt-get update && apt-get install -y build-essential libpoppler-cpp-dev pkg-config tesseract-ocr && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ backend/
COPY prompts/ prompts/

# Expose default HF Spaces port
EXPOSE 7860

# Start the app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
