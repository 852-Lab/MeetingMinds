import SwiftUI

struct TranscriptView: View {
    let transcript: Transcript?
    
    var body: some View {
        ScrollView {
            if let transcript = transcript {
                VStack(alignment: .leading, spacing: 16) {
                    // Full text view
                    if !transcript.segments.isEmpty {
                        VStack(alignment: .leading, spacing: 12) {
                            ForEach(transcript.segments) { segment in
                                TranscriptSegmentView(segment: segment)
                            }
                        }
                    } else {
                        // Fallback to full text
                        Text(transcript.fullText)
                            .textSelection(.enabled)
                    }
                }
                .padding()
            } else {
                VStack(spacing: 16) {
                    Image(systemName: "doc.text")
                        .font(.system(size: 48))
                        .foregroundColor(.secondary)
                    
                    Text("No transcript available")
                        .font(.headline)
                        .foregroundColor(.secondary)
                    
                    Text("The transcript is still being processed or was not generated.")
                        .font(.caption)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .padding()
            }
        }
    }
}

// MARK: - Transcript Segment View

struct TranscriptSegmentView: View {
    let segment: TranscriptSegment
    
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            // Timestamp
            Text(segment.formattedTimestamp)
                .font(.system(.caption, design: .monospaced))
                .foregroundColor(.secondary)
                .frame(width: 60, alignment: .leading)
            
            // Text
            VStack(alignment: .leading, spacing: 4) {
                Text(segment.text)
                    .textSelection(.enabled)
                
                if let confidence = segment.confidence {
                    Text("Confidence: \(Int(confidence * 100))%")
                        .font(.caption2)
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding(.vertical, 4)
    }
}
