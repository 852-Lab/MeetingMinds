# MeetingMind Setup Guide

## Complete Installation Instructions

### 1. System Requirements Check

Before starting, verify your system meets these requirements:

```bash
# Check macOS version
sw_vers

# Should show macOS 13.0 or higher
# Recommended: macOS 14.4+ for best CoreAudio support

# Check available RAM
sysctl hw.memsize | awk '{print $2/1073741824 " GB"}'

# Should show 8GB minimum, 16GB recommended

# Check free disk space
df -h /
```

### 2. Install Ollama

#### Option A: Using Homebrew (Recommended)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Ollama
brew install ollama

# Verify installation
ollama --version
```

#### Option B: Direct Download

1. Visit https://ollama.ai
2. Download the macOS installer
3. Open the .dmg file
4. Drag Ollama to Applications
5. Open Ollama from Applications

### 3. Download AI Models

Start Ollama server first:

```bash
# Open a terminal and run:
ollama serve

# Keep this terminal window open
# Or run in background: ollama serve &
```

In a new terminal, download models:

```bash
# For transcription - choose ONE based on your Mac:

# Option 1: Base model (fastest, good for most uses)
ollama pull whisper:base

# Option 2: Small model (balanced)
ollama pull whisper:small

# Option 3: Medium model (best accuracy, requires more RAM)
ollama pull whisper:medium

# For summarization - choose ONE:

# Option 1: Llama 3.2 3B (recommended)
ollama pull llama3.2

# Option 2: Mistral 7B (alternative)
ollama pull mistral

# Verify models are downloaded
ollama list
```

Expected output:
```
NAME              SIZE      MODIFIED
whisper:base      150MB     2 minutes ago
llama3.2          2.0GB     3 minutes ago
```

### 4. Install MeetingMind

#### Download Release

1. Go to [Releases Page](https://github.com/your-org/meetingmind/releases)
2. Download `MeetingMind-v1.0.dmg`
3. Open the downloaded .dmg file
4. Drag MeetingMind to Applications folder
5. Eject the disk image

#### First Launch

```bash
# Open from Applications
open /Applications/MeetingMind.app

# Or use Spotlight: Cmd+Space, type "MeetingMind"
```

**First Launch Security:**

If you see "MeetingMind cannot be opened":
1. Go to System Settings → Privacy & Security
2. Scroll to "Security" section
3. Click "Open Anyway" next to MeetingMind
4. Click "Open" in confirmation dialog

### 5. Grant Permissions

MeetingMind requires two permissions:

#### A. Screen & System Audio Recording

**When prompted:**
1. Click "Open System Settings"
2. Enable "MeetingMind" under Screen & System Audio Recording
3. Restart MeetingMind

**Manual setup:**
```
System Settings → Privacy & Security → Screen & System Audio Recording
→ Enable MeetingMind
```

#### B. Microphone Access

**When prompted:**
1. Click "OK" to allow microphone access
2. Grant permission in dialog

**Manual setup:**
```
System Settings → Privacy & Security → Microphone
→ Enable MeetingMind
```

### 6. Configure MeetingMind

#### First-Time Setup Wizard

On first launch, you'll see the setup wizard:

1. **Welcome Screen**
   - Read privacy statement
   - Click "Continue"

2. **Check Ollama Connection**
   - Wizard verifies Ollama is running
   - If not detected: Start Ollama and click "Retry"

3. **Select Models**
   - Choose Whisper model (detected automatically)
   - Choose LLM model (detected automatically)
   - Click "Continue"

4. **Language Preferences**
   - Primary: English (default)
   - Secondary: German (optional)
   - Enable auto-detect if needed
   - Click "Continue"

5. **Ready to Use**
   - Click "Start Using MeetingMind"

### 7. Test Your Setup

#### Quick Test Recording

1. **Prepare a Test Meeting**
   - Open YouTube and find a short video (2-3 minutes)
   - Or join a test Zoom call

2. **Start Recording**
   - Click MeetingMind menu bar icon
   - Click "Start Recording"
   - Verify red recording indicator appears

3. **Play Test Audio**
   - Play the YouTube video or speak into mic
   - Let it run for 1-2 minutes

4. **Stop and Process**
   - Click "Stop Recording"
   - Wait for processing (should take 20-30 seconds)

5. **View Results**
   - Check transcript accuracy
   - Review generated summary
   - Verify timestamps are correct

Expected result:
```
✅ Transcript shows correct words
✅ Summary has key points
✅ Timestamps match audio
✅ Action items identified (if any)
```

### 8. Troubleshooting

#### Problem: Ollama not detected

**Solution:**
```bash
# Check if Ollama is running
ps aux | grep ollama

# If not running, start it:
ollama serve

# Check connection
curl http://localhost:11434/api/tags
```

#### Problem: Models not found

**Solution:**
```bash
# List installed models
ollama list

# If empty, download again:
ollama pull whisper:base
ollama pull llama3.2
```

#### Problem: Permissions denied

**Solution:**
1. Go to System Settings → Privacy & Security
2. Check both "Screen Recording" and "Microphone" sections
3. Enable MeetingMind in both
4. Restart MeetingMind

#### Problem: No audio captured

**Solution:**
```bash
# Verify audio devices
system_profiler SPAudioDataType

# Check if system audio is working
# Play a video and check volume

# Restart MeetingMind and try again
```

#### Problem: Transcription very slow

**Solution:**
- Check RAM usage (Activity Monitor)
- Close other memory-intensive apps
- Use smaller Whisper model (base instead of medium)
- Upgrade to Apple Silicon Mac if on Intel

### 9. Advanced Configuration

#### Custom Model Paths

If you want to use custom model paths:

```bash
# Edit MeetingMind settings
# Settings → Advanced → Model Paths

# Or edit config file directly:
nano ~/Library/Application Support/MeetingMind/config.json
```

#### Performance Tuning

For best performance on M-series Macs:

```json
{
  "whisper_model": "whisper:small",
  "llm_model": "llama3.2",
  "audio_quality": "high",
  "processing_threads": 4,
  "enable_gpu": true
}
```

For Intel Macs:

```json
{
  "whisper_model": "whisper:base",
  "llm_model": "llama3.2",
  "audio_quality": "medium",
  "processing_threads": 2,
  "enable_gpu": false
}
```

### 10. Uninstallation

If you need to remove MeetingMind:

```bash
# Stop Ollama (if you don't use it elsewhere)
pkill ollama

# Remove MeetingMind app
rm -rf /Applications/MeetingMind.app

# Remove user data (optional - this deletes all meetings)
rm -rf ~/Library/Application Support/MeetingMind

# Remove Ollama (if not needed)
brew uninstall ollama

# Or manually:
rm -rf /Applications/Ollama.app
rm -rf ~/.ollama
```

### 11. Getting Help

If you encounter issues:

1. **Check logs:**
   ```bash
   # View MeetingMind logs
   log show --predicate 'subsystem == "com.meetingmind"' --last 1h
   ```

2. **Report issues:**
   - GitHub: https://github.com/your-org/meetingmind/issues
   - Include log excerpts and system info

3. **Community support:**
   - Discussions: https://github.com/your-org/meetingmind/discussions

---

## Quick Reference

### Essential Commands

```bash
# Start Ollama
ollama serve

# List models
ollama list

# Pull a model
ollama pull <model-name>

# Check Ollama status
curl http://localhost:11434/api/tags

# Open MeetingMind
open /Applications/MeetingMind.app
```

### Default Keyboard Shortcuts

- **Start/Stop Recording:** `Cmd+Shift+R`
- **Open Meetings:** `Cmd+1`
- **Search:** `Cmd+F`
- **Settings:** `Cmd+,`

---

**Setup Complete! 🎉**

You're ready to record and summarize meetings with complete privacy.
