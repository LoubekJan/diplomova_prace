#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://localhost:8080}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-120}"

printf 'Čekám na %s/health/ready\n' "$BASE_URL"
for ((i=1; i<=TIMEOUT_SECONDS; i++)); do
  if curl --fail --silent "$BASE_URL/health/ready" >/dev/null; then
    break
  fi
  if [[ "$i" -eq "$TIMEOUT_SECONDS" ]]; then
    echo "Aplikace není dostupná." >&2
    exit 1
  fi
  sleep 1
done

TITLE="smoke-test-$(date +%s)"
CREATED="$(curl --fail --silent \
  -H 'Content-Type: application/json' \
  -d "{\"title\":\"$TITLE\"}" \
  "$BASE_URL/api/tasks")"

TASK_ID="$(python -c 'import json,sys; print(json.load(sys.stdin)["id"])' <<<"$CREATED")"
curl --fail --silent "$BASE_URL/api/tasks" | grep -q "$TITLE"
curl --fail --silent -X PATCH \
  -H 'Content-Type: application/json' \
  -d '{"completed":true}' \
  "$BASE_URL/api/tasks/$TASK_ID" >/dev/null
curl --fail --silent -X DELETE "$BASE_URL/api/tasks/$TASK_ID" >/dev/null

echo "Smoke test proběhl úspěšně."
