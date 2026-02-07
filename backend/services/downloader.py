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
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # yt-dlp with postprocessor changes extension, predicting it:
            base, _ = os.path.splitext(filename)
            final_path = f"{base}.mp3"
            return final_path
    except Exception as e:
        print(f"yt-dlp Error: {e}")
        raise e
