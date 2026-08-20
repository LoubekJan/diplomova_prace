from pathlib import Path
import re
import sys

if len(sys.argv) != 3:
    raise SystemExit("Použití: set-images.py <backend-image> <frontend-image>")

root = Path(__file__).resolve().parents[1]
updates = {
    root / "deploy/base/backend-deployment.yaml": sys.argv[1],
    root / "deploy/base/frontend-deployment.yaml": sys.argv[2],
}

for path, image in updates.items():
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(
        r"(?m)^(\s*image:\s*)ghcr\.io/owner/repository-(?:backend|frontend):[^\s]+$",
        rf"\g<1>{image}",
        text,
        count=1,
    )
    if count != 1:
        raise SystemExit(f"V souboru {path} nebyl nalezen očekávaný image řádek.")
    path.write_text(updated, encoding="utf-8")
