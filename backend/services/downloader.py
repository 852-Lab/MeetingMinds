import yt_dlp
import os

def download_youtube_audio(url: str, output_dir: str) -> str:
    """
    Downloads audio from a YouTube URL (video or live stream).
    Returns the path to the downloaded file.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    print(f"Starting download for URL: {url} to directory: {output_dir}")
    try:
        max_retries = 3
        retry_delay = 2
        last_error = None

        for attempt in range(max_retries):
            try:
                print(f"yt-dlp download attempt {attempt + 1}/{max_retries} for {url}...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    # yt-dlp with postprocessor changes extension, predicting it:
                    base, _ = os.path.splitext(filename)
                    final_path = f"{base}.mp3"
                    if os.path.exists(final_path):
                        return final_path
                    raise RuntimeError(f"Downloaded file not found at {final_path}")
            except Exception as e:
                last_error = e
                print(f"yt-dlp attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    import time
                    time.sleep(retry_delay)
        
        raise last_error
    except Exception as e:
        print(f"yt-dlp Final Error: {e}")
        raise e
