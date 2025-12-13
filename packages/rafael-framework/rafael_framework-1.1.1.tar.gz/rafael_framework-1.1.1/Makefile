# RAFAEL Framework Makefile
# Convenient commands for development and deployment

.PHONY: help install test lint format clean build deploy docker

help:
	@echo "🔱 RAFAEL Framework - Available Commands"
	@echo "========================================"
	@echo ""
	@echo "Development:"
	@echo "  make install     - Install dependencies"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linters"
	@echo "  make format      - Format code"
	@echo "  make clean       - Clean build artifacts"
	@echo ""
	@echo "Deployment:"
	@echo "  make build       - Build package"
	@echo "  make deploy      - Deploy to PyPI"
	@echo "  make docker      - Build Docker image"
	@echo "  make docker-push - Push Docker image"
	@echo ""
	@echo "Examples:"
	@echo "  make run-fintech - Run fintech example"
	@echo "  make run-game    - Run game example"
	@echo ""

install:
	@echo "📦 Installing dependencies..."
	pip install -e ".[dev]"
	@echo "✅ Installation complete"

test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v --cov=core --cov=chaos_forge --cov=vault --cov=guardian
	@echo "✅ Tests complete"

lint:
	@echo "🔍 Running linters..."
	flake8 core/ chaos_forge/ vault/ guardian/ devkit/ --max-line-length=100
	mypy core/ --ignore-missing-imports || true
	@echo "✅ Linting complete"

format:
	@echo "✨ Formatting code..."
	black core/ chaos_forge/ vault/ guardian/ devkit/ examples/ tests/
	@echo "✅ Formatting complete"

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "✅ Cleanup complete"

build: clean
	@echo "🔨 Building package..."
	python -m build
	twine check dist/*
	@echo "✅ Build complete"

deploy: build test
	@echo "🚀 Deploying to PyPI..."
	twine upload dist/*
	@echo "✅ Deployment complete"

docker:
	@echo "🐳 Building Docker image..."
	docker build -t rafaelframework/rafael:latest .
	@echo "✅ Docker image built"

docker-push: docker
	@echo "📤 Pushing Docker image..."
	docker push rafaelframework/rafael:latest
	@echo "✅ Docker image pushed"

run-fintech:
	@echo "💳 Running fintech example..."
	python examples/fintech_example.py

run-game:
	@echo "🎮 Running game example..."
	python examples/game_example.py

# Quick commands
all: clean install test lint build

dev: install format test

release: test lint build deploy

.DEFAULT_GOAL := help
