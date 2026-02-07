import requests
import sys
import os

def test_transcription(url, name):
    print(f"\n--- Testing {name} ---")
    payload = {"url": url}
    try:
        response = requests.post("http://localhost:8000/api/youtube-transcribe", json=payload)
        response.raise_for_status()
        data = response.json()
        print(f"Success! Method used: {data['method']}")
        print(f"File saved at: {data['file_path']}")
        print(f"First 100 chars: {data['text'][:100]}...")
    except Exception as e:
        print(f"Error testing {name}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")

if __name__ == "__main__":
    # Case 1: Video with captions (Easy case)
    # Using a known video with captions: "Never Gonna Give You Up" has captions
    test_transcription("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "Captioned Video")

    # Case 2: Video without captions (Hard case)
    # Using a video that likely has no captions (or I can mock it if I can't find one easily)
    # For now, let's try a recent music video or something similar where captions might be auto-generated but maybe disabled.
    # Actually, YouTube often has auto-generated captions.
    # To truly test the fallback, I might need to mock the API error in youtube.py if I can't find a video easily.
    # But let's try this one: 
    # test_transcription("https://www.youtube.com/watch?v=some_random_id", "Non-Captioned Video")
