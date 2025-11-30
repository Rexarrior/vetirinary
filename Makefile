.PHONY: help build up down logs shell migrate makemigrations createsuperuser collectstatic test clean

# Colors for help
BLUE := \033[36m
NC := \033[0m

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-15s$(NC) %s\n", $$1, $$2}'

# Docker commands
build: ## Build Docker images
	docker compose build

up: ## Start all services
	docker compose up -d

down: ## Stop all services
	docker compose down

logs: ## View logs from all services
	docker compose logs -f

logs-web: ## View logs from web service
	docker compose logs -f web

shell: ## Open Django shell
	docker compose exec web python manage.py shell

bash: ## Open bash in web container
	docker compose exec web bash

# Django commands
migrate: ## Run Django migrations
	docker compose exec web python manage.py migrate

makemigrations: ## Create Django migrations
	docker compose exec web python manage.py makemigrations

createsuperuser: ## Create Django superuser
	docker compose exec web python manage.py createsuperuser

collectstatic: ## Collect static files
	docker compose exec web python manage.py collectstatic --noinput

# Development commands
dev: ## Start development server (without Docker)
	python manage.py runserver

test: ## Run tests
	docker compose exec web python manage.py test

# Maintenance
clean: ## Remove all containers, volumes, and images
	docker compose down -v --rmi all

restart: down up ## Restart all services

rebuild: down build up ## Rebuild and restart all services

# Database
db-shell: ## Open PostgreSQL shell
	docker compose exec db psql -U vetclinic_user -d vetclinic

db-backup: ## Backup database
	docker compose exec db pg_dump -U vetclinic_user vetclinic > backup_$$(date +%Y%m%d_%H%M%S).sql

# Status
status: ## Show status of services
	docker compose ps



