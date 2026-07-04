.PHONY: install dev build test docker-up docker-down clean

install:
	# Install backend dependencies
	cd backend && pip install -r requirements.txt

	# Install frontend dependencies
	cd frontend && npm install

dev:
	# Start development environment
	./scripts/dev.sh

build:
	# Build frontend for production
	cd frontend && npm run build

	# Build Docker images
	docker-compose build

test:
	# Run backend tests
	cd backend && pytest

	# Run frontend tests
	cd frontend && npm test

docker-up:
	# Start all services using Docker Compose
	docker-compose up -d

docker-down:
	# Stop all services using Docker Compose
	docker-compose down

clean:
	# Remove all Docker containers, images, and volumes
	docker-compose down --volumes --rmi all