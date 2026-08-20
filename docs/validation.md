# Ověření vytvořeného řešení

Při vytvoření repozitáře byly provedeny následující kontroly:

- 3 backendové testy přes FastAPI TestClient a SQLite – úspěšné,
- smoke test REST API proti lokálně spuštěnému Uvicornu – úspěšný,
- kompilace Python souborů – úspěšná,
- syntaktická kontrola JSX pomocí TypeScript parseru – úspěšná,
- parsování YAML souborů, kontrola odkazovaných Kustomize resources/patches a syntaxe shell skriptů – úspěšná.

V aktuálním prostředí nebyl dostupný Docker daemon, Kubernetes/OKD cluster ani síťové stažení npm balíčků. Proto zde nebylo možné provést skutečné sestavení kontejnerových obrazů, `npm run build`, `docker compose up` ani nasazení do clusteru. Tyto kroky jsou připravené v repozitáři a musí být ověřeny na cílové infrastruktuře.
