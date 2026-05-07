FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create bin and storage directories
RUN mkdir -p bin storage models

# Download Sona Linux binary
RUN curl -L https://github.com/thewh1teagle/sona/releases/download/v0.2.1/sona-linux-amd64 -o bin/sona \
    && chmod +x bin/sona

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
