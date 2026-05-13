import uvicorn
import os
import sys
import multiprocessing

# This is needed for PyInstaller + multiprocessing on Windows/Mac
multiprocessing.freeze_support()

if __name__ == "__main__":
    # Get port from env or default to 8000
    port = int(os.getenv("PORT", 8000))
    host = "127.0.0.1"
    
    print(f"Starting MeetingMinds Backend on {host}:{port}")
    
    # Import the app here to avoid issues with early imports
    from main import app
    
    uvicorn.run(app, host=host, port=port, log_level="info")
