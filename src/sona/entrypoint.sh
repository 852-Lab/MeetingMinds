#!/bin/bash
set -e

MODEL_PATH="/app/models/ggml-large-v3-turbo.bin"
MODEL_URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin"

if [ ! -f "$MODEL_PATH" ]; then
    echo "Whisper model not found at $MODEL_PATH"
    echo "Downloading model from $MODEL_URL..."
    curl -L "$MODEL_URL" -o "$MODEL_PATH"
    echo "Download complete."
else
    echo "Whisper model found at $MODEL_PATH"
fi

echo "Starting Sona server on port 52341..."
exec /app/bin/sona serve "$MODEL_PATH" --port 52341
