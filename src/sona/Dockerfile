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

# Use build args to determine architecture
ARG TARGETARCH

# Download correct Sona binary based on architecture
RUN if [ "$TARGETARCH" = "arm64" ]; then \
        curl -L https://github.com/thewh1teagle/sona/releases/download/v0.2.1/sona-linux-arm64 -o bin/sona; \
    else \
        curl -L https://github.com/thewh1teagle/sona/releases/download/v0.2.1/sona-linux-amd64 -o bin/sona; \
    fi \
    && chmod +x bin/sona

# Copy entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 52341

# Run the entrypoint
ENTRYPOINT ["./entrypoint.sh"]
