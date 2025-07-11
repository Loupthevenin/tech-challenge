include .env
export


DOCKER_COMPOSE = docker compose
DOCKER_COMPOSE_FILE = ./docker-compose.yml
DOCKER = $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE)

K8S_DIR = ./k8s

BACKEND_DIR=backend
FRONTEND_DIR=frontend

GREY	= \033[30m
RED		= \033[31m
GREEN	= \033[32m
YELLOW	= \033[33m
BLUE	= \033[34m
PURPLE	= \033[35m
CYAN	= \033[36m
WHITE	= \033[37m
END		= \033[0m

all: up

# DOCKER
build:
	@echo "$(BLUE)Building docker images...$(END)"
	@$(DOCKER) build

up: build
	@echo "$(BLUE)Starting Docker containers...$(END)"
	@$(DOCKER) up

down:
	@echo "$(RED)Stopping docker containers...$(END)"
	@$(DOCKER) down

logs:
	@echo "$(PURPLE)Showing docker logs...$(END)"
	@$(DOCKER) logs


# K8S

check-k8s:
	@kubectl cluster-info > /dev/null || (echo "🚫 Pas de cluster Kubernetes actif. Lance 'minikube start' d'abord." && exit 1)

k8s-apply: check-k8s
	@echo "$(BLUE)Applying all Kubernetes manifests...$(END)"
	kubectl apply -f $(K8S_DIR)/opensearch

	docker build \
		-f $(BACKEND_DIR)/Dockerfile.prod \
		--build-arg OPENSEARCH_HOST=opensearch \
		--build-arg OPENSEARCH_PORT=9200 \
		-t fastapi-backend:latest \
		$(BACKEND_DIR)
	minikube image load fastapi-backend:latest
	kubectl apply -f $(K8S_DIR)/backend

	docker build \
		-f $(FRONTEND_DIR)/Dockerfile.prod \
		--build-arg VITE_API_BASE_URL=$(VITE_API_BASE_URL) \
		--build-arg VITE_API_WS_URL=$(VITE_API_WS_URL) \
		-t frontend:latest \
		$(FRONTEND_DIR)
	minikube image load frontend:latest
	kubectl apply -f $(K8S_DIR)/frontend

k8s-delete:
	@echo "$(RED)Deleting all Kubernetes resources...$(END)"
	kubectl delete -f $(K8S_DIR)/frontend || true
	kubectl delete -f $(K8S_DIR)/backend || true
	kubectl delete -f $(K8S_DIR)/opensearch || true

k8s-logs:
	kubectl logs -l app=fastapi-backend

k8s-status:
	kubectl get all

clean:
	@echo "$(YELLOW)Stopping and removing Docker...$(END)"
	@$(DOCKER) down -v --remove-orphans --rmi all

	@echo "$(YELLOW)Removing Python virtual environment (.venv)...$(END)"
	@rm -rf $(BACKEND_DIR)/app/venv

	@echo "$(YELLOW)Removing Python cache (__pycache__)...$(END)"
	@find $(BACKEND_DIR)/app -type d -name "__pycache__" -exec rm -rf {} +

	@echo "$(GREEN)Cleanup complete!$(END)"

.PHONY: all up down logs k8s-apply k8s-delete k8s-logs k8s-status clean
