# MeetingMind - Local AI Meeting Assistant

MeetingMind is a privacy-first, locally-hosted AI meeting assistant that records, transcribes, and intelligently summarizes meetings without sending data to external servers. By leveraging local AI models through Ollama, the product ensures complete data privacy while delivering enterprise-grade meeting intelligence.

## Features

- **Local Processing**: Transcriptions and summaries are generated entirely on your machine.
- **Privacy First**: No data leaves your device.
- **Multilingual Support**: Supports English, German, and auto-detection.
- **YouTube Integration**: Download audio from YouTube videos for transcription.

## Architecture

The application consists of two main components:

1.  **Backend**: A FastAPI server handling audio processing, transcription (Whisper), and summarization (Ollama).
2.  **Frontend**: A React/Vite web interface for uploading files and viewing results.

## Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **FFmpeg**: Must be installed and available in your PATH.
- **Ollama**: Must be installed and running locally with the `llama3.2` model (or your preferred model).

## Getting Started

### 1. Start the Backend

Open a terminal and run:

```bash
./backend/run_backend.sh
```

This script will:
- Create a virtual environment (`backend/venv`) if it doesn't exist.
- Install necessary Python dependencies.
- Start the FastAPI server on `http://localhost:8000`.

### 2. Start the Frontend

Open a second terminal and run:

```bash
./frontend/run_frontend.sh
```

This script will:
- Install necessary Node.js dependencies.
- Start the Vite dev server on `http://localhost:5173`.

### 3. Usage

1.  Open your browser to `http://localhost:5173`.
2.  **Upload File**: Upload an audio or video file from your computer.
3.  **YouTube URL**: Paste a YouTube URL to download and process audio.
4.  **View Results**: Once processed, view the transcript and generate summaries or meeting notes.

## Troubleshooting

- **FFmpeg Error**: Ensure FFmpeg is installed (`brew install ffmpeg` on macOS).
- **Ollama Error**: Ensure Ollama is running (`ollama serve`) and the model is pulled (`ollama pull llama3.2`).
- **CSS Not Loading**: If the UI looks unstyled, ensure `@tailwindcss/postcss` is installed in the `frontend` directory and `postcss.config.js` is correctly configured.

---

## Technical Details

### Security & Privacy
- **Localhost Only**: All communication between the frontend, backend, and Ollama stays on `localhost`.
- **Data Persistence**: Uploaded files are stored in the `backend/storage` directory and are not uploaded to any cloud service.

### Dependencies
- **Backend**: FastAPI, Uvicorn, OpenAI (for Whisper compatibility), etc.
- **Frontend**: React, Vite, Tailwind CSS v4, Axios.

---

**End of Document**

