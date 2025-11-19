import Foundation
import GRDB

struct Transcript: Codable, Identifiable {
    var id: Int64?
    var meetingId: Int64
    var fullText: String
    var segmentsJSON: String
    var createdAt: Date
    
    init(id: Int64? = nil, meetingId: Int64, fullText: String, segments: [TranscriptSegment]) {
        self.id = id
        self.meetingId = meetingId
        self.fullText = fullText
        self.segmentsJSON = (try? JSONEncoder().encode(segments).base64EncodedString()) ?? "[]"
        self.createdAt = Date()
    }
    
    var segments: [TranscriptSegment] {
        guard let data = Data(base64Encoded: segmentsJSON),
              let segments = try? JSONDecoder().decode([TranscriptSegment].self, from: data) else {
            return []
        }
        return segments
    }
}

// GRDB conformance
extension Transcript: FetchableRecord, MutablePersistableRecord {
    static let databaseTableName = "transcripts"
    
    enum Columns {
        static let id = Column(CodingKeys.id)
        static let meetingId = Column(CodingKeys.meetingId)
        static let fullText = Column(CodingKeys.fullText)
        static let segmentsJSON = Column(CodingKeys.segmentsJSON)
        static let createdAt = Column(CodingKeys.createdAt)
    }
    
    mutating func didInsert(_ inserted: InsertionSuccess) {
        id = inserted.rowID
    }
}

// Transcript segment model
struct TranscriptSegment: Codable, Identifiable {
    var id: UUID
    var timestamp: TimeInterval
    var text: String
    var confidence: Double?
    
    init(id: UUID = UUID(), timestamp: TimeInterval, text: String, confidence: Double? = nil) {
        self.id = id
        self.timestamp = timestamp
        self.text = text
        self.confidence = confidence
    }
    
    var formattedTimestamp: String {
        let hours = Int(timestamp) / 3600
        let minutes = (Int(timestamp) % 3600) / 60
        let seconds = Int(timestamp) % 60
        
        if hours > 0 {
            return String(format: "%02d:%02d:%02d", hours, minutes, seconds)
        } else {
            return String(format: "%02d:%02d", minutes, seconds)
        }
    }
}
