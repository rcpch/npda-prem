#!/bin/bash -e

# SessionStart hook for Claude Code on the web.
# Starts PostgreSQL 18 and installs Python dependencies so tests and linters
# are ready to use. Does NOT launch the Django dev server — run s/start-claude-web for that.

# Only run in remote (web) sessions.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
    exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

# ── PostgreSQL 18 ──────────────────────────────────────────────────────────────

if ! dpkg -s postgresql-18 &>/dev/null; then
    echo "==> Installing PostgreSQL 18..."
    apt-get install -y curl ca-certificates lsb-release
    install -d /usr/share/postgresql-common/pgdg
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc \
        -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc
    sh -c 'echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] \
https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" \
> /etc/apt/sources.list.d/pgdg.list'
    apt-get update -qq
    apt-get install -y postgresql-18
fi

if ! pg_lsclusters -h 2>/dev/null | grep -q "^18 main"; then
    echo "==> Initialising PostgreSQL 18 cluster..."
    pg_createcluster 18 main
fi

if ! pg_ctlcluster 18 main status &>/dev/null; then
    echo "==> Starting PostgreSQL 18..."
    pg_ctlcluster 18 main start
fi

# Read the actual port the cluster is listening on.
PG_PORT=$(pg_lsclusters -h | awk '/^18 main/ {print $3}')

# ── Environment file ───────────────────────────────────────────────────────────

if [ ! -f envs/.env ]; then
    echo "==> Creating envs/.env from template..."
    cp envs/.env.template envs/.env
    # Use localhost instead of the Docker service name.
    sed -i 's/POSTGRES_HOST="postgres"/POSTGRES_HOST="localhost"/' envs/.env
fi

# Ensure the port matches the running cluster (may differ from the template default).
sed -i "s/^POSTGRES_PORT=.*/POSTGRES_PORT=${PG_PORT}/" envs/.env

set -a
# shellcheck disable=SC1091
source envs/.env
set +a

# ── Database user & database ───────────────────────────────────────────────────

echo "==> Ensuring database user and database exist..."
su -c "psql -p ${PG_PORT} -c \"CREATE USER \\\"${POSTGRES_USER}\\\" WITH PASSWORD '${POSTGRES_PASSWORD}';\" 2>/dev/null || true" postgres
su -c "createdb -p ${PG_PORT} -O \"${POSTGRES_USER}\" \"${POSTGRES_DB}\" 2>/dev/null || true" postgres

# ── Python dependencies ────────────────────────────────────────────────────────

echo "==> Installing Python dependencies..."
uv sync

# Persist PYTHONPATH for linters and test runners.
echo 'export PYTHONPATH="."' >> "$CLAUDE_ENV_FILE"

echo "==> Session environment ready. Run s/start-claude-web to launch the dev server."
