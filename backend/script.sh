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

if [ ! -d ".venv" ]; then
	info "Création d'un environnement virtuel..."
	python3 -m venv venv
	success "Environnement virtuel créé."
else
	info "Environnement virtuel déjà présent"
fi

info "Activation de l'environnement virtual"
source venv/bin/activate
success "Environnement virtuel activé."

info "Installation des dépendances..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
success "Dépendances installées."

info "Lancement de FastAPI..."
uvicorn main:app --host "${FASTAPI_HOST}" --port "${FASTAPI_PORT}"
