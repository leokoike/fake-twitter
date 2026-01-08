.PHONY: help install run migrate docker-build docker-up docker-down docker-logs docker-migrate clean

.DEFAULT_GOAL := help

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Local Development with UV
install: ## Install dependencies with uv
	uv sync

run: ## Run API locally with uvicorn
	uv run uvicorn fake_twitter.main:app --reload --host 0.0.0.0 --port 8000

run-prod: ## Run API with gunicorn
	uv run gunicorn fake_twitter.main:app -c gunicorn.conf.py

# Database Migrations
migrate: ## Run database migrations
	uv run alembic upgrade head

migrate-down: ## Rollback last migration
	uv run alembic downgrade -1

migrate-create: ## Create new migration (make migrate-create msg="description")
	uv run alembic revision -m "$(msg)"

migrate-status: ## Show current migration status
	uv run alembic current

# Docker Commands
docker-build: ## Build Docker image
	docker build -t fake-twitter:latest .

docker-up: ## Start containers with docker-compose
	docker-compose up -d

docker-down: ## Stop and remove containers
	docker-compose down -t 0

docker-logs: ## Show container logs
	docker-compose logs -f

docker-restart: ## Restart containers
	docker-compose restart

docker-rebuild: ## Rebuild and restart containers
	docker-compose up -d --build

docker-shell: ## Open shell in API container
	docker-compose exec api /bin/bash

docker-db-shell: ## Open PostgreSQL shell
	docker-compose exec db psql -U postgres -d fake_twitter

# Docker Database Migrations
docker-migrate: ## Run migrations in Docker
	docker-compose exec api uv run alembic upgrade head

docker-migrate-down: ## Rollback migration in Docker
	docker-compose exec api uv run alembic downgrade -1

# Setup Commands
setup: install migrate ## Setup local environment (install + migrate)
	@echo "✓ Setup complete! Run 'make run' to start"

docker-setup: docker-up docker-migrate ## Setup with Docker (up + migrate)
	@echo "✓ Docker setup complete! API running at http://localhost:8000"

# Cleanup
clean: ## Clean Python cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

docker-clean: ## Stop containers and remove volumes
	docker-compose down -v

clean-all: clean docker-clean ## Clean everything

validate: ## Run all validations (lint, type check, tests)
	uv run pre-commit run --all-files
