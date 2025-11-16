# Technical Architecture Document
# MeetingMind - Local AI Meeting Assistant

**Version:** 1.0  
**Date:** November 16, 2025  
**Authors:** Engineering Team

---

## 1. System Overview

MeetingMind is a native macOS application built with Swift and SwiftUI that provides local AI-powered meeting transcription and summarization. The system architecture prioritizes privacy, performance, and offline-first operation.

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      User Interface Layer                        │
│         (SwiftUI - Menu Bar App + Meeting Viewer)               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Application Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Meeting    │  │  Transcript  │  │   Summary    │         │
│  │  Controller  │  │   Manager    │  │   Generator  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Service Layer                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │    Audio     │  │   Ollama     │  │    Data      │         │
│  │   Recorder   │  │    Client    │  │   Storage    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  External Dependencies                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ScreenCapture │  │     Ollama    │  │    SQLite    │         │
│  │     Kit      │  │   (localhost) │  │   Database   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Specifications

### 2.1 Audio Recording Service

**Responsibility:** Capture system audio and microphone input

**Technologies:**
- ScreenCaptureKit (macOS 14.2+) for system audio
- AVFoundation for microphone capture
- CoreAudio for audio processing

**Key Classes:**

```swift
// AudioRecorder.swift
import ScreenCaptureKit
import AVFoundation

class AudioRecorder: NSObject, ObservableObject {
    @Published var isRecording = false
    @Published var recordingDuration: TimeInterval = 0

    private var stream: SCStream?
    private var audioEngine: AVAudioEngine?
    private var audioFile: AVAudioFile?
    private var streamOutput: AudioStreamOutput?

    // System audio setup
    func setupSystemAudioRecording() async throws {
        // Request permission
        guard await checkScreenRecordingPermission() else {
            throw RecordingError.permissionDenied
        }

        // Get available content
        let content = try await SCShareableContent.current

        // Create filter (capture system audio only, exclude app windows)
        let filter = SCContentFilter(
            display: content.displays.first!,
            excludingApplications: [],
            exceptingWindows: []
        )

        // Configure stream
        let streamConfig = SCStreamConfiguration()
        streamConfig.capturesAudio = true
        streamConfig.excludesCurrentProcessAudio = true
        streamConfig.sampleRate = 48000
        streamConfig.channelCount = 2

        // Create stream
        stream = SCStream(filter: filter, configuration: streamConfig, delegate: nil)

        // Add audio output
        streamOutput = AudioStreamOutput()
        try stream?.addStreamOutput(streamOutput!, type: .audio, sampleHandlerQueue: .main)
    }

    // Microphone setup
    func setupMicrophoneRecording() throws {
        audioEngine = AVAudioEngine()
        let inputNode = audioEngine!.inputNode
        let inputFormat = inputNode.outputFormat(forBus: 0)

        // Create audio file
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let audioFilename = documentsPath.appendingPathComponent("meeting_\(Date().timeIntervalSince1970).m4a")

        let settings: [String: Any] = [
            AVFormatIDKey: Int(kAudioFormatMPEG4AAC),
            AVSampleRateKey: 44100.0,
            AVNumberOfChannelsKey: 1,
            AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
        ]

        audioFile = try AVAudioFile(forWriting: audioFilename, settings: settings)

        // Install tap
        inputNode.installTap(onBus: 0, bufferSize: 4096, format: inputFormat) { [weak self] (buffer, time) in
            try? self?.audioFile?.write(from: buffer)
        }
    }

    // Start recording
    func startRecording() async throws {
        try await setupSystemAudioRecording()
        try setupMicrophoneRecording()

        try audioEngine?.start()
        try await stream?.startCapture()

        isRecording = true
        startDurationTimer()
    }

    // Stop recording
    func stopRecording() async throws -> URL {
        isRecording = false

        audioEngine?.stop()
        await stream?.stopCapture()

        guard let fileURL = audioFile?.url else {
            throw RecordingError.noFileCreated
        }

        return fileURL
    }
}

// Custom stream output handler
class AudioStreamOutput: NSObject, SCStreamOutput {
    func stream(_ stream: SCStream, didOutputSampleBuffer sampleBuffer: CMSampleBuffer, of type: SCStreamOutputType) {
        // Process audio buffer
        guard type == .audio else { return }

        // Write to file or process in real-time
        // Implementation depends on mixing strategy
    }
}

enum RecordingError: Error {
    case permissionDenied
    case noFileCreated
    case captureFailure
}
```

**Permission Handling:**

```swift
// PermissionManager.swift
class PermissionManager {
    func checkScreenRecordingPermission() async -> Bool {
        // Check using CGPreflightScreenCaptureAccess
        let hasPermission = CGPreflightScreenCaptureAccess()

        if !hasPermission {
            // Request permission
            CGRequestScreenCaptureAccess()
        }

        return hasPermission
    }

    func checkMicrophonePermission() async -> Bool {
        let status = AVCaptureDevice.authorizationStatus(for: .audio)

        switch status {
        case .authorized:
            return true
        case .notDetermined:
            return await AVCaptureDevice.requestAccess(for: .audio)
        case .denied, .restricted:
            return false
        @unknown default:
            return false
        }
    }
}
```

---

### 2.2 Ollama Integration Service

**Responsibility:** Interface with local Ollama server for transcription and summarization

**Technologies:**
- URLSession for HTTP requests
- Async/await for concurrent operations
- Combine for reactive updates

**Key Classes:**

```swift
// OllamaClient.swift
import Foundation

class OllamaClient {
    private let baseURL = "http://localhost:11434/api"
    private let session: URLSession

    init() {
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 300 // 5 minutes for large models
        session = URLSession(configuration: config)
    }

    // Check if Ollama is running
    func isOllamaRunning() async -> Bool {
        let url = URL(string: "\(baseURL)/tags")!
        do {
            let (_, response) = try await session.data(from: url)
            return (response as? HTTPURLResponse)?.statusCode == 200
        } catch {
            return false
        }
    }

    // Get available models
    func getAvailableModels() async throws -> [OllamaModel] {
        let url = URL(string: "\(baseURL)/tags")!
        let (data, _) = try await session.data(from: url)
        let response = try JSONDecoder().decode(ModelsResponse.self, from: data)
        return response.models
    }

    // Transcribe audio using Whisper
    func transcribe(audioURL: URL, language: String? = nil, model: String = "whisper:base") async throws -> TranscriptionResult {
        // Prepare audio data
        let audioData = try Data(contentsOf: audioURL)
        let base64Audio = audioData.base64EncodedString()

        // Create request
        var request = URLRequest(url: URL(string: "\(baseURL)/generate")!)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let prompt = """
        Transcribe the following audio accurately with timestamps. 
        Format: [HH:MM:SS] Speaker: Text
        Language: \(language ?? "auto-detect")
        """

        let body: [String: Any] = [
            "model": model,
            "prompt": prompt,
            "stream": false,
            "options": [
                "temperature": 0.0,
                "num_predict": -1
            ]
        ]

        request.httpBody = try JSONSerialization.data(withJSONObject: body)

        // Send request
        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
            throw OllamaError.requestFailed
        }

        let result = try JSONDecoder().decode(GenerateResponse.self, from: data)
        return parseTranscription(result.response)
    }

    // Generate summary using LLM
    func generateSummary(transcript: String, model: String = "llama3.2") async throws -> MeetingSummary {
        var request = URLRequest(url: URL(string: "\(baseURL)/generate")!)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let prompt = """
        Analyze the following meeting transcript and generate a structured summary.

        Format your response as JSON with this structure:
        {
          "title": "Meeting title or topic",
          "keyPoints": ["point 1", "point 2", ...],
          "decisions": [{"text": "decision", "timestamp": "HH:MM:SS"}],
          "actionItems": [{"task": "description", "assignee": "name or null", "dueDate": "date or null"}],
          "nextSteps": ["step 1", "step 2", ...]
        }

        Transcript:
        \(transcript)
        """

        let body: [String: Any] = [
            "model": model,
            "prompt": prompt,
            "stream": false,
            "format": "json",
            "options": [
                "temperature": 0.3,
                "top_p": 0.9
            ]
        ]

        request.httpBody = try JSONSerialization.data(withJSONObject: body)

        let (data, _) = try await session.data(for: request)
        let result = try JSONDecoder().decode(GenerateResponse.self, from: data)

        // Parse JSON response
        guard let summaryData = result.response.data(using: .utf8) else {
            throw OllamaError.invalidResponse
        }

        return try JSONDecoder().decode(MeetingSummary.self, from: summaryData)
    }
}

// Data models
struct OllamaModel: Codable {
    let name: String
    let size: Int64
    let modified: Date
}

struct ModelsResponse: Codable {
    let models: [OllamaModel]
}

struct GenerateResponse: Codable {
    let response: String
    let model: String
    let done: Bool
}

struct TranscriptionResult {
    let text: String
    let segments: [TranscriptSegment]
    let language: String
}

struct TranscriptSegment: Codable {
    let timestamp: TimeInterval
    let text: String
    let confidence: Double?
}

struct MeetingSummary: Codable {
    let title: String
    let keyPoints: [String]
    let decisions: [Decision]
    let actionItems: [ActionItem]
    let nextSteps: [String]

    struct Decision: Codable {
        let text: String
        let timestamp: String
    }

    struct ActionItem: Codable {
        let task: String
        let assignee: String?
        let dueDate: String?
    }
}

enum OllamaError: Error {
    case notRunning
    case requestFailed
    case invalidResponse
    case modelNotFound
}
```

---

### 2.3 Data Storage Layer

**Responsibility:** Persist meetings, transcripts, and summaries locally

**Technologies:**
- SQLite database via GRDB.swift
- File system for audio files
- JSON for structured data

**Database Schema:**

```sql
-- meetings table
CREATE TABLE meetings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date DATETIME NOT NULL,
    duration INTEGER NOT NULL, -- in seconds
    audio_file_path TEXT,
    language TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- transcripts table
CREATE TABLE transcripts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL,
    full_text TEXT NOT NULL,
    segments_json TEXT, -- JSON array of segments with timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
);

-- summaries table
CREATE TABLE summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL,
    summary_json TEXT NOT NULL, -- JSON with keyPoints, actionItems, etc.
    model_used TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
);

-- indexes
CREATE INDEX idx_meetings_date ON meetings(date DESC);
CREATE INDEX idx_transcripts_meeting ON transcripts(meeting_id);
CREATE INDEX idx_summaries_meeting ON summaries(meeting_id);
```

**Swift Models:**

```swift
// Models.swift
import GRDB

struct Meeting: Codable, FetchableRecord, PersistableRecord {
    var id: Int64?
    var title: String
    var date: Date
    var duration: Int
    var audioFilePath: String?
    var language: String?
    var createdAt: Date

    // Relationships
    var transcript: Transcript?
    var summary: MeetingSummary?
}

struct Transcript: Codable, FetchableRecord, PersistableRecord {
    var id: Int64?
    var meetingId: Int64
    var fullText: String
    var segmentsJSON: String
    var createdAt: Date

    // Computed property for segments
    var segments: [TranscriptSegment] {
        guard let data = segmentsJSON.data(using: .utf8),
              let segments = try? JSONDecoder().decode([TranscriptSegment].self, from: data) else {
            return []
        }
        return segments
    }
}

// Database manager
class DatabaseManager {
    static let shared = DatabaseManager()
    private var dbQueue: DatabaseQueue?

    init() {
        do {
            let fileURL = try FileManager.default
                .url(for: .applicationSupportDirectory, in: .userDomainMask, appropriateFor: nil, create: true)
                .appendingPathComponent("MeetingMind.db")

            dbQueue = try DatabaseQueue(path: fileURL.path)
            try migrator.migrate(dbQueue!)
        } catch {
            fatalError("Database initialization failed: \(error)")
        }
    }

    // Save meeting
    func saveMeeting(_ meeting: Meeting) throws -> Int64 {
        try dbQueue!.write { db in
            try meeting.insert(db)
            return db.lastInsertedRowID
        }
    }

    // Save transcript
    func saveTranscript(_ transcript: Transcript) throws {
        try dbQueue!.write { db in
            try transcript.insert(db)
        }
    }

    // Fetch all meetings
    func fetchAllMeetings() throws -> [Meeting] {
        try dbQueue!.read { db in
            try Meeting.order(Column("date").desc).fetchAll(db)
        }
    }

    // Search meetings
    func searchMeetings(query: String) throws -> [Meeting] {
        try dbQueue!.read { db in
            let pattern = "%\(query)%"
            let sql = """
                SELECT DISTINCT m.* FROM meetings m
                LEFT JOIN transcripts t ON m.id = t.meeting_id
                WHERE m.title LIKE ? OR t.full_text LIKE ?
                ORDER BY m.date DESC
                """
            return try Meeting.fetchAll(db, sql: sql, arguments: [pattern, pattern])
        }
    }
}
```

---

## 3. User Interface Components

### 3.1 Menu Bar App

```swift
// MeetingMindApp.swift
import SwiftUI

@main
struct MeetingMindApp: App {
    @StateObject private var appState = AppState()

    var body: some Scene {
        MenuBarExtra("MeetingMind", systemImage: "mic.circle.fill") {
            MenuBarView()
                .environmentObject(appState)
        }
        .menuBarExtraStyle(.window)
    }
}

// MenuBarView.swift
struct MenuBarView: View {
    @EnvironmentObject var appState: AppState
    @StateObject private var recorder = AudioRecorder()

    var body: some View {
        VStack(spacing: 0) {
            // Header
            HStack {
                Image(systemName: "brain.head.profile")
                Text("MeetingMind")
                    .font(.headline)
                Spacer()
            }
            .padding()

            Divider()

            // Recording controls
            if recorder.isRecording {
                VStack {
                    HStack {
                        Circle()
                            .fill(Color.red)
                            .frame(width: 12, height: 12)
                            .animation(.easeInOut(duration: 1).repeatForever(), value: recorder.isRecording)

                        Text("Recording: \(formatDuration(recorder.recordingDuration))")
                            .font(.system(.body, design: .monospaced))
                    }

                    Button("Stop Recording") {
                        Task {
                            await stopAndProcess()
                        }
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(.red)
                }
                .padding()
            } else {
                Button {
                    Task {
                        try? await recorder.startRecording()
                    }
                } label: {
                    Label("Start Recording", systemImage: "record.circle")
                }
                .buttonStyle(.borderedProminent)
                .padding()
            }

            Divider()

            // Recent meetings
            List(appState.recentMeetings) { meeting in
                MeetingRow(meeting: meeting)
            }
            .frame(height: 200)

            Divider()

            // Footer buttons
            HStack {
                Button("View All") {
                    appState.showMainWindow = true
                }

                Spacer()

                Button("Settings") {
                    appState.showSettings = true
                }
            }
            .padding()
        }
        .frame(width: 320)
    }

    private func stopAndProcess() async {
        do {
            let audioURL = try await recorder.stopRecording()

            // Start processing
            appState.isProcessing = true

            // Transcribe
            let ollamaClient = OllamaClient()
            let transcription = try await ollamaClient.transcribe(audioURL: audioURL)

            // Generate summary
            let summary = try await ollamaClient.generateSummary(transcript: transcription.text)

            // Save to database
            let meeting = Meeting(
                title: summary.title,
                date: Date(),
                duration: Int(recorder.recordingDuration),
                audioFilePath: audioURL.path,
                language: transcription.language,
                createdAt: Date()
            )

            let meetingId = try DatabaseManager.shared.saveMeeting(meeting)

            // Show notification
            showNotification(title: "Meeting Processed", message: "Summary ready to view")

            appState.isProcessing = false
        } catch {
            print("Error processing meeting: \(error)")
        }
    }
}
```

---

## 4. Implementation Timeline

### Week 1-2: Foundation
- [ ] Set up Xcode project with SPM dependencies
- [ ] Implement audio recording with ScreenCaptureKit
- [ ] Build basic menu bar UI
- [ ] Test audio capture on multiple devices

### Week 3-4: AI Integration
- [ ] Create Ollama client wrapper
- [ ] Implement Whisper transcription pipeline
- [ ] Add LLM summarization
- [ ] Test accuracy with sample audio

### Week 5-6: Data & UI
- [ ] Set up SQLite database
- [ ] Build meeting viewer UI
- [ ] Add export functionality
- [ ] Polish UX and handle edge cases

---

## 5. Performance Considerations

### 5.1 Optimization Strategies

**Audio Processing:**
- Use hardware-accelerated encoding (VideoToolbox)
- Buffer audio in chunks to prevent memory overflow
- Compress recordings to M4A (AAC) format

**AI Processing:**
- Process transcription in parallel with recording when possible
- Cache frequently used models in memory
- Use quantized models on older Macs (INT8)

**Database:**
- Index frequently searched columns
- Use prepared statements
- Lazy load transcript segments

### 5.2 Resource Limits

| Component | RAM Usage | CPU Usage | Disk Space |
|-----------|-----------|-----------|------------|
| Audio Recording | ~100MB | 5-10% | 1MB/min |
| Whisper Base | ~1GB | 30-50% | 150MB model |
| Llama 3.2 3B | ~2GB | 40-60% | 2GB model |
| **Total (Recording)** | ~3.1GB | ~50-70% | - |

---

## 6. Testing Strategy

### 6.1 Unit Tests
- Audio recorder state management
- Ollama client request/response parsing
- Database CRUD operations
- Timestamp formatting utilities

### 6.2 Integration Tests
- End-to-end recording → transcription → summary pipeline
- Permission handling flows
- Model loading and fallback mechanisms

### 6.3 Manual Testing Checklist
- [ ] Record 5min meeting and verify audio quality
- [ ] Test on Intel and Apple Silicon Macs
- [ ] Verify transcription accuracy (90%+ WER)
- [ ] Check summary quality with 3 different meeting types
- [ ] Test with English, German, and mixed-language audio

---

## 7. Deployment

### 7.1 Build Configuration

**Release Build:**
```bash
xcodebuild -scheme MeetingMind \
  -configuration Release \
  -archivePath ./build/MeetingMind.xcarchive \
  archive

xcodebuild -exportArchive \
  -archivePath ./build/MeetingMind.xcarchive \
  -exportPath ./build/Release \
  -exportOptionsPlist ExportOptions.plist
```

**Code Signing:**
- Developer ID Application certificate
- Notarization via Apple notary service
- Hardened runtime enabled

### 7.2 Distribution

**Initial POC:**
- Direct download (.dmg file)
- Installation via drag-and-drop
- Bundled setup guide for Ollama

**Future:**
- Mac App Store distribution (if compliant)
- Homebrew cask
- Auto-update via Sparkle framework

---

## 8. Monitoring & Observability

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
