# Stage 1: Build frontend
FROM node:18 as frontend
WORKDIR /frontend
COPY frontend/ .
RUN npm install && npm run build

# Stage 2: Backend + frontend serving
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (tesseract + poppler for resume parsing)
RUN apt-get update && apt-get install -y build-essential libpoppler-cpp-dev pkg-config tesseract-ocr && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and prompt code
COPY backend/ ./backend/
COPY prompts/ ./prompts/

# Copy built frontend into backend/static
COPY --from=frontend /frontend/build ./backend/static

# Expose port
EXPOSE 7860

# Start FastAPI server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
