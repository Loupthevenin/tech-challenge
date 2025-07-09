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

npm install

npm run build

npm install -g serve

# TODO: utiliser var d'env
serve -s dist -l 3000
