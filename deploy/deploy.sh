#!/bin/sh
set -e

APP_DIR="${APP_DIR:-/opt/blogweb}"
BRANCH="${BRANCH:-main}"
COMPOSE="docker compose --env-file .env.production"

cd "$APP_DIR"
git fetch origin "$BRANCH"
git checkout "$BRANCH"
git pull --ff-only origin "$BRANCH"

if [ ! -f .env.production ]; then
  echo ".env.production not found. Copy .env.production.example and fill production values first." >&2
  exit 1
fi

$COMPOSE build
$COMPOSE up -d --remove-orphans
$COMPOSE exec -T backend uv run python manage.py migrate --noinput
$COMPOSE exec -T backend uv run python manage.py collectstatic --noinput
$COMPOSE ps
