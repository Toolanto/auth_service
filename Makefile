install:
	@echo "Installing"
	poetry install || poetry update
	poetry run pre-commit install

test-unit:
	@echo "Test"
	poetry run pytest tests/ -m "not integration" -vv --cov=src

test:
	@echo "Test"
	poetry run pytest tests/ -vv --cov=src

dev:
	@echo "Dev"
	poetry run uvicorn main:app --reload

access-container:
	@echo "Auth postgres container"
	docker exec -it auth-postgres /bin/bash
