from pathlib import Path
import re
import sys

if len(sys.argv) != 3:
    raise SystemExit("Usage: set-images.py <backend-image> <frontend-image>")

root = Path(__file__).resolve().parents[1]

updates = {
    root / "deploy/base/backend-deployment.yaml": (
        r"ghcr\.io/owner/repository-backend:[^\s]+",
        sys.argv[1],
    ),
    root / "deploy/base/frontend-deployment.yaml": (
        r"ghcr\.io/owner/repository-frontend:[^\s]+",
        sys.argv[2],
    ),
}

for path, (pattern, image) in updates.items():
    text = path.read_text(encoding="utf-8")

    updated, count = re.subn(pattern, image, text)

    if count == 0:
        raise SystemExit(f"Expected image reference not found in {path}")

    path.write_text(updated, encoding="utf-8")

    print(f"{path.name}: updated {count} image reference(s)")
