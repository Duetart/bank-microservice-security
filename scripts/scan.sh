#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
OUT=${1:-"$ROOT/sast/generated"}
mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)
cd "$ROOT/microservice"
export SEMGREP_SEND_METRICS=off
semgrep --version | tee "$OUT/semgrep-version.txt"
semgrep scan --validate --config "$ROOT/sast/rules/semgrep-rules.yml"
semgrep scan --config "$ROOT/sast/rules/semgrep-rules.yml" --no-git-ignore --no-rewrite-rule-ids --metrics=off --json --output "$OUT/semgrep-results.json" app/*.py docker-compose.yml
if [[ ${ADD_MANUAL_IDOR:-0} == 1 ]]; then
  python3 "$ROOT/scripts/add_idor.py" "$OUT/semgrep-results.json" "$OUT/semgrep-results-with-idor.json"
fi
