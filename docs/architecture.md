# Architektura

Aplikace má tři vrstvy:

1. **Frontend** – React aplikace sestavená pomocí Vite a servírovaná přes Nginx na portu 8080.
2. **Backend** – REST API ve FastAPI na portu 8000. Poskytuje CRUD operace, health endpointy a metriky.
3. **Databáze** – PostgreSQL s trvalým úložištěm.

Frontend předává požadavky na `/api`, `/health` a `/metrics` backendové službě. Backend jako jediná komponenta přistupuje k databázi. V Kubernetes a OKD je tento tok omezen pomocí NetworkPolicy.

```text
Uživatel -> Frontend/Nginx -> FastAPI -> PostgreSQL
                      |          |
                    /health    /metrics
```

Stejné aplikační obrazy se používají v Dockeru, Kubernetes i OKD. Platformní rozdíly jsou uloženy v `deploy/overlays`.
