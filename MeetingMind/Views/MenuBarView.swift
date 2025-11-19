import SwiftUI
import UserNotifications

struct MenuBarView: View {
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        VStack(spacing: 0) {
            // Header
            headerView
            
            Divider()
            
            // Recording controls
            recordingControlsView
            
            Divider()
            
            // Recent meetings
            if !appState.recentMeetings.isEmpty {
                recentMeetingsView
                Divider()
            }
            
            // Footer
            footerView
        }
        .frame(width: 320)
    }
    
    // MARK: - Header
    
    private var headerView: some View {
        HStack {
            Image(systemName: "brain.head.profile")
                .font(.title2)
                .foregroundColor(.blue)
            Text("MeetingMind")
                .font(.headline)
            Spacer()
        }
        .padding()
    }
    
    // MARK: - Recording Controls
    
    private var recordingControlsView: some View {
        VStack(spacing: 12) {
            if appState.isRecording {
                // Recording indicator
                HStack {
                    Circle()
                        .fill(Color.red)
                        .frame(width: 12, height: 12)
                    
                    Text("Recording: \(formatDuration(appState.audioRecorder.recordingDuration))")
                        .font(.system(.body, design: .monospaced))
                }
                
                Button(action: {
                    Task {
                        try? await appState.stopRecording()
                    }
                }) {
                    Label("Stop Recording", systemImage: "stop.circle.fill")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.borderedProminent)
                .tint(.red)
                
            } else if appState.isProcessing {
                // Processing indicator
                VStack {
                    ProgressView()
                    Text("Processing meeting...")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
            } else {
                // Start recording button
                Button(action: {
                    Task {
                        do {
                            try await appState.startRecording()
                        } catch {
                            print("Failed to start recording: \(error)")
                        }
                    }
                }) {
                    Label("Start Recording", systemImage: "record.circle")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.borderedProminent)
            }
        }
        .padding()
    }
    
    // MARK: - Recent Meetings
    
    private var recentMeetingsView: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("Recent Meetings")
                .font(.caption)
                .foregroundColor(.secondary)
                .padding(.horizontal)
                .padding(.top, 8)
            
            ScrollView {
                VStack(spacing: 0) {
                    ForEach(appState.recentMeetings) { meeting in
                        MeetingRowView(meeting: meeting)
                            .onTapGesture {
                                appState.currentMeeting = meeting
                                appState.showMainWindow = true
                            }
                    }
                }
            }
            .frame(maxHeight: 200)
        }
    }
    
    // MARK: - Footer
    
    private var footerView: some View {
        HStack {
            Button("View All") {
                appState.showMainWindow = true
            }
            
            Spacer()
            
            Button("Settings") {
                appState.showSettings = true
            }
            
            Spacer()
            
            Button("Quit") {
                NSApplication.shared.terminate(nil)
            }
        }
        .buttonStyle(.plain)
        .padding()
    }
    
    // MARK: - Helpers
    
    private func formatDuration(_ duration: TimeInterval) -> String {
        let hours = Int(duration) / 3600
        let minutes = (Int(duration) % 3600) / 60
        let seconds = Int(duration) % 60
        
        if hours > 0 {
            return String(format: "%d:%02d:%02d", hours, minutes, seconds)
        } else {
            return String(format: "%d:%02d", minutes, seconds)
        }
    }
}

// MARK: - Meeting Row View

struct MeetingRowView: View {
    let meeting: Meeting
    
    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(meeting.title)
                    .font(.subheadline)
                    .lineLimit(1)
                
                HStack {
                    Text(meeting.formattedDate)
                        .font(.caption)
                        .foregroundColor(.secondary)
                    
                    Text("•")
                        .foregroundColor(.secondary)
                    
                    Text(meeting.formattedDuration)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            
            Spacer()
            
            Image(systemName: "chevron.right")
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding(.horizontal)
        .padding(.vertical, 8)
        .contentShape(Rectangle())
    }
}
