import Foundation
import GRDB

// Summary record for database storage
struct SummaryRecord: Codable, Identifiable {
    var id: Int64?
    var meetingId: Int64
    var summaryJSON: String
    var modelUsed: String
    var createdAt: Date
    
    init(id: Int64? = nil, meetingId: Int64, summary: MeetingSummary, modelUsed: String) {
        self.id = id
        self.meetingId = meetingId
        self.summaryJSON = (try? JSONEncoder().encode(summary).base64EncodedString()) ?? "{}"
        self.modelUsed = modelUsed
        self.createdAt = Date()
    }
    
    var summary: MeetingSummary? {
        guard let data = Data(base64Encoded: summaryJSON),
              let summary = try? JSONDecoder().decode(MeetingSummary.self, from: data) else {
            return nil
        }
        return summary
    }
}

// GRDB conformance
extension SummaryRecord: FetchableRecord, MutablePersistableRecord {
    static let databaseTableName = "summaries"
    
    enum Columns {
        static let id = Column(CodingKeys.id)
        static let meetingId = Column(CodingKeys.meetingId)
        static let summaryJSON = Column(CodingKeys.summaryJSON)
        static let modelUsed = Column(CodingKeys.modelUsed)
        static let createdAt = Column(CodingKeys.createdAt)
    }
    
    mutating func didInsert(_ inserted: InsertionSuccess) {
        id = inserted.rowID
    }
}

// Meeting summary structure
struct MeetingSummary: Codable {
    var title: String
    var keyPoints: [String]
    var decisions: [Decision]
    var actionItems: [ActionItem]
    var nextSteps: [String]
    
    struct Decision: Codable, Identifiable {
        var id: UUID
        var text: String
        var timestamp: String
        
        init(id: UUID = UUID(), text: String, timestamp: String) {
            self.id = id
            self.text = text
            self.timestamp = timestamp
        }
    }
    
    struct ActionItem: Codable, Identifiable {
        var id: UUID
        var task: String
        var assignee: String?
        var dueDate: String?
        var completed: Bool
        
        init(id: UUID = UUID(), task: String, assignee: String? = nil, dueDate: String? = nil, completed: Bool = false) {
            self.id = id
            self.task = task
            self.assignee = assignee
            self.dueDate = dueDate
            self.completed = completed
        }
    }
}

// Export formats
extension MeetingSummary {
    func toMarkdown() -> String {
        var markdown = """
        # \(title)
        
        ## Executive Summary
        
        """
        
        for point in keyPoints {
            markdown += "- \(point)\n"
        }
        
        if !decisions.isEmpty {
            markdown += "\n## Key Decisions\n\n"
            for decision in decisions {
                markdown += "- \(decision.text) [Timestamp: \(decision.timestamp)]\n"
            }
        }
        
        if !actionItems.isEmpty {
            markdown += "\n## Action Items\n\n"
            for item in actionItems {
                let checkbox = item.completed ? "[x]" : "[ ]"
                var line = "\(checkbox) \(item.task)"
                if let assignee = item.assignee {
                    line += " - Assigned to: \(assignee)"
                }
                if let dueDate = item.dueDate {
                    line += " - Due: \(dueDate)"
                }
                markdown += line + "\n"
            }
        }
        
        if !nextSteps.isEmpty {
            markdown += "\n## Next Steps\n\n"
            for step in nextSteps {
                markdown += "- \(step)\n"
            }
        }
        
        return markdown
    }
}
