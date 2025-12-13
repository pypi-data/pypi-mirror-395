# RAFAEL Framework Makefile
# Convenient commands for development and deployment

.PHONY: help install test lint format clean build upload docs coverage security

help:
	@echo "RAFAEL Framework - Makefile Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install     - Install development dependencies"
	@echo "  make test        - Run all tests"
	@echo "  make test-unit   - Run unit tests only"
	@echo "  make test-integration - Run integration tests"
	@echo "  make coverage    - Generate coverage report"
	@echo "  make lint        - Run linters"
	@echo "  make format      - Format code"
	@echo "  make security    - Run security scans"
	@echo ""
	@echo "Build & Deploy:"
	@echo "  make build       - Build distribution packages"
	@echo "  make upload      - Upload to PyPI"
	@echo "  make docs        - Build documentation"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean       - Remove build artifacts"
	@echo "  make clean-all   - Remove all generated files"

install:
	pip install --upgrade pip
	pip install -e .[dev]
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --cov=core --cov=chaos_forge --cov=vault --cov=guardian --cov=devkit \
		--cov-report=html --cov-report=term-missing --asyncio-mode=auto

test-unit:
	pytest tests/ -v -m "not integration" --asyncio-mode=auto

test-integration:
	pytest tests/test_integration.py -v --asyncio-mode=auto

coverage:
	pytest tests/ --cov=core --cov=chaos_forge --cov=vault --cov=guardian --cov=devkit \
		--cov-report=html --cov-report=xml --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	@echo "Running flake8..."
	flake8 core chaos_forge vault guardian devkit --max-line-length=100
	@echo "Running mypy..."
	mypy core chaos_forge vault guardian devkit --ignore-missing-imports
	@echo "Running pylint..."
	pylint core chaos_forge vault guardian devkit --disable=C0111,R0903 || true
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
