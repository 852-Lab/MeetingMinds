import Foundation
import GRDB

struct Meeting: Codable, Identifiable {
    var id: Int64?
    var title: String
    var date: Date
    var duration: Int // in seconds
    var audioFilePath: String?
    var language: String?
    var createdAt: Date
    
    init(id: Int64? = nil, title: String, date: Date, duration: Int, audioFilePath: String? = nil, language: String? = nil) {
        self.id = id
        self.title = title
        self.date = date
        self.duration = duration
        self.audioFilePath = audioFilePath
        self.language = language
        self.createdAt = Date()
    }
}

// GRDB conformance
extension Meeting: FetchableRecord, MutablePersistableRecord {
    static let databaseTableName = "meetings"
    
    enum Columns {
        static let id = Column(CodingKeys.id)
        static let title = Column(CodingKeys.title)
        static let date = Column(CodingKeys.date)
        static let duration = Column(CodingKeys.duration)
        static let audioFilePath = Column(CodingKeys.audioFilePath)
        static let language = Column(CodingKeys.language)
        static let createdAt = Column(CodingKeys.createdAt)
    }
    
    mutating func didInsert(_ inserted: InsertionSuccess) {
        id = inserted.rowID
    }
}

// Computed properties
extension Meeting {
    var formattedDuration: String {
        let hours = duration / 3600
        let minutes = (duration % 3600) / 60
        let seconds = duration % 60
        
        if hours > 0 {
            return String(format: "%d:%02d:%02d", hours, minutes, seconds)
        } else {
            return String(format: "%d:%02d", minutes, seconds)
        }
    }
    
    var formattedDate: String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .short
        return formatter.string(from: date)
    }
}
