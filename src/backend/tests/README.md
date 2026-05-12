# Backend Tests

This directory contains the test suite for the MeetingMinds backend.

## Running Tests

We use `uv` for Python package management and `pytest` for testing.

### From the Project Root
To run all backend tests from the repository root:

```bash
uv run pytest
```

### From the Backend Directory (`src/backend`)
If you are already inside `src/backend`:

```bash
uv run pytest tests
```

## Test Structure
- `test_api.py`: Tests for the FastAPI endpoints.
- `test_scribe.py`: Tests for the transcription service (Sona).
- `test_services.py`: General service logic tests.
