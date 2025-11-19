import SwiftUI

struct SummaryView: View {
    let summary: MeetingSummary?
    @State private var showExportSheet = false
    
    var body: some View {
        ScrollView {
            if let summary = summary {
                VStack(alignment: .leading, spacing: 24) {
                    // Executive Summary
                    SectionView(title: "Executive Summary", icon: "doc.text.fill") {
                        VStack(alignment: .leading, spacing: 8) {
                            ForEach(summary.keyPoints, id: \.self) { point in
                                HStack(alignment: .top, spacing: 8) {
                                    Image(systemName: "circle.fill")
                                        .font(.system(size: 6))
                                        .foregroundColor(.blue)
                                        .padding(.top, 6)
                                    Text(point)
                                }
                            }
                        }
                    }
                    
                    // Key Decisions
                    if !summary.decisions.isEmpty {
                        SectionView(title: "Key Decisions", icon: "checkmark.circle.fill") {
                            VStack(alignment: .leading, spacing: 12) {
                                ForEach(summary.decisions) { decision in
                                    DecisionRowView(decision: decision)
                                }
                            }
                        }
                    }
                    
                    // Action Items
                    if !summary.actionItems.isEmpty {
                        SectionView(title: "Action Items", icon: "list.bullet.circle.fill") {
                            VStack(alignment: .leading, spacing: 12) {
                                ForEach(summary.actionItems) { item in
                                    ActionItemRowView(item: item)
                                }
                            }
                        }
                    }
                    
                    // Next Steps
                    if !summary.nextSteps.isEmpty {
                        SectionView(title: "Next Steps", icon: "arrow.right.circle.fill") {
                            VStack(alignment: .leading, spacing: 8) {
                                ForEach(summary.nextSteps, id: \.self) { step in
                                    HStack(alignment: .top, spacing: 8) {
                                        Image(systemName: "arrow.right")
                                            .font(.caption)
                                            .foregroundColor(.green)
                                            .padding(.top, 2)
                                        Text(step)
                                    }
                                }
                            }
                        }
                    }
                    
                    // Export button
                    Button(action: { showExportSheet = true }) {
                        Label("Export Summary", systemImage: "square.and.arrow.up")
                            .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.borderedProminent)
                    .padding(.top)
                }
                .padding()
            } else {
                VStack(spacing: 16) {
                    Image(systemName: "doc.text.magnifyingglass")
                        .font(.system(size: 48))
                        .foregroundColor(.secondary)
                    
                    Text("No summary available")
                        .font(.headline)
                        .foregroundColor(.secondary)
                    
                    Text("The summary is still being generated or was not created.")
                        .font(.caption)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .padding()
            }
        }
        .sheet(isPresented: $showExportSheet) {
            if let summary = summary {
                ExportView(summary: summary)
            }
        }
    }
}

// MARK: - Section View

struct SectionView<Content: View>: View {
    let title: String
    let icon: String
    @ViewBuilder let content: Content
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Label(title, systemImage: icon)
                .font(.headline)
                .foregroundColor(.primary)
            
            content
        }
        .padding()
        .background(Color(.controlBackgroundColor))
        .cornerRadius(12)
    }
}

// MARK: - Decision Row

struct DecisionRowView: View {
    let decision: MeetingSummary.Decision
    
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: "checkmark.circle.fill")
                .foregroundColor(.green)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(decision.text)
                Text(decision.timestamp)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
    }
}

// MARK: - Action Item Row

struct ActionItemRowView: View {
    let item: MeetingSummary.ActionItem
    
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: item.completed ? "checkmark.square.fill" : "square")
                .foregroundColor(item.completed ? .green : .secondary)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(item.task)
                    .strikethrough(item.completed)
                
                HStack {
                    if let assignee = item.assignee {
                        Label(assignee, systemImage: "person.fill")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    
                    if let dueDate = item.dueDate {
                        Label(dueDate, systemImage: "calendar")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
            }
        }
    }
}

// MARK: - Export View

struct ExportView: View {
    let summary: MeetingSummary
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Export Summary")
                .font(.title2)
                .fontWeight(.bold)
            
            VStack(spacing: 12) {
                Button(action: { exportAsMarkdown() }) {
                    Label("Export as Markdown", systemImage: "doc.text")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.borderedProminent)
                
                Button(action: { exportAsText() }) {
                    Label("Export as Plain Text", systemImage: "doc.plaintext")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.bordered)
                
                Button(action: { copyToClipboard() }) {
                    Label("Copy to Clipboard", systemImage: "doc.on.clipboard")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.bordered)
            }
            
            Button("Cancel") {
                dismiss()
            }
            .buttonStyle(.plain)
        }
        .padding()
        .frame(width: 400)
    }
    
    private func exportAsMarkdown() {
        let markdown = summary.toMarkdown()
        saveFile(content: markdown, filename: "\(summary.title).md")
    }
    
    private func exportAsText() {
        let text = summary.toMarkdown() // Can be simplified for plain text
        saveFile(content: text, filename: "\(summary.title).txt")
    }
    
    private func copyToClipboard() {
        let markdown = summary.toMarkdown()
        NSPasteboard.general.clearContents()
        NSPasteboard.general.setString(markdown, forType: .string)
        dismiss()
    }
    
    private func saveFile(content: String, filename: String) {
        let savePanel = NSSavePanel()
        savePanel.nameFieldStringValue = filename
        savePanel.begin { response in
            if response == .OK, let url = savePanel.url {
                try? content.write(to: url, atomically: true, encoding: .utf8)
            }
            dismiss()
        }
    }
}
