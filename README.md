# Diploma Container Platforms

Startovní implementace praktické části diplomové práce zaměřené na Docker, Kubernetes, OKD a jednotnou CI/CD pipeline.

## Obsah

- React frontend
- FastAPI REST API
- PostgreSQL databáze
- backendové automatizované testy
- Dockerfile pro frontend a backend
- Docker Compose pro lokální a serverové nasazení
- Kustomize base a overlays pro Kubernetes a OKD
- readiness, liveness a startup probes
- resource requests/limits, rolling update a HPA
- perzistentní databázové úložiště
- NetworkPolicy
- GitHub Actions CI/CD
- smoke test a návrh testovacích scénářů

## Rychlé spuštění

Požadavky: Docker s pluginem Compose.

```bash
cp .env.example .env
docker compose up --build -d
./scripts/smoke-test.sh http://localhost:8080
```

Webové rozhraní: `http://localhost:8080`

API dokumentace: `http://localhost:8080/docs` není z frontendu proxyována; pro lokální vývoj spusťte backend samostatně nebo dočasně publikujte port 8000. Health endpoint je dostupný na `http://localhost:8080/health/ready` a metriky na `http://localhost:8080/metrics`.

## Lokální vývoj bez Dockeru

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt -r backend/requirements-dev.txt
cd backend
uvicorn app.main:app --reload
```

V druhém terminálu:

```bash
cd frontend
npm install --no-audit --no-fund
npm run dev
```

Bez proměnné `DATABASE_URL` backend používá lokální SQLite databázi. Docker a clusterová prostředí používají PostgreSQL.

## Testy a kontrola kvality

```bash
make install
make lint
make test
```

## Kubernetes a OKD

```bash
kubectl kustomize deploy/overlays/kubernetes
kubectl kustomize deploy/overlays/okd
```

Před nasazením změňte image názvy, hostnames a výchozí databázové heslo. Podrobnosti jsou v `docs/deployment.md` a `docs/ci-cd.md`.

## Struktura

```text
backend/                  FastAPI, SQLAlchemy, testy a Dockerfile
frontend/                 React, Vite, Nginx a Dockerfile
deploy/base/              společné Kubernetes objekty
deploy/overlays/kubernetes Ingress a HPA
deploy/overlays/okd/      Route a OKD úpravy
.github/workflows/        CI a nasazení
scripts/                  smoke test a aktualizace image v Kustomize
docs/                     architektura a postupy
tests/                    testovací scénáře pro praktické vyhodnocení
```

## Bezpečnostní poznámky

- Výchozí heslo `change-me` slouží pouze pro demonstraci a musí být změněno.
- Produkční secrets neukládejte do Git repozitáře.
- Aplikační kontejnery nepoužívají privilegovaný režim a zahazují Linux capabilities.
- Docker a GitHub Actions tagy `latest` v pomocných nástrojích nahraďte při finálním experimentu přesnými verzemi nebo digesty.
- Před měřením zaznamenejte verze Dockeru, Kubernetes, OKD, clusterových komponent a hostitelského systému.
