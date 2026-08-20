# Nasazení

## Docker Compose

```bash
cp .env.example .env
docker compose up --build -d
./scripts/smoke-test.sh http://localhost:8080
```

Aplikace bude dostupná na `http://localhost:8080`.

## Kubernetes

1. Nahraďte ukázkové image názvy vlastními obrazy.
2. Změňte heslo v `deploy/base/kustomization.yaml` nebo vytvořte Secret jiným bezpečným způsobem.
3. Upravte hostname v `deploy/overlays/kubernetes/ingress.yaml`.
4. Nasaďte aplikaci:

```bash
kubectl apply -k deploy/overlays/kubernetes
kubectl -n task-app get pods,svc,ingress,pvc,hpa
```

Ingress předpokládá dostupný Ingress Controller. HPA předpokládá dostupné resource metrics, typicky Metrics Server.

## OKD

1. Upravte hostname nebo nechte OKD vygenerovat hostitele Route.
2. Nasaďte overlay:

```bash
kubectl apply -k deploy/overlays/okd
kubectl -n task-app get pods,svc,pvc,route
```

OKD overlay nahrazuje databázový obraz variantou připravenou pro prostředí OpenShift/OKD a používá Route namísto Ingressu.
