import SwiftUI

struct MeetingListView: View {
    @EnvironmentObject var appState: AppState
    @State private var meetings: [Meeting] = []
    @State private var searchText = ""
    @State private var selectedMeeting: Meeting?
    
    var body: some View {
        NavigationSplitView {
            // Sidebar - List of meetings
            VStack(spacing: 0) {
                // Search bar
                HStack {
                    Image(systemName: "magnifyingglass")
                        .foregroundColor(.secondary)
                    TextField("Search meetings...", text: $searchText)
                        .textFieldStyle(.plain)
                }
                .padding(8)
                .background(Color(.textBackgroundColor))
                .cornerRadius(8)
                .padding()
                
                Divider()
                
                // Meetings list
                List(filteredMeetings, selection: $selectedMeeting) { meeting in
                    NavigationLink(value: meeting) {
                        MeetingListRowView(meeting: meeting)
                    }
                }
                .listStyle(.sidebar)
            }
            .navigationTitle("Meetings")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button(action: refreshMeetings) {
                        Image(systemName: "arrow.clockwise")
                    }
                }
            }
            
        } detail: {
            // Detail view
            if let meeting = selectedMeeting {
                MeetingDetailView(meeting: meeting)
            } else {
                Text("Select a meeting to view details")
                    .foregroundColor(.secondary)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
        }
        .onAppear {
            refreshMeetings()
        }
    }
    
    private var filteredMeetings: [Meeting] {
        if searchText.isEmpty {
            return meetings
        } else {
            return meetings.filter { meeting in
                meeting.title.localizedCaseInsensitiveContains(searchText)
            }
        }
    }
    
    private func refreshMeetings() {
        do {
            meetings = try appState.databaseManager.fetchAllMeetings()
        } catch {
            print("Failed to fetch meetings: \(error)")
        }
    }
}

// MARK: - Meeting List Row

struct MeetingListRowView: View {
    let meeting: Meeting
    
    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(meeting.title)
                .font(.headline)
            
            HStack {
                Label(meeting.formattedDate, systemImage: "calendar")
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                Spacer()
                
                Label(meeting.formattedDuration, systemImage: "clock")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}

// MARK: - Meeting Detail View

struct MeetingDetailView: View {
    let meeting: Meeting
    @State private var selectedTab = 0
    @State private var transcript: Transcript?
    @State private var summary: SummaryRecord?
    
    var body: some View {
        VStack(spacing: 0) {
            // Header
            VStack(alignment: .leading, spacing: 8) {
                Text(meeting.title)
                    .font(.title)
                    .fontWeight(.bold)
                
                HStack {
                    Label(meeting.formattedDate, systemImage: "calendar")
                    Spacer()
                    Label(meeting.formattedDuration, systemImage: "clock")
                    if let language = meeting.language {
                        Spacer()
                        Label(language.uppercased(), systemImage: "globe")
                    }
                }
                .font(.subheadline)
                .foregroundColor(.secondary)
            }
            .padding()
            
            Divider()
            
            // Tab selector
            Picker("View", selection: $selectedTab) {
                Text("Transcript").tag(0)
                Text("Summary").tag(1)
            }
            .pickerStyle(.segmented)
            .padding()
            
            // Content
            TabView(selection: $selectedTab) {
                TranscriptView(transcript: transcript)
                    .tag(0)
                
                SummaryView(summary: summary?.summary)
                    .tag(1)
            }
            .tabViewStyle(.automatic)
        }
        .onAppear {
            loadMeetingData()
        }
    }
    
    private func loadMeetingData() {
        guard let meetingId = meeting.id else { return }
        
        do {
            transcript = try DatabaseManager.shared.fetchTranscript(forMeetingId: meetingId)
            summary = try DatabaseManager.shared.fetchSummary(forMeetingId: meetingId)
        } catch {
            print("Failed to load meeting data: \(error)")
        }
    }
}
