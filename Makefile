install:
	@echo "Installing"
	poetry install || poetry update

test-unit:
	@echo "Test"
	poetry run pytest tests/ -m "not integration" -vv --cov=src

test:
	@echo "Test"
	poetry run pytest tests/ -vv --cov=src

dev:
	@echo "Dev"
	poetry run uvicorn main:web --reload