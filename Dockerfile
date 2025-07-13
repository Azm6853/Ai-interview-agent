# Stage 1: Build frontend
FROM node:18 AS frontend

WORKDIR /frontend
COPY frontend/ ./
RUN npm install && npm run build

# Stage 2: Backend + Serve built frontend
FROM python:3.10-slim AS backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential libpoppler-cpp-dev pkg-config tesseract-ocr curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ backend/
COPY prompts/ prompts/

# Copy built frontend
COPY --from=frontend /frontend/build ./frontend_build

# Expose FastAPI port
EXPOSE 7860

# Start server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
