import SwiftUI

struct SettingsView: View {
    @EnvironmentObject var appState: AppState
    @State private var selectedWhisperModel = "whisper:base"
    @State private var selectedLLMModel = "llama3.2"
    @State private var primaryLanguage = "en"
    @State private var autoDetectLanguage = true
    @State private var availableModels: [OllamaModel] = []
    
    var body: some View {
        TabView {
            // General Settings
            generalSettingsView
                .tabItem {
                    Label("General", systemImage: "gear")
                }
            
            // AI Models
            modelsSettingsView
                .tabItem {
                    Label("AI Models", systemImage: "brain")
                }
            
            // Privacy
            privacySettingsView
                .tabItem {
                    Label("Privacy", systemImage: "lock.shield")
                }
        }
        .frame(width: 500, height: 400)
        .onAppear {
            loadAvailableModels()
        }
    }
    
    // MARK: - General Settings
    
    private var generalSettingsView: some View {
        Form {
            Section("Language Preferences") {
                Picker("Primary Language", selection: $primaryLanguage) {
                    Text("English").tag("en")
                    Text("German").tag("de")
                }
                
                Toggle("Auto-detect Language", isOn: $autoDetectLanguage)
                    .help("Automatically detect the language of the meeting")
            }
            
            Section("Permissions") {
                VStack(alignment: .leading, spacing: 8) {
                    HStack {
                        Image(systemName: "checkmark.circle.fill")
                            .foregroundColor(.green)
                        Text("Screen Recording")
                    }
                    
                    HStack {
                        Image(systemName: "checkmark.circle.fill")
                            .foregroundColor(.green)
                        Text("Microphone Access")
                    }
                    
                    Button("Open System Preferences") {
                        appState.permissionManager.openSystemPreferences()
                    }
                    .buttonStyle(.link)
                }
            }
        }
        .formStyle(.grouped)
        .padding()
    }
    
    // MARK: - Models Settings
    
    private var modelsSettingsView: some View {
        Form {
            Section("Transcription Model") {
                Picker("Whisper Model", selection: $selectedWhisperModel) {
                    Text("Base (Fast, Good Quality)").tag("whisper:base")
                    Text("Small (Balanced)").tag("whisper:small")
                    Text("Medium (Best Quality)").tag("whisper:medium")
                }
                
                Text("Larger models provide better accuracy but require more RAM and processing time.")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Section("Summarization Model") {
                Picker("LLM Model", selection: $selectedLLMModel) {
                    Text("Llama 3.2 (Recommended)").tag("llama3.2")
                    Text("Mistral 7B").tag("mistral")
                }
                
                Text("The language model used to generate meeting summaries.")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Section("Ollama Status") {
                HStack {
                    Image(systemName: "circle.fill")
                        .foregroundColor(.green)
                    Text("Connected to Ollama")
                }
                
                if !availableModels.isEmpty {
                    Text("\(availableModels.count) models available")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
                Button("Refresh Models") {
                    loadAvailableModels()
                }
            }
        }
        .formStyle(.grouped)
        .padding()
    }
    
    // MARK: - Privacy Settings
    
    private var privacySettingsView: some View {
        Form {
            Section("Data Storage") {
                VStack(alignment: .leading, spacing: 12) {
                    Text("All data is stored locally on your Mac")
                        .font(.headline)
                    
                    Text("• Audio recordings are saved in your Documents folder")
                    Text("• Transcripts and summaries are stored in a local database")
                    Text("• No data is ever sent to external servers")
                    
                    Divider()
                    
                    Button("Open Data Folder") {
                        openDataFolder()
                    }
                    
                    Button("Clear All Data", role: .destructive) {
                        // Implement data clearing
                    }
                }
            }
            
            Section("Privacy Features") {
                Toggle("Encrypt stored transcripts", isOn: .constant(false))
                    .disabled(true)
                    .help("Coming in future version")
                
                Toggle("Auto-delete recordings after 30 days", isOn: .constant(false))
                    .disabled(true)
                    .help("Coming in future version")
            }
        }
        .formStyle(.grouped)
        .padding()
    }
    
    // MARK: - Helpers
    
    private func loadAvailableModels() {
        Task {
            do {
                availableModels = try await appState.ollamaClient.getAvailableModels()
            } catch {
                print("Failed to load models: \(error)")
            }
        }
    }
    
    private func openDataFolder() {
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        NSWorkspace.shared.open(documentsPath)
    }
}
