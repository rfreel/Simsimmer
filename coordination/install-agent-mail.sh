#!/usr/bin/env bash
set -euo pipefail

VERSION="v0.3.29"
COMMIT="ae1183b2489aa03f8852cc4d50221d4940981778"
INSTALLER_URL="https://raw.githubusercontent.com/Dicklesworthstone/mcp_agent_mail_rust/${COMMIT}/install.sh"

printf 'Installing MCP Agent Mail %s from pinned commit %s\n' "$VERSION" "$COMMIT"

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT
curl -fsSL "$INSTALLER_URL" -o "$tmp"
bash "$tmp" --version "$VERSION" --verify --no-service --yes

if ! command -v am >/dev/null 2>&1; then
  printf 'Agent Mail install completed but am is not on PATH. Check ~/.local/bin.\n' >&2
  exit 1
fi

observed="$(am --version 2>&1 || true)"
printf 'Observed: %s\n' "$observed"
case "$observed" in
  *0.3.29*) ;;
  *)
    printf 'Version mismatch: expected Agent Mail 0.3.29\n' >&2
    exit 1
    ;;
esac

printf 'Pin verified. Start Agent Mail explicitly when coordination is needed.\n'
printf 'Then follow coordination/AGENT_MAIL.md; do not invent .agent-mail.yaml project_uid by hand.\n'
