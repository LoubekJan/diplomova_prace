# CI/CD pipeline

Repozitář obsahuje dvě GitHub Actions workflow:

- `ci.yml` provádí lint, automatizované testy, sestavení frontendu, sestavení obrazů a kontrolu kritických zranitelností pomocí Trivy.
- `deploy.yml` sestaví obrazy, uloží je do GHCR a umožní ruční nasazení do Dockeru, Kubernetes a OKD.

## Potřebné GitHub environments a secrets

### docker

Self-hosted runner s labely `self-hosted` a `docker` a secrets:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

### kubernetes

- volitelná repository variable `KUBECTL_VERSION` podle verze clusteru
- `KUBE_CONFIG_B64` – kubeconfig zakódovaný pomocí Base64.

### okd

- `OKD_KUBE_CONFIG_B64` – kubeconfig pro OKD zakódovaný pomocí Base64.

Pro produkční prostředí nastavte v GitHub Environment požadavek na ruční schválení. Akce jsou v ukázce odkazovány verzovacími tagy; před ostrým použitím je vhodné je připnout na konkrétní commit SHA.
