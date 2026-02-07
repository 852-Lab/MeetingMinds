.PHONY: install dev backend frontend help

# Default target
all: help

help:
	@echo "Available commands:"
	@echo "  make install  - Install dependencies for backend and frontend"
	@echo "  make start    - Start both backend and frontend concurrently"
	@echo "  make backend  - Start only the backend server"
	@echo "  make frontend - Start only the frontend development server"

install:
	@echo "Installing backend dependencies..."
	cd backend && ./venv/bin/pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

backend:
	@echo "Starting backend..."
	cd backend && ./run_backend.sh

frontend:
	@echo "Starting frontend..."
	cd frontend && ./run_frontend.sh

start:
	@echo "Starting both backend and frontend..."
	@# Run both in parallel using & and wait for them
	cd backend && ./run_backend.sh & \
	cd frontend && ./run_frontend.sh & \
	wait
