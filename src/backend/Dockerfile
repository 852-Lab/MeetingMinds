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

# Install dependencies using uv
# We copy pyproject.toml, uv.lock, and README.md from the root context
COPY pyproject.toml uv.lock README.md ./
# We copy the backend source code so setuptools can find it as defined in pyproject.toml
COPY src/backend ./src/backend

# Install the project dependencies
RUN uv pip install --system --no-cache .

# Create storage directories in the backend folder
RUN mkdir -p src/backend/storage src/backend/models

# Set working directory to the backend folder for execution
WORKDIR /app/src/backend

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
