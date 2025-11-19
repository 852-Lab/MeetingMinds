import Foundation
import SwiftUI

@MainActor
class AppState: ObservableObject {
    @Published var isRecording = false
    @Published var isProcessing = false
    @Published var recentMeetings: [Meeting] = []
    @Published var showMainWindow = false
    @Published var showSettings = false
    @Published var currentMeeting: Meeting?
    
    // Services
    let audioRecorder = AudioRecorder()
    let ollamaClient = OllamaClient()
    let databaseManager = DatabaseManager.shared
    let permissionManager = PermissionManager()
    
    init() {
        loadRecentMeetings()
    }
    
    func loadRecentMeetings() {
        do {
            recentMeetings = try databaseManager.fetchRecentMeetings(limit: 5)
        } catch {
            print("Failed to load recent meetings: \(error)")
        }
    }
    
    func startRecording() async throws {
        // Check permissions first
        guard await permissionManager.checkAllPermissions() else {
            throw AppError.permissionsNotGranted
        }
        
        try await audioRecorder.startRecording()
        isRecording = true
    }
    
    func stopRecording() async throws {
        let audioURL = try await audioRecorder.stopRecording()
        isRecording = false
        isProcessing = true
        
        // Process in background
        Task {
            await processRecording(audioURL: audioURL)
        }
    }
    
    private func processRecording(audioURL: URL) async {
        do {
            // Transcribe
            let transcription = try await ollamaClient.transcribe(audioURL: audioURL)
            
            // Generate summary
            let summary = try await ollamaClient.generateSummary(transcript: transcription.text)
            
            // Save to database
            var meeting = Meeting(
                title: summary.title,
                date: Date(),
                duration: Int(audioRecorder.recordingDuration),
                audioFilePath: audioURL.path,
                language: transcription.language
            )
            
            let meetingId = try databaseManager.saveMeeting(&meeting)
            
            var transcript = Transcript(
                meetingId: meetingId,
                fullText: transcription.text,
                segments: transcription.segments
            )
            try databaseManager.saveTranscript(&transcript)
            
            var summaryRecord = SummaryRecord(
                meetingId: meetingId,
                summary: summary,
                modelUsed: "llama3.2"
            )
            try databaseManager.saveSummary(&summaryRecord)
            
            // Reload recent meetings
            loadRecentMeetings()
            
            // Show notification
            sendNotification(title: "Meeting Processed", message: summary.title)
            
        } catch {
            print("Failed to process recording: \(error)")
        }
        
        isProcessing = false
    }
    
    private func sendNotification(title: String, message: String) {
        let content = UNMutableNotificationContent()
        content.title = title
        content.body = message
        content.sound = .default
        
        let request = UNNotificationRequest(
            identifier: UUID().uuidString,
            content: content,
            trigger: nil
        )
        
        UNUserNotificationCenter.current().add(request)
    }
}

enum AppError: Error {
    case permissionsNotGranted
    case recordingFailed
    case processingFailed
}
