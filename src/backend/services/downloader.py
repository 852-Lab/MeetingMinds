import yt_dlp
import os

def download_youtube_audio(url: str, output_dir: str, progress_callback=None) -> str:
    """
    Downloads audio from a YouTube URL (video or live stream).
    Returns the path to the downloaded file.
    progress_callback: optional function to call with progress dict
    """
    def progress_hook(d):
        if progress_callback and d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%', '').strip()
            print(f"DEBUG: yt-dlp percent: {p}")
            try:
                progress_callback(float(p))
            except:
                pass

    ydl_opts = {
        'format': 'best/bestaudio',  # Use best available, android client is pickier
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
        'live_from_start': True,
        'noplaylist': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],
            }
        },
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
                        if os.path.getsize(final_path) < 1000:
                            raise RuntimeError(f"Downloaded file is too small ({os.path.getsize(final_path)} bytes)")
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
