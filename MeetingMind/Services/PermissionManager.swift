import Foundation
import ScreenCaptureKit
import AVFoundation

class PermissionManager {
    
    // Check all required permissions
    func checkAllPermissions() async -> Bool {
        let screenPermission = await checkScreenRecordingPermission()
        let micPermission = await checkMicrophonePermission()
        return screenPermission && micPermission
    }
    
    // Check screen recording permission
    func checkScreenRecordingPermission() async -> Bool {
        // Check if we have screen recording permission
        let hasPermission = CGPreflightScreenCaptureAccess()
        
        if !hasPermission {
            // Request permission
            CGRequestScreenCaptureAccess()
        }
        
        return hasPermission
    }
    
    // Check microphone permission
    func checkMicrophonePermission() async -> Bool {
        let status = AVCaptureDevice.authorizationStatus(for: .audio)
        
        switch status {
        case .authorized:
            return true
        case .notDetermined:
            return await AVCaptureDevice.requestAccess(for: .audio)
        case .denied, .restricted:
            return false
        @unknown default:
            return false
        }
    }
    
    // Request all permissions
    func requestAllPermissions() async -> Bool {
        await checkAllPermissions()
    }
    
    // Open system preferences for permissions
    func openSystemPreferences() {
        if let url = URL(string: "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture") {
            NSWorkspace.shared.open(url)
        }
    }
}
