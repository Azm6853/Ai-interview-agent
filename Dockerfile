# Stage 1: Install Python dependencies
FROM python:3.10-slim AS backend

WORKDIR /app

# System dependencies for resume parsing
RUN apt-get update && apt-get install -y build-essential libpoppler-cpp-dev pkg-config tesseract-ocr curl && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ backend/
COPY prompts/ prompts/
COPY main.py .

# Stage 2: Build React frontend
FROM node:18 AS frontend

WORKDIR /frontend
COPY frontend/ .          # This includes src/, public/, package.json, etc.
RUN npm install && npm run build

# Stage 3: Final unified image
FROM python:3.10-slim

WORKDIR /app

# Copy Python environment from backend stage
COPY --from=backend /app /app

# Copy built React app from frontend stage
COPY --from=frontend /frontend/build /app/frontend/build

# Expose port
EXPOSE 7860

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
