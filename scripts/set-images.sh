#!/usr/bin/env bash
set -euo pipefail

BACKEND_IMAGE="${1:?Použití: set-images.sh <backend-image> <frontend-image>}"
FRONTEND_IMAGE="${2:?Chybí frontend image}"

python scripts/set-images.py "$BACKEND_IMAGE" "$FRONTEND_IMAGE"
