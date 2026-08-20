SHELL := /bin/bash

.PHONY: help install test lint build up down logs smoke render-k8s render-okd

help:
	@echo "make install      Instalace lokálních závislostí"
	@echo "make test         Backend testy"
	@echo "make lint         Kontrola Python kódu"
	@echo "make build        Sestavení frontend a Docker obrazů"
	@echo "make up           Spuštění Docker Compose"
	@echo "make down         Zastavení Docker Compose"
	@echo "make smoke        Smoke test aplikace na localhost:8080"
	@echo "make render-k8s   Render Kubernetes manifestů"
	@echo "make render-okd   Render OKD manifestů"

install:
	python -m venv .venv
	.venv/bin/pip install -r backend/requirements.txt -r backend/requirements-dev.txt
	cd frontend && npm install --no-audit --no-fund

test:
	cd backend && ../.venv/bin/pytest -q

lint:
	.venv/bin/ruff check backend

build:
	cd frontend && npm install --no-audit --no-fund && npm run build
	docker compose build

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

smoke:
	./scripts/smoke-test.sh http://localhost:8080

render-k8s:
	kubectl kustomize deploy/overlays/kubernetes

render-okd:
	kubectl kustomize deploy/overlays/okd
