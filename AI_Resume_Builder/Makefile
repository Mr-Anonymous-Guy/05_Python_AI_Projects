# Makefile for AI Resume Builder
.PHONY: help install run test clean

help:
	@echo "AI Resume Builder - Makefile Commands"
	@echo "======================================"
	@echo "install    Install dependencies"
	@echo "run        Start Flask development server"
	@echo "test       Run test suite"
	@echo "clean      Remove generated files and cache"
	@echo "ollama     Check Ollama status"

install:
	pip install -r requirements.txt

run:
	python app.py

test:
	python -m pytest tests/ -v

clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache
	rm -rf generated/*
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

ollama:
	@echo "Checking Ollama installation..."
	@command -v ollama >/dev/null 2>&1 || { echo "Ollama not installed. Visit: https://ollama.ai"; exit 1; }
	@echo "Ollama is installed"
	@ollama list
