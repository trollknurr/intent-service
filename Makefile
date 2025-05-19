dev:
	fastapi dev src/intent_service/__main__.py


#
# CI
#

.PHONY: format lint test
format:
	ruff format . src/ tests/

lint:
	ruff format --check src/ tests/
	ruff check --fix src/ tests/

test:
	pytest tests