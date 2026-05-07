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

## Getting Started

### 1. Prerequisites
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

### 2. Setup
Simply run the following command to start the backend, frontend, and Ollama:
```bash
docker compose up --build
```

### 3. Pull LLM Model
Once the containers are running, you need to pull the `llama3.2` model into the Ollama container:
```bash
docker exec -it meetingminds-ollama-1 ollama pull llama3.2
```
*(Note: Container name might vary slightly depending on your directory name, use `docker ps` to check)*

The application will be available at:
- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend API: [http://localhost:8000](http://localhost:8000)

### 4. Whisper Model
On the first run, the system will look for the Whisper model in `src/backend/models`. If you already have it on your Mac, you can copy it there to save download time:
```bash
mkdir -p src/backend/models
cp ~/Library/Application\ Support/github.com.thewh1teagle.vibe/ggml-large-v3-turbo.bin src/backend/models/
```

## Usage

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
- **Data Persistence**: Uploaded files are stored in the `src/backend/storage` directory and are not uploaded to any cloud service.

### Dependencies
- **Backend**: FastAPI, Uvicorn, OpenAI (for Whisper compatibility), etc.
- **Frontend**: React, Vite, Tailwind CSS v4, Axios.

---

**End of Document**

