# Xcode Project Setup Instructions

Since Xcode project files (`.xcodeproj`) are binary and cannot be created via text files, you need to manually create the Xcode project. Follow these steps:

## Step 1: Create New Xcode Project

1. Open Xcode
2. Select **File → New → Project**
3. Choose **macOS** → **App**
4. Click **Next**

## Step 2: Configure Project Settings

- **Product Name:** MeetingMind
- **Team:** Select your development team
- **Organization Identifier:** com.yourcompany (or your preferred identifier)
- **Bundle Identifier:** Will auto-generate as com.yourcompany.MeetingMind
- **Interface:** SwiftUI
- **Language:** Swift
- **Include Tests:** Optional (recommended for future development)

Click **Next** and save the project in:
```
/Users/davnnis2003/AntigravityProjects/MeetingMind-POC
```

## Step 3: Remove Default Files

Xcode will create some default files. Delete these:
- `ContentView.swift` (we have our own views)
- The default `MeetingMindApp.swift` if it was created

## Step 4: Add Source Files to Project

1. In Xcode, right-click on the **MeetingMind** group in the navigator
2. Select **Add Files to "MeetingMind"...**
3. Navigate to `/Users/davnnis2003/AntigravityProjects/MeetingMind-POC/MeetingMind`
4. Select all folders (Models, Services, Views, Utilities, Resources)
5. **Important:** Check "Copy items if needed" and "Create groups"
6. Click **Add**

## Step 5: Configure Swift Package Dependencies

1. Select the project in the navigator (top-level MeetingMind)
2. Select the **MeetingMind** target
3. Go to **General** tab
4. Scroll to **Frameworks, Libraries, and Embedded Content**
5. Click the **+** button
6. Select **Add Package Dependency**

Add these packages:

### GRDB.swift
- URL: `https://github.com/groue/GRDB.swift`
- Version: 6.0.0 or later
- Add to target: MeetingMind

### swift-log
- URL: `https://github.com/apple/swift-log`
- Version: 1.5.0 or later
- Add to target: MeetingMind

## Step 6: Configure Info.plist

1. Select the **MeetingMind** target
2. Go to **Info** tab
3. Replace the default Info.plist with the one at:
   `MeetingMind/Resources/Info.plist`

Or manually add these keys:
- **NSMicrophoneUsageDescription**: "MeetingMind needs access to your microphone to record your voice during meetings."
- **NSScreenCaptureDescription**: "MeetingMind needs screen recording permission to capture system audio."
- **LSUIElement**: YES (makes it a menu bar app without dock icon)

## Step 7: Configure Signing & Capabilities

1. Select the **MeetingMind** target
2. Go to **Signing & Capabilities** tab
3. Enable **Automatically manage signing**
4. Select your **Team**

Add these capabilities:
- Click **+ Capability**
- Add **Hardened Runtime**
  - Enable: Audio Input
  - Enable: Screen Recording

## Step 8: Configure Build Settings

1. Select the **MeetingMind** target
2. Go to **Build Settings** tab
3. Search for "macOS Deployment Target"
4. Set to **13.0** or later

## Step 9: Build the Project

1. Select **Product → Build** (or press Cmd+B)
2. Fix any compilation errors if they appear
3. Most errors will be related to:
   - Missing imports (add `import UserNotifications` where needed)
   - GRDB not properly linked (re-add the package)

## Step 10: Run the App

1. Select **Product → Run** (or press Cmd+R)
2. The app should launch as a menu bar app
3. Look for the brain icon in your menu bar
4. Click it to see the MeetingMind interface

## Troubleshooting

### "Cannot find type 'UNMutableNotificationContent'"
Add `import UserNotifications` to `AppState.swift`

### "Cannot find 'GRDB' in scope"
1. Go to **File → Packages → Resolve Package Versions**
2. Clean build folder: **Product → Clean Build Folder**
3. Rebuild

### Permission prompts not appearing
1. Check Info.plist has the correct usage descriptions
2. Reset permissions: `tccutil reset All com.yourcompany.MeetingMind`
3. Restart the app

### App doesn't appear in menu bar
1. Check that `LSUIElement` is set to `YES` in Info.plist
2. Verify the app is using `MenuBarExtra` in the main app file

## Next Steps

After successful build:
1. Install Ollama: `brew install ollama`
2. Start Ollama: `ollama serve`
3. Download models:
   ```bash
   ollama pull whisper:base
   ollama pull llama3.2
   ```
4. Test the app by starting a recording

## Additional Notes

- The app requires macOS 13.0 or later
- Apple Silicon Macs (M1/M2/M3) are recommended for best performance
- The first run will request microphone and screen recording permissions
- All data is stored locally in `~/Library/Application Support/MeetingMind/`
