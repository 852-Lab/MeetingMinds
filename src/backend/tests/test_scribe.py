import pytest
import requests
from unittest.mock import patch, MagicMock
from services.scribe import SonaTranscriber
import os

@pytest.fixture
def transcriber():
    return SonaTranscriber(base_url="http://mock-sona:8000/v1")

def test_sona_init():
    t = SonaTranscriber(base_url="http://test:8000/v1")
    assert t.base_url == "http://test:8000/v1"

@patch("services.scribe.requests.get")
def test_is_ready(mock_get, transcriber):
    mock_get.return_value.status_code = 200
    assert transcriber.is_ready() is True
    
    mock_get.side_effect = requests.exceptions.RequestException()
    assert transcriber.is_ready() is False

@patch("services.scribe.requests.post")
@patch("services.scribe.requests.get")
@patch("os.path.exists")
@patch("builtins.open", new_callable=MagicMock)
def test_transcribe_success(mock_open, mock_exists, mock_get, mock_post, transcriber):
    mock_exists.return_value = True
    mock_get.return_value.status_code = 200
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"text": "Hello world", "segments": []}
    
    result = transcriber.transcribe("dummy.wav")
    assert result["text"] == "Hello world"
    mock_post.assert_called()

@patch("services.scribe.requests.post")
@patch("services.scribe.requests.get")
@patch("os.path.exists")
@patch("builtins.open", new_callable=MagicMock)
def test_transcribe_connection_error(mock_open, mock_exists, mock_get, mock_post, transcriber):
    mock_exists.return_value = True
    mock_get.return_value.status_code = 200
    # Simulate the "Remote end closed connection" error
    mock_post.side_effect = requests.exceptions.ConnectionError("Connection aborted.")
    
    with pytest.raises(RuntimeError) as excinfo:
        transcriber.transcribe("dummy.wav")
    
    assert "Transcription server crashed" in str(excinfo.value)

@patch("services.scribe.requests.post")
@patch("services.scribe.requests.get")
@patch("os.path.exists")
@patch("builtins.open", new_callable=MagicMock)
def test_transcribe_timeout_error(mock_open, mock_exists, mock_get, mock_post, transcriber):
    mock_exists.return_value = True
    mock_get.return_value.status_code = 200
    mock_post.side_effect = requests.exceptions.Timeout("Timeout")
    
    with pytest.raises(RuntimeError) as excinfo:
        transcriber.transcribe("dummy.wav")
    
    assert "Transcription timed out" in str(excinfo.value)
