import ffmpeg
import os
import logging

logger = logging.getLogger(__name__)

def extract_audio(input_path: str, output_path: str):
    """
    Extracts audio from video or converts audio to a standard format (mp3/wav).
    Uses ffmpeg-python wrapper.
    """
    logger.info(f"Extracting audio from {input_path} to {output_path}")
    try:
        (
            ffmpeg
            .input(input_path)
            .output(output_path, acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        logger.info(f"Successfully extracted audio to {output_path}")
        return output_path
    except ffmpeg.Error as e:
        stderr = e.stderr.decode('utf8') if e.stderr else "No stderr"
        stdout = e.stdout.decode('utf8') if e.stdout else "No stdout"
        logger.error(f"FFmpeg Error: {stderr}")
        logger.debug(f"FFmpeg stdout: {stdout}")
        raise e
