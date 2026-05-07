import pytest
from unittest.mock import patch, MagicMock
from services.llm import LLMGenerator
from services.audio import extract_audio
import os

def test_llm_generator_init():
    generator = LLMGenerator(model="gemma3:4b")
    assert generator.model == "gemma3:4b"

@patch("services.llm.requests.post")
def test_llm_generate(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"response": "Success"}
    
    generator = LLMGenerator(model="gemma3:4b")
    result = generator.generate("Hello")
    assert result == "Success"

@patch("services.audio.ffmpeg")
def test_extract_audio_mock(mock_ffmpeg):
    # Mocking the entire chain
    mock_input = mock_ffmpeg.input.return_value
    mock_output = mock_input.output.return_value
    mock_overwrite = mock_output.overwrite_output.return_value
    
    extract_audio("input.mp4", "output.wav")
    
    mock_ffmpeg.input.assert_called_with("input.mp4")
    mock_input.output.assert_called_with("output.wav", acodec='pcm_s16le', ac=1, ar='16k')
    mock_output.overwrite_output.assert_called()
    mock_overwrite.run.assert_called_with(capture_stdout=True, capture_stderr=True)
