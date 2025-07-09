#!/bin/bash

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
END='\033[0m' # No Color

info() {
	echo -e "${BLUE}[INFO]${END} $1"
}

success() {
	echo -e "${GREEN}[SUCCESS]${END} $1"
}

error() {
	echo -e "${RED}[ERROR]${END} $1"
}

set -e

if [ ! -d "venv" ]; then
	info "Creating virtual environment..."
	python3 -m venv venv
	success "Virtual environment created."
else
	info "Virtual environment already exists."
fi

info "Activating virtual environment..."
source venv/bin/activate
success "Virtual environment activated."

info "Installing dependencies..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
success "Dependencies installed."

info "Starting FastAPI server..."
uvicorn main:app --host "${FASTAPI_HOST}" --port "${FASTAPI_PORT}"
