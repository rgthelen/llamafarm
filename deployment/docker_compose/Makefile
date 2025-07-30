# LlamaFarm Docker Compose Commands

.PHONY: help build up down logs clean dev prod restart

help: ## Show this help message
	@echo "LlamaFarm Docker Compose Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build all services
	docker-compose build

up: ## Start all services in production mode
	docker-compose up -d --build

down: ## Stop all services
	docker-compose down

logs: ## Show logs for all services
	docker-compose logs -f

clean: ## Remove all containers, networks, and volumes
	docker-compose down -v --remove-orphans
	docker system prune -f

dev: ## Start development environment
	docker-compose -f docker-compose.dev.yml up --build

dev-down: ## Stop development environment
	docker-compose -f docker-compose.dev.yml down

prod: ## Start production environment
	docker-compose up -d --build

restart: ## Restart all services
	docker-compose restart

# Individual service commands
server: ## Start only the server
	docker-compose up server

designer: ## Start only the designer frontend
	docker-compose up designer

runtime: ## Start only the runtime service
	docker-compose up runtime

# Development individual services
dev-server: ## Start server in development mode
	docker-compose -f docker-compose.dev.yml up server

dev-designer: ## Start designer in development mode
	docker-compose -f docker-compose.dev.yml up designer

# Utility commands
shell-server: ## Open shell in server container
	docker-compose exec server bash

shell-designer: ## Open shell in designer container
	docker-compose exec designer sh

shell-runtime: ## Open shell in runtime container
	docker-compose exec runtime bash

health: ## Check health of all services
	docker-compose ps