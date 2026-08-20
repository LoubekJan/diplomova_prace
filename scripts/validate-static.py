from pathlib import Path
import json
import subprocess
import sys

import yaml

root = Path(__file__).resolve().parents[1]
errors: list[str] = []

for path in sorted(root.rglob("*.yaml")) + sorted(root.rglob("*.yml")):
    try:
        documents = list(yaml.safe_load_all(path.read_text(encoding="utf-8")))
    except Exception as exc:
        errors.append(f"{path.relative_to(root)}: neplatné YAML: {exc}")
        continue
    for index, document in enumerate(documents, start=1):
        if document is None:
            continue
        if not isinstance(document, dict):
            errors.append(f"{path.relative_to(root)}#{index}: dokument není mapa")

for kustomization in root.rglob("kustomization.yaml"):
    data = yaml.safe_load(kustomization.read_text(encoding="utf-8"))
    for key in ("resources",):
        for resource in data.get(key, []):
            candidate = (kustomization.parent / resource).resolve()
            if not candidate.exists():
                errors.append(f"{kustomization.relative_to(root)}: chybí resource {resource}")
    for patch in data.get("patches", []):
        if isinstance(patch, dict) and "path" in patch:
            candidate = (kustomization.parent / patch["path"]).resolve()
            if not candidate.exists():
                errors.append(f"{kustomization.relative_to(root)}: chybí patch {patch['path']}")

try:
    json.loads((root / "frontend/package.json").read_text(encoding="utf-8"))
except Exception as exc:
    errors.append(f"frontend/package.json: {exc}")

for script in root.glob("scripts/*.sh"):
    result = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True)
    if result.returncode:
        errors.append(f"{script.relative_to(root)}: {result.stderr.strip()}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print("Statická validace proběhla úspěšně.")
