import SwiftUI

@main
struct MeetingMindApp: App {
    @StateObject private var appState = AppState()
    
    var body: some Scene {
        MenuBarExtra("MeetingMind", systemImage: "brain.head.profile") {
            MenuBarView()
                .environmentObject(appState)
        }
        .menuBarExtraStyle(.window)
        
        // Settings window
        Settings {
            SettingsView()
                .environmentObject(appState)
        }
    }
}
