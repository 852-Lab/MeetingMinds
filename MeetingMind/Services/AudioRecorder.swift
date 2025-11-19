import Foundation
import ScreenCaptureKit
import AVFoundation
import Combine

@MainActor
class AudioRecorder: NSObject, ObservableObject {
    @Published var isRecording = false
    @Published var recordingDuration: TimeInterval = 0
    
    private var stream: SCStream?
    private var audioEngine: AVAudioEngine?
    private var audioFile: AVAudioFile?
    private var streamOutput: AudioStreamOutput?
    private var durationTimer: Timer?
    private var recordingStartTime: Date?
    
    // Start recording both system audio and microphone
    func startRecording() async throws {
        guard !isRecording else { return }
        
        // Setup system audio recording
        try await setupSystemAudioRecording()
        
        // Setup microphone recording
        try setupMicrophoneRecording()
        
        // Start both
        try audioEngine?.start()
        try await stream?.startCapture()
        
        isRecording = true
        recordingStartTime = Date()
        startDurationTimer()
    }
    
    // Stop recording and return audio file URL
    func stopRecording() async throws -> URL {
        guard isRecording else {
            throw RecordingError.notRecording
        }
        
        isRecording = false
        durationTimer?.invalidate()
        
        audioEngine?.stop()
        await stream?.stopCapture()
        
        guard let fileURL = audioFile?.url else {
            throw RecordingError.noFileCreated
        }
        
        // Reset state
        recordingDuration = 0
        recordingStartTime = nil
        
        return fileURL
    }
    
    // MARK: - Private Setup Methods
    
    private func setupSystemAudioRecording() async throws {
        // Get available content
        let content = try await SCShareableContent.current
        
        guard let display = content.displays.first else {
            throw RecordingError.noDisplayFound
        }
        
        // Create filter (capture system audio only)
        let filter = SCContentFilter(
            display: display,
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
        
        // Add audio output handler
        streamOutput = AudioStreamOutput()
        try stream?.addStreamOutput(streamOutput!, type: .audio, sampleHandlerQueue: .main)
    }
    
    private func setupMicrophoneRecording() throws {
        audioEngine = AVAudioEngine()
        
        guard let audioEngine = audioEngine else {
            throw RecordingError.audioEngineInitFailed
        }
        
        let inputNode = audioEngine.inputNode
        let inputFormat = inputNode.outputFormat(forBus: 0)
        
        // Create audio file
        let audioFilename = createAudioFileURL()
        
        let settings: [String: Any] = [
            AVFormatIDKey: Int(kAudioFormatMPEG4AAC),
            AVSampleRateKey: 44100.0,
            AVNumberOfChannelsKey: 1,
            AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
        ]
        
        audioFile = try AVAudioFile(forWriting: audioFilename, settings: settings)
        
        // Install tap on microphone input
        inputNode.installTap(onBus: 0, bufferSize: 4096, format: inputFormat) { [weak self] buffer, _ in
            try? self?.audioFile?.write(from: buffer)
        }
    }
    
    private func createAudioFileURL() -> URL {
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let timestamp = Int(Date().timeIntervalSince1970)
        return documentsPath.appendingPathComponent("meeting_\(timestamp).m4a")
    }
    
    private func startDurationTimer() {
        durationTimer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            guard let self = self, let startTime = self.recordingStartTime else { return }
            self.recordingDuration = Date().timeIntervalSince(startTime)
        }
    }
}

// Custom stream output handler for system audio
class AudioStreamOutput: NSObject, SCStreamOutput {
    func stream(_ stream: SCStream, didOutputSampleBuffer sampleBuffer: CMSampleBuffer, of type: SCStreamOutputType) {
        guard type == .audio else { return }
        
        // Process audio buffer
        // In a full implementation, this would mix system audio with microphone
        // For POC, we're primarily using microphone recording
    }
}

// Recording errors
enum RecordingError: Error, LocalizedError {
    case permissionDenied
    case noFileCreated
    case captureFailure
    case notRecording
    case noDisplayFound
    case audioEngineInitFailed
    
    var errorDescription: String? {
        switch self {
        case .permissionDenied:
            return "Screen recording permission denied"
        case .noFileCreated:
            return "Failed to create audio file"
        case .captureFailure:
            return "Audio capture failed"
        case .notRecording:
            return "Not currently recording"
        case .noDisplayFound:
            return "No display found for recording"
        case .audioEngineInitFailed:
            return "Failed to initialize audio engine"
        }
    }
}
