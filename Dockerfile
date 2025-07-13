# Stage 1: Build React frontend
FROM node:18 as frontend-builder
WORKDIR /app
COPY frontend/ .
RUN npm install && npm run build

# Stage 2: Build FastAPI backend and serve frontend
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpoppler-cpp-dev pkg-config tesseract-ocr && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY backend/ backend/
COPY prompts/ prompts/

# Copy built frontend from Stage 1
COPY --from=frontend-builder /app/build backend/static/

# Add CORS and Mount Static in main.py (see next step)

# Expose FastAPI port
EXPOSE 7860

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
