import Foundation
import SwiftUI

// MARK: - Date Extensions

extension Date {
    func formatted(style: DateFormatter.Style = .medium) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = style
        formatter.timeStyle = .none
        return formatter.string(from: self)
    }
    
    func formattedWithTime(dateStyle: DateFormatter.Style = .medium, timeStyle: DateFormatter.Style = .short) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = dateStyle
        formatter.timeStyle = timeStyle
        return formatter.string(from: self)
    }
}

// MARK: - TimeInterval Extensions

extension TimeInterval {
    func formattedDuration() -> String {
        let hours = Int(self) / 3600
        let minutes = (Int(self) % 3600) / 60
        let seconds = Int(self) % 60
        
        if hours > 0 {
            return String(format: "%d:%02d:%02d", hours, minutes, seconds)
        } else {
            return String(format: "%d:%02d", minutes, seconds)
        }
    }
}

// MARK: - String Extensions

extension String {
    func truncated(to length: Int, trailing: String = "...") -> String {
        if self.count > length {
            return String(self.prefix(length)) + trailing
        }
        return self
    }
}

// MARK: - Color Extensions

extension Color {
    static let meetingMindBlue = Color(red: 0.0, green: 0.48, blue: 1.0)
    static let meetingMindGreen = Color(red: 0.2, green: 0.78, blue: 0.35)
}

// MARK: - View Extensions

extension View {
    func cornerRadius(_ radius: CGFloat, corners: UIRectCorner) -> some View {
        clipShape(RoundedCorner(radius: radius, corners: corners))
    }
}

// Custom shape for specific corner radius
struct RoundedCorner: Shape {
    var radius: CGFloat = .infinity
    var corners: UIRectCorner = .allCorners
    
    func path(in rect: CGRect) -> Path {
        let path = UIBezierPath(
            roundedRect: rect,
            byRoundingCorners: corners,
            cornerRadii: CGSize(width: radius, height: radius)
        )
        return Path(path.cgPath)
    }
}

#if canImport(UIKit)
import UIKit
#else
// macOS fallback
struct UIRectCorner: OptionSet {
    let rawValue: Int
    
    static let topLeft = UIRectCorner(rawValue: 1 << 0)
    static let topRight = UIRectCorner(rawValue: 1 << 1)
    static let bottomLeft = UIRectCorner(rawValue: 1 << 2)
    static let bottomRight = UIRectCorner(rawValue: 1 << 3)
    static let allCorners: UIRectCorner = [.topLeft, .topRight, .bottomLeft, .bottomRight]
}

class UIBezierPath {
    let cgPath: CGPath
    
    init(roundedRect rect: CGRect, byRoundingCorners corners: UIRectCorner, cornerRadii: CGSize) {
        let path = CGMutablePath()
        
        let topLeft = rect.origin
        let topRight = CGPoint(x: rect.maxX, y: rect.minY)
        let bottomRight = CGPoint(x: rect.maxX, y: rect.maxY)
        let bottomLeft = CGPoint(x: rect.minX, y: rect.maxY)
        
        path.move(to: CGPoint(x: topLeft.x + cornerRadii.width, y: topLeft.y))
        
        path.addLine(to: CGPoint(x: topRight.x - cornerRadii.width, y: topRight.y))
        if corners.contains(.topRight) {
            path.addArc(tangent1End: topRight, tangent2End: CGPoint(x: topRight.x, y: topRight.y + cornerRadii.height), radius: cornerRadii.width)
        }
        
        path.addLine(to: CGPoint(x: bottomRight.x, y: bottomRight.y - cornerRadii.height))
        if corners.contains(.bottomRight) {
            path.addArc(tangent1End: bottomRight, tangent2End: CGPoint(x: bottomRight.x - cornerRadii.width, y: bottomRight.y), radius: cornerRadii.width)
        }
        
        path.addLine(to: CGPoint(x: bottomLeft.x + cornerRadii.width, y: bottomLeft.y))
        if corners.contains(.bottomLeft) {
            path.addArc(tangent1End: bottomLeft, tangent2End: CGPoint(x: bottomLeft.x, y: bottomLeft.y - cornerRadii.height), radius: cornerRadii.width)
        }
        
        path.addLine(to: CGPoint(x: topLeft.x, y: topLeft.y + cornerRadii.height))
        if corners.contains(.topLeft) {
            path.addArc(tangent1End: topLeft, tangent2End: CGPoint(x: topLeft.x + cornerRadii.width, y: topLeft.y), radius: cornerRadii.width)
        }
        
        path.closeSubpath()
        cgPath = path
    }
}
#endif
