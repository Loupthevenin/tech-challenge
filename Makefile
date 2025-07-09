DOCKER_COMPOSE = docker compose
DOCKER_COMPOSE_FILE = ./docker-compose.yml
DOCKER = $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE)

BACKEND_DIR=backend

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

clean:
	@echo "$(YELLOW)Stopping and removing Docker...$(END)"
	@$(DOCKER) down -v --remove-orphans --rmi all

	@echo "$(YELLOW)Removing Python virtual environment (.venv)...$(END)"
	@rm -rf $(BACKEND_DIR)/app/venv

	@echo "$(YELLOW)Removing Python cache (__pycache__)...$(END)"
	@find $(BACKEND_DIR)/app -type d -name "__pycache__" -exec rm -rf {} +

	@echo "$(GREEN)Cleanup complete!$(END)"

.PHONY: all up down logs clean
