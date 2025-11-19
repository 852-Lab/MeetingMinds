import Foundation
import GRDB

class DatabaseManager {
    static let shared = DatabaseManager()
    
    private var dbQueue: DatabaseQueue?
    
    private init() {
        do {
            let fileURL = try FileManager.default
                .url(for: .applicationSupportDirectory, in: .userDomainMask, appropriateFor: nil, create: true)
                .appendingPathComponent("MeetingMind")
            
            try FileManager.default.createDirectory(at: fileURL, withIntermediateDirectories: true)
            
            let dbPath = fileURL.appendingPathComponent("MeetingMind.db").path
            dbQueue = try DatabaseQueue(path: dbPath)
            
            try migrator.migrate(dbQueue!)
        } catch {
            fatalError("Database initialization failed: \(error)")
        }
    }
    
    // MARK: - Migrations
    
    private var migrator: DatabaseMigrator {
        var migrator = DatabaseMigrator()
        
        migrator.registerMigration("v1") { db in
            // Create meetings table
            try db.create(table: "meetings") { t in
                t.autoIncrementedPrimaryKey("id")
                t.column("title", .text).notNull()
                t.column("date", .datetime).notNull()
                t.column("duration", .integer).notNull()
                t.column("audioFilePath", .text)
                t.column("language", .text)
                t.column("createdAt", .datetime).notNull()
            }
            
            // Create transcripts table
            try db.create(table: "transcripts") { t in
                t.autoIncrementedPrimaryKey("id")
                t.column("meetingId", .integer).notNull()
                    .references("meetings", onDelete: .cascade)
                t.column("fullText", .text).notNull()
                t.column("segmentsJSON", .text).notNull()
                t.column("createdAt", .datetime).notNull()
            }
            
            // Create summaries table
            try db.create(table: "summaries") { t in
                t.autoIncrementedPrimaryKey("id")
                t.column("meetingId", .integer).notNull()
                    .references("meetings", onDelete: .cascade)
                t.column("summaryJSON", .text).notNull()
                t.column("modelUsed", .text).notNull()
                t.column("createdAt", .datetime).notNull()
            }
            
            // Create indexes
            try db.create(index: "idx_meetings_date", on: "meetings", columns: ["date"])
            try db.create(index: "idx_transcripts_meeting", on: "transcripts", columns: ["meetingId"])
            try db.create(index: "idx_summaries_meeting", on: "summaries", columns: ["meetingId"])
        }
        
        return migrator
    }
    
    // MARK: - Meeting Operations
    
    func saveMeeting(_ meeting: inout Meeting) throws -> Int64 {
        try dbQueue!.write { db in
            try meeting.insert(db)
            return db.lastInsertedRowID
        }
    }
    
    func fetchAllMeetings() throws -> [Meeting] {
        try dbQueue!.read { db in
            try Meeting
                .order(Meeting.Columns.date.desc)
                .fetchAll(db)
        }
    }
    
    func fetchRecentMeetings(limit: Int = 5) throws -> [Meeting] {
        try dbQueue!.read { db in
            try Meeting
                .order(Meeting.Columns.date.desc)
                .limit(limit)
                .fetchAll(db)
        }
    }
    
    func fetchMeeting(id: Int64) throws -> Meeting? {
        try dbQueue!.read { db in
            try Meeting.fetchOne(db, key: id)
        }
    }
    
    func deleteMeeting(id: Int64) throws {
        try dbQueue!.write { db in
            try Meeting.deleteOne(db, key: id)
        }
    }
    
    // MARK: - Transcript Operations
    
    func saveTranscript(_ transcript: inout Transcript) throws {
        try dbQueue!.write { db in
            try transcript.insert(db)
        }
    }
    
    func fetchTranscript(forMeetingId meetingId: Int64) throws -> Transcript? {
        try dbQueue!.read { db in
            try Transcript
                .filter(Transcript.Columns.meetingId == meetingId)
                .fetchOne(db)
        }
    }
    
    // MARK: - Summary Operations
    
    func saveSummary(_ summary: inout SummaryRecord) throws {
        try dbQueue!.write { db in
            try summary.insert(db)
        }
    }
    
    func fetchSummary(forMeetingId meetingId: Int64) throws -> SummaryRecord? {
        try dbQueue!.read { db in
            try SummaryRecord
                .filter(SummaryRecord.Columns.meetingId == meetingId)
                .fetchOne(db)
        }
    }
    
    // MARK: - Search
    
    func searchMeetings(query: String) throws -> [Meeting] {
        try dbQueue!.read { db in
            let pattern = "%\(query)%"
            let sql = """
                SELECT DISTINCT m.* FROM meetings m
                LEFT JOIN transcripts t ON m.id = t.meetingId
                WHERE m.title LIKE ? OR t.fullText LIKE ?
                ORDER BY m.date DESC
                """
            return try Meeting.fetchAll(db, sql: sql, arguments: [pattern, pattern])
        }
    }
}
