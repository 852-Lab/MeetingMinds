FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    ca-certificates \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create storage directory
RUN mkdir -p storage models

# Install dependencies using uv
# We copy pyproject.toml and uv.lock from the root context
COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-cache .

# Copy application code from src/backend
COPY src/backend .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
