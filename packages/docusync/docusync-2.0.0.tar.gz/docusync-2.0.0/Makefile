########################################################################
# Help
########################################################################
help:
	@echo "============================== Commands =============================="
	@echo "install                      - install dependencies"
	@echo "clean                        - clean virtual env and build artifacts"
	@echo "format                       - format code with black and isort"
	@echo "lint                         - lint code with flake8 and mypy"
	@echo "help                         - show this help message"
	@echo "======================================================================"


########################################################################
# Commands
########################################################################
install:
	@uv sync --all-groups --quiet

format: install
	@uv run black -l 79 .
	@uv run isort .

lint: install
	@uv run flake8 .
	@uv run mypy .

########################################################################
# Clean up build artifacts
########################################################################
ifeq ($(OS),Windows_NT)
clean:
	@echo Cleaning .mypy_cache directory...
	@if exist .mypy_cache (rmdir /S /Q .mypy_cache)
	@echo Cleaning .pytest_cache directory...
	@if exist .pytest_cache (rmdir /S /Q .pytest_cache)
	@echo Cleaning __pycache__ directories...
	@powershell -NoProfile -Command "Get-ChildItem -Recurse -Force -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force"
	@echo Cleaning .venv directory...
	@if exist .venv (rmdir /S /Q .venv)
else
clean:
	@echo "Cleaning .mypy_cache directory..."
	@rm -rf .mypy_cache
	@echo "Cleaning .pytest_cache directory..."
	@rm -rf .pytest_cache
	@echo "Cleaning __pycache__ directories..."
	@find . -type d -name __pycache__ | xargs rm -r
	@echo "Cleaning .venv directory..."
	@rm -rf .venv
endif