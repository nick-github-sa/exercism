#!/usr/bin/env bash
set -euo pipefail

# --- config you asked for ---
GITHUB_USERNAME="nick-github-sa"
ENV_FILE="../.env"        # contains GITHUB_TOKEN=...
# ----------------------------

# Load token from ../.env
if [[ ! -f "$ENV_FILE" ]]; then
  echo "Error: $ENV_FILE not found. Create it with: GITHUB_TOKEN=<your_token>" >&2
  exit 1
fi
# shellcheck disable=SC1090
source "$ENV_FILE"

: "${GITHUB_TOKEN:?Error: GITHUB_TOKEN not set in $ENV_FILE}"

# Ask for commit message
read -r -p "Commit message: " COMMIT_MSG
if [[ -z "${COMMIT_MSG// }" ]]; then
  echo "Aborted: empty commit message." >&2
  exit 1
fi

# Add and commit (allow no-op commit gracefully)
git add -A
if ! git commit -m "$COMMIT_MSG"; then
  echo "No changes to commit; continuing to push…" >&2
fi

# Ensure remote is HTTPS and embed username
ORIGIN_URL="$(git config --get remote.origin.url || true)"
if [[ -z "$ORIGIN_URL" ]]; then
  echo "Error: no 'origin' remote configured." >&2
  exit 1
fi

# Convert SSH -> HTTPS if needed
if [[ "$ORIGIN_URL" =~ ^git@github\.com: ]]; then
  REPO_PATH="${ORIGIN_URL#git@github.com:}"           # owner/repo.git
  ORIGIN_URL="https://github.com/${REPO_PATH}"
fi

# Add username if missing
if [[ "$ORIGIN_URL" =~ ^https://github\.com/ ]] && [[ ! "$ORIGIN_URL" =~ ^https://.+@github\.com/ ]]; then
  ORIGIN_URL="${ORIGIN_URL/https:\/\/github.com/https:\/\/${GITHUB_USERNAME}@github.com}"
fi

# Temporary askpass script that supplies the token as the "password"
ASKPASS_SCRIPT="$(mktemp)"
trap 'rm -f "$ASKPASS_SCRIPT"' EXIT
cat > "$ASKPASS_SCRIPT" <<'EOF'
#!/usr/bin/env bash
# Git will call this with a prompt; we always return the token.
echo "${GITHUB_TOKEN}"
EOF
chmod 700 "$ASKPASS_SCRIPT"

# Push using askpass (prevents token in process list/history)
GIT_ASKPASS="$ASKPASS_SCRIPT" \
GIT_ASKPASS_REQUIRE=force \
GITHUB_TOKEN="$GITHUB_TOKEN" \
git push "$ORIGIN_URL" HEAD

echo "✅ Pushed to origin."
