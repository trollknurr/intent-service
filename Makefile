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

#
# Docker
#

.PHONY: build
build:
	docker build -t intent-service:dev .

.PHONY: run
run:
	docker run -p 8000:8000 intent-service:dev
