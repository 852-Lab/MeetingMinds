import ffmpeg
import os

def extract_audio(input_path: str, output_path: str):
    """
    Extracts audio from video or converts audio to a standard format (mp3/wav).
    Uses ffmpeg-python wrapper.
    """
    try:
        (
            ffmpeg
            .input(input_path)
            .output(output_path, acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return output_path
    except ffmpeg.Error as e:
        print(f"FFmpeg Error: {e.stderr.decode('utf8')}")
        raise e
