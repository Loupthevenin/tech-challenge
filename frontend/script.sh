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

info "Installing npm dependencies..."
npm install
success "Dependencies installed."

info "Building the frontend app..."
npm run build
success "Build completed."

info "Installing 'serve' globally..."
npm install -g serve
success "'serve' installed."

info "Starting the server on port 3000..."
serve -s dist -l 3000
