import Foundation
import OSLog

extension Logger {
    static let audio = Logger(subsystem: "com.meetingmind", category: "audio")
    static let ai = Logger(subsystem: "com.meetingmind", category: "ai")
    static let database = Logger(subsystem: "com.meetingmind", category: "database")
    static let app = Logger(subsystem: "com.meetingmind", category: "app")
}
