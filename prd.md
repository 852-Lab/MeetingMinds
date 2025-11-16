# Product Requirements Document (PRD)
# MeetingMind - AI-Powered Local Meeting Assistant

**Version:** 1.0  
**Author:** Product Team  
**Last Updated:** November 16, 2025  
**Status:** Draft - POC Phase

---

## 1. Executive Summary

### 1.1 Product Vision
MeetingMind is a privacy-first, locally-hosted AI meeting assistant for macOS that records, transcribes, and intelligently summarizes meetings without sending data to external servers. By leveraging local AI models through Ollama, the product ensures complete data privacy while delivering enterprise-grade meeting intelligence.

### 1.2 Problem Statement
Professionals spend significant time in meetings but struggle to:
- Capture all important details while actively participating
- Generate actionable summaries and follow-up items
- Maintain data privacy when using cloud-based transcription services
- Support multiple languages (especially English and German) in multilingual environments

### 1.3 Solution Overview
A native macOS application that:
1. Records system audio and microphone input during meetings
2. Transcribes audio in real-time using local Whisper models via Ollama
3. Generates AI-powered executive summaries with timestamps, action items, and next steps
4. Operates completely offline with no data leaving the user's device

### 1.4 Success Metrics
- **Transcription Accuracy:** >90% for English, >85% for German
- **Processing Time:** Real-time transcription + summary generation within 60 seconds of meeting end
- **User Adoption:** 70% of beta testers use daily within first month
- **Privacy Compliance:** 100% local processing with no external API calls

---

## 2. Target Users & Use Cases

### 2.1 Primary Personas

**Persona 1: Enterprise Knowledge Worker**
- Role: Product Manager, Business Analyst, Consultant
- Needs: Capture meeting details, track action items, maintain confidentiality
- Pain: Too many meetings, difficult to focus while taking notes
- Tech Savvy: High (comfortable with local AI setup)

**Persona 2: Remote/Hybrid Professional**
- Role: Software Engineer, Designer, Marketing Manager
- Needs: Async meeting summaries for distributed teams, multilingual support
- Pain: Timezone differences, language barriers in global teams
- Tech Savvy: Medium to High

**Persona 3: Privacy-Conscious Professional**
- Role: Legal, Healthcare, Finance sector workers
- Needs: Compliance with data protection regulations (GDPR, HIPAA)
- Pain: Cannot use cloud transcription services due to compliance
- Tech Savvy: Medium

### 2.2 Key Use Cases

1. **Daily Standup Recording**
   - Record 15-min team standup
   - Generate bullet-point summary with action items per team member
   - Export to Slack/project management tool

2. **Client Meeting Documentation**
   - Capture 60-min client meeting
   - Identify key decisions, next steps, and deliverables
   - Share sanitized summary with stakeholders

3. **Multilingual Team Meetings**
   - Record meeting with English/German speakers
   - Transcribe with language detection
   - Generate summary in user's preferred language

4. **Personal Voice Notes**
   - Quick voice-to-text for ideas and reminders
   - Auto-categorize as action items or reference notes

---

## 3. Product Features & Requirements

### 3.1 Core Features (MVP - POC Phase)

#### Feature 1: System Audio Recording
**Priority:** P0 (Must Have)

**Description:**  
Record system audio from meeting applications (Zoom, Teams, Google Meet) and microphone input using macOS CoreAudio APIs.

**Functional Requirements:**
- FR-1.1: Capture system audio using ScreenCaptureKit API (macOS 14.2+)
- FR-1.2: Simultaneously capture microphone input via AVFoundation
- FR-1.3: Support recording start/stop via menu bar interface
- FR-1.4: Save raw audio files in M4A/WAV format
- FR-1.5: Display real-time recording indicator

**Technical Requirements:**
- TR-1.1: Request and verify "Screen & System Audio Recording" permissions
- TR-1.2: Handle audio device switching during recording
- TR-1.3: Maintain audio sync between system and mic channels
- TR-1.4: Support 44.1kHz/16-bit audio quality minimum

**Acceptance Criteria:**
- ✓ Audio recording starts within 2 seconds of user action
- ✓ No audio dropouts or glitches during 60-min recording
- ✓ Clear permission prompts with explanatory text
- ✓ Graceful handling of audio device disconnection

---

#### Feature 2: Local AI Transcription
**Priority:** P0 (Must Have)

**Description:**  
Convert recorded audio to text using Whisper models running locally via Ollama, with support for English, German, and auto-language detection.

**Functional Requirements:**
- FR-2.1: Transcribe audio files using Whisper models (base, small, medium, large)
- FR-2.2: Support English as primary language
- FR-2.3: Support German as secondary language
- FR-2.4: Auto-detect language when not specified
- FR-2.5: Generate word-level timestamps
- FR-2.6: Display transcription progress indicator

**Technical Requirements:**
- TR-2.1: Interface with Ollama API (localhost:11434)
- TR-2.2: Use Whisper base model as default (balance speed/accuracy)
- TR-2.3: Process audio in 30-second chunks for real-time feedback
- TR-2.4: Handle model loading and initialization
- TR-2.5: Implement retry logic for failed transcription segments

**Acceptance Criteria:**
- ✓ Transcription accuracy >90% for clear English speech
- ✓ Processing speed: 5x faster than real-time (10min audio → 2min processing)
- ✓ Correct language detection >95% of the time
- ✓ Word timestamps accurate within ±0.5 seconds

---

#### Feature 3: AI-Powered Summarization
**Priority:** P0 (Must Have)

**Description:**  
Generate executive summaries from transcripts using Ollama LLMs, extracting key points, action items, and next steps.

**Functional Requirements:**
- FR-3.1: Generate executive summary in bullet-point format
- FR-3.2: Extract meeting title (if mentioned) or suggest based on content
- FR-3.3: Include local timezone timestamps for key moments
- FR-3.4: Identify and list action items with assignees (if mentioned)
- FR-3.5: Highlight next steps and follow-up items
- FR-3.6: Support custom summary templates

**Technical Requirements:**
- TR-3.1: Use Llama 3.2/3.3 or Mistral models via Ollama
- TR-3.2: Implement prompt engineering for consistent output format
- TR-3.3: Process transcripts in chunks for long meetings (>60 min)
- TR-3.4: Generate summaries within 30-45 seconds
- TR-3.5: Format output as structured JSON/Markdown

**Summary Output Format:**
```markdown
# Meeting Summary

**Title:** [Auto-detected or "Meeting on YYYY-MM-DD"]
**Date:** YYYY-MM-DD
**Time:** HH:MM AM/PM [Timezone]
**Duration:** XX minutes

## Executive Summary
- Key point 1
- Key point 2
- Key point 3

## Key Decisions
- Decision 1 [Timestamp: HH:MM:SS]
- Decision 2 [Timestamp: HH:MM:SS]

## Action Items
- [ ] Task 1 - Assigned to: [Name] - Due: [Date if mentioned]
- [ ] Task 2 - Assigned to: [Name]

## Next Steps
- Follow-up item 1
- Follow-up item 2

## Full Transcript
[Timestamped transcript...]
```

**Acceptance Criteria:**
- ✓ Summary captures 90% of key points (validated by user feedback)
- ✓ Action items correctly identified (80% accuracy)
- ✓ Timestamps display in user's local timezone
- ✓ Summary length: 10-15 bullet points for 60-min meeting

---

### 3.2 Secondary Features (Post-POC)

#### Feature 4: Speaker Diarization
**Priority:** P1 (Should Have)
- Distinguish between different speakers
- Label speakers as "Speaker 1", "Speaker 2", etc.
- Allow manual speaker name assignment

#### Feature 5: Search & Archive
**Priority:** P1 (Should Have)
- Full-text search across all transcripts
- Tag meetings by project/topic
- Export summaries to PDF/Markdown

#### Feature 6: Integration Exports
**Priority:** P2 (Nice to Have)
- Export action items to Notion, Asana, Jira
- Calendar integration for meeting metadata
- Slack/Teams webhook for summary sharing

---

## 4. Technical Architecture

### 4.1 System Components

**Frontend (SwiftUI)**
- Menu bar app with system tray icon
- Recording controls (Start/Stop/Pause)
- Transcription viewer
- Summary display
- Settings panel

**Audio Capture Layer**
- ScreenCaptureKit for system audio (macOS 14.2+)
- AVFoundation for microphone
- Audio processing and encoding

**AI Processing Layer**
- Ollama client (HTTP API)
- Whisper model manager
- LLM summarization engine
- Prompt templates

**Data Storage Layer**
- Local SQLite database
- File storage for audio recordings
- Encrypted transcript storage (optional)

### 4.2 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Platform** | macOS 13.0+ (Ventura) |
| **Language** | Swift 5.9+ |
| **UI Framework** | SwiftUI |
| **Audio APIs** | ScreenCaptureKit, AVFoundation, CoreAudio |
| **AI Runtime** | Ollama (local server) |
| **Models** | Whisper (base/small/medium), Llama 3.2/3.3, Mistral |
| **Database** | SQLite (via Swift GRDB) |
| **Build System** | Xcode 15+ |

### 4.3 System Requirements

**Minimum:**
- macOS 13.0 (Ventura)
- Apple Silicon (M1/M2/M3) or Intel with 8GB RAM
- 10GB free disk space (for models)
- Ollama installed and running

**Recommended:**
- macOS 14.4+ (for best CoreAudio support)
- Apple Silicon M2 Pro or better
- 16GB+ RAM
- 20GB free disk space

---

## 5. User Experience & Design

### 5.1 User Flow

1. **First Launch**
   - App requests audio recording permissions
   - Setup wizard guides Ollama installation check
   - User selects preferred Whisper model
   - User sets default language preference

2. **Recording a Meeting**
   - User clicks menu bar icon → "Start Recording"
   - Real-time recording indicator shows duration
   - User clicks "Stop Recording" when meeting ends
   - App saves audio file and starts transcription

3. **Viewing Results**
   - Transcription progress bar shows processing status
   - Completed transcript appears in viewer
   - User clicks "Generate Summary" button
   - AI summary displays in <60 seconds
   - User can edit, copy, or export summary

### 5.2 Key UI Screens

**1. Menu Bar Interface**
- Start/Stop Recording button
- Current recording status
- Quick access to recent meetings
- Settings menu

**2. Meeting Viewer**
- List of past meetings (chronological)
- Search and filter options
- Meeting metadata (date, duration, title)

**3. Transcript View**
- Timestamped transcript with playback sync
- Highlight and annotation tools
- Speaker labels (future)

**4. Summary View**
- Executive summary card
- Action items checklist
- Export options
- Regenerate summary button

**5. Settings Panel**
- Model selection (Whisper size, LLM choice)
- Language preferences
- Audio device selection
- Storage management
- Privacy options

---

## 6. Privacy & Security

### 6.1 Privacy Requirements

**PR-1: Zero Cloud Dependency**
- All processing happens locally on user's Mac
- No data transmitted to external servers
- No internet connection required after model download

**PR-2: Data Encryption**
- Optional AES-256 encryption for stored transcripts
- Encrypted database for sensitive metadata
- Secure deletion of recordings

**PR-3: Permissions Transparency**
- Clear explanations for each macOS permission request
- Granular permissions (system audio vs. microphone)
- User control over data retention

### 6.2 Compliance Considerations

- **GDPR:** No personal data leaves device
- **HIPAA:** Local processing suitable for healthcare (with proper BAA)
- **SOC 2:** Security controls in place for enterprise users

---

## 7. Development Roadmap

### Phase 1: POC Development (Weeks 1-6)

**Week 1-2: Audio Recording**
- [ ] Implement ScreenCaptureKit audio capture
- [ ] Build AVFoundation microphone recording
- [ ] Create menu bar app skeleton
- [ ] Test audio quality and sync

**Week 3-4: Transcription Integration**
- [ ] Integrate Ollama API client
- [ ] Implement Whisper model loading
- [ ] Build transcription pipeline
- [ ] Add progress indicators

**Week 5-6: Summarization & UI**
- [ ] Implement LLM summarization
- [ ] Design and build summary viewer
- [ ] Add export functionality
- [ ] User testing and bug fixes

### Phase 2: Beta Release (Weeks 7-12)
- Speaker diarization
- Enhanced UI/UX
- Search and archive features
- Performance optimizations

### Phase 3: Public Launch (Weeks 13-16)
- Integration exports
- Advanced AI features
- Documentation and onboarding
- Marketing and distribution

---

## 8. Success Criteria & Metrics

### 8.1 POC Success Criteria

**Technical Milestones:**
- ✓ Audio recording works reliably for 2+ hour meetings
- ✓ Transcription accuracy >85% on test dataset
- ✓ Summary generation completes in <60 seconds
- ✓ App runs entirely offline (no internet dependency)

**User Acceptance:**
- 5 beta users test for 2 weeks
- >80% satisfaction score
- Users report time savings of 20+ minutes per meeting
- Zero critical bugs in core functionality

### 8.2 Key Performance Indicators (KPIs)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Transcription Accuracy | >90% | WER (Word Error Rate) |
| Processing Speed | <5x realtime | 10min audio → 2min |
| Summary Quality | >8/10 user rating | User feedback survey |
| App Stability | <2 crashes/month | Crash reports |
| Privacy Score | 100% local | Code audit |

---

## 9. Risks & Mitigations

### 9.1 Technical Risks

**Risk 1: Model Performance on Older Macs**
- *Impact:* Intel Macs may have slow transcription
- *Mitigation:* Support smaller Whisper models, optimize CPU usage, warn users

**Risk 2: Ollama Installation Complexity**
- *Impact:* Non-technical users struggle with setup
- *Mitigation:* In-app setup wizard, automated installation script, clear docs

**Risk 3: Audio Capture Permission Denials**
- *Impact:* Users cannot record meetings
- *Mitigation:* Clear permission prompts, fallback to mic-only mode, help docs

### 9.2 Business Risks

**Risk 4: Competition from Cloud Services**
- *Impact:* Users prefer convenience over privacy
- *Mitigation:* Emphasize privacy/compliance, target enterprise, integrate locally

**Risk 5: Limited Model Support**
- *Impact:* Languages beyond English/German lack quality models
- *Mitigation:* Partner with model providers, document limitations clearly

---

## 10. Open Questions

**Q1:** Should we support recording multiple audio sources simultaneously (e.g., Zoom + separate mic)?
**Q2:** How do we handle very long meetings (3+ hours) without exhausting memory?
**Q3:** Should summaries be editable/regeneratable with custom prompts?
**Q4:** Do we need a cloud backup option (encrypted) for users who want it?
**Q5:** What's the onboarding flow for users without Ollama pre-installed?

---

## 11. Appendices

### Appendix A: Glossary
- **Ollama:** Local AI model server for running LLMs
- **Whisper:** OpenAI's speech-to-text model
- **ScreenCaptureKit:** macOS API for screen/audio recording
- **LLM:** Large Language Model (e.g., Llama, Mistral)
- **CoreAudio:** Low-level audio API in macOS

### Appendix B: References
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Whisper Model Card](https://github.com/openai/whisper)
- [ScreenCaptureKit API](https://developer.apple.com/documentation/screencapturekit)
- [AVFoundation Guide](https://developer.apple.com/av-foundation/)

### Appendix C: Competitive Analysis

| Product | Cloud/Local | Pricing | Privacy | Pros | Cons |
|---------|-------------|---------|---------|------|------|
| Otter.ai | Cloud | $16.99/mo | Low | Great accuracy, integrations | Cloud-only, privacy concerns |
| Fireflies.ai | Cloud | $10/mo | Low | Good summaries, bots | Requires internet, data in cloud |
| MacWhisper | Local | $29 one-time | High | Local processing, fast | No summarization, basic UI |
| **MeetingMind** | **Local** | **TBD** | **High** | **Full AI, privacy-first** | **Requires Ollama setup** |

---

## Document Control

**Change Log:**
- v1.0 (2025-11-16): Initial draft for POC phase

**Approvals:**
- Product Manager: [TBD]
- Engineering Lead: [TBD]
- Design Lead: [TBD]

**Next Review Date:** 2025-12-01
