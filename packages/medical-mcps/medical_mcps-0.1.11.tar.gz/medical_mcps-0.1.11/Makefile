.PHONY: server server-no-reload help test-watch test docker install build publish deploy-cloud-run get-service-url

# Cloud Run deployment configuration
SERVICE_NAME ?= medical-mcps
REGION ?= us-central1
DOCKERHUB_USERNAME ?= pascalwhoop
IMAGE_TAG ?= latest
IMAGE ?= docker.io/$(DOCKERHUB_USERNAME)/medical-mcps:$(IMAGE_TAG)
PORT ?= 8080
MEMORY ?= 512Mi
TIMEOUT ?= 3600
MAX_INSTANCES ?= 100
MIN_INSTANCES ?= 0
SENTRY_DSN ?=
ENVIRONMENT ?= production

install:
	uv sync

# Start the MCP server with uvicorn and livereload
server:
	uv run uvicorn medical_mcps.http_server:app --reload --host 0.0.0.0 --port 8000

# Start the MCP server without auto-reload
server-no-reload:
	uv run uvicorn medical_mcps.http_server:app --host 0.0.0.0 --port 8000

# Run pytest-watch to automatically run tests on file changes
test-watch:
	uv run ptw --runner "uv run pytest"

# Run all tests (excluding slow Pathway Commons tests)
test: install
	uv run pytest tests/ --ignore=tests/test_pathwaycommons_tools.tavern.yaml

# Run slow tests (Pathway Commons) with extended timeout
test-slow: install
	uv run pytest tests/test_pathwaycommons_tools.tavern.yaml --timeout=200

# Run all tests including slow ones
test-all: install
	uv run pytest tests/ --timeout=200

# Build the package
build:
	uv lock
	uv build

# Publish to PyPI (builds first)
publish: build
	uv publish

inspector:
	npx @modelcontextprotocol/inspector@latest

# Docker Compose - start services with watch and build
docker:
	docker-compose watch

# Deploy to Cloud Run
# Usage: make deploy-cloud-run IMAGE_TAG=v0.1.9 DOCKERHUB_USERNAME=yourusername SENTRY_DSN=your-dsn
deploy-cloud-run:
	@if [ -z "$(DOCKERHUB_USERNAME)" ]; then \
		echo "Error: DOCKERHUB_USERNAME must be set"; \
		exit 1; \
	fi
	@echo "Deploying $(IMAGE) to Cloud Run..."
	@ENV_VARS="ENVIRONMENT=$(ENVIRONMENT)"; \
	if [ -n "$(SENTRY_DSN)" ]; then \
		ENV_VARS="$$ENV_VARS,SENTRY_DSN=$(SENTRY_DSN)"; \
	fi; \
	gcloud run deploy $(SERVICE_NAME) \
		--region $(REGION) \
		--image $(IMAGE) \
		--allow-unauthenticated \
		--memory $(MEMORY) \
		--timeout $(TIMEOUT) \
		--port $(PORT) \
		--max-instances $(MAX_INSTANCES) \
		--min-instances $(MIN_INSTANCES) \
		--set-env-vars "$$ENV_VARS" \
		--startup-probe-path /health \
		--liveness-probe-path /health
	@echo "Deployment complete!"

# Get the deployed service URL
get-service-url:
	@gcloud run services describe $(SERVICE_NAME) --region $(REGION) --format='value(status.url)'