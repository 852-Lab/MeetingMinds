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


### 8.1 Logging

```swift
// Logger.swift
import OSLog

extension Logger {
    static let audio = Logger(subsystem: "com.meetingmind", category: "audio")
    static let ai = Logger(subsystem: "com.meetingmind", category: "ai")
    static let database = Logger(subsystem: "com.meetingmind", category: "database")
}

// Usage
Logger.audio.info("Started recording with duration: \(duration)")
Logger.ai.error("Transcription failed: \(error.localizedDescription)")
```

### 8.2 Crash Reporting

- Use native macOS crash logs
- Implement custom error boundary for non-fatal errors
- User-controlled opt-in for anonymous crash reports (local only)

---

## 9. Security Considerations

### 9.1 Data Protection

**Audio Files:**
- Store in sandboxed application support directory
- Optional encryption using CryptoKit (AES-GCM)
- Automatic cleanup of old recordings

**Database:**
- Use SQLite encryption extension (SQLCipher)
- Encrypt sensitive fields (meeting titles, transcripts)
- Secure erase on deletion

### 9.2 Network Security

**Ollama Communication:**
- Localhost-only connections (no remote access)
- Verify Ollama server identity
- Timeout protection against hanging requests

---

## 10. Future Enhancements

### 10.1 Advanced Features
- Real-time transcription during recording
- Speaker diarization with voice embeddings
- Sentiment analysis of meeting tone
- Multi-language translation

### 10.2 Integration Opportunities
- Calendar sync for automatic meeting detection
- Slack/Teams webhooks for instant sharing
- Obsidian/Notion export plugins
- AppleScript automation support

---

## Appendix A: Dependencies

**Swift Package Manager:**
```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/groue/GRDB.swift", from: "6.0.0"),
    .package(url: "https://github.com/Alamofire/Alamofire", from: "5.8.0"),
    .package(url: "https://github.com/apple/swift-log", from: "1.5.0")
]
```

**External Tools:**
- Ollama (https://ollama.ai) - v0.1.20+
- Whisper model - Base, Small, or Medium
- Llama 3.2 or Mistral 7B

---

**End of Technical Architecture Document**
