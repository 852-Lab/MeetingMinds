FROM debian:bookworm-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create bin and models directories
RUN mkdir -p bin models

# Download Sona Linux binary (AMD64)
# We use AMD64 even on ARM Mac because Sona's ARM binary has compatibility issues (SIGILL).
# Docker for Mac handles the emulation perfectly.
RUN curl -L https://github.com/thewh1teagle/sona/releases/download/v0.2.1/sona-linux-amd64 -o bin/sona \
    && chmod +x bin/sona

# Copy entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 52341

# Run the entrypoint
ENTRYPOINT ["./entrypoint.sh"]
