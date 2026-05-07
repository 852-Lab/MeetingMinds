import sys
import os

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), "src/backend"))

from services.scribe import transcriber

def test_transcription():
    audio_path = "tests/test.mp3"
    print(f"Testing transcription of {audio_path}...")
    try:
        result = transcriber.transcribe(audio_path, language="en")
        print("\nTranscription Result:")
        print(f"Text: {result.get('text', '')[:100]}...")
        print(f"Segments count: {len(result.get('segments', []))}")
        if result.get('segments'):
            first = result['segments'][0]
            print(f"First segment: [{first['start']} -> {first['end']}] {first['text']}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        transcriber.stop()

if __name__ == "__main__":
    test_transcription()
