#!/bin/sh
set -eu

APP_DIR="${APP_DIR:-/opt/blogweb}"
BRANCH="${BRANCH:-main}"

if docker info >/dev/null 2>&1; then
  DOCKER="docker"
elif sudo -n docker info >/dev/null 2>&1; then
  DOCKER="sudo docker"
else
  echo "Cannot access Docker. Add the deploy user to the docker group, use root, or allow passwordless sudo for docker." >&2
  exit 1
fi

COMPOSE="$DOCKER compose --env-file .env.production"

print_failure_context() {
  status=$?
  echo "Deploy failed with status $status. Recent container logs:" >&2
  $COMPOSE ps >&2 || true
  $COMPOSE logs --tail=120 backend nginx >&2 || true
  exit "$status"
}

trap print_failure_context EXIT

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

HTTP_PORT="$(awk -F= '/^HTTP_PORT=/ { print $2 }' .env.production | tail -n 1)"
HTTP_PORT="${HTTP_PORT:-80}"
curl -fsS --retry 5 --retry-delay 3 --max-time 10 "http://127.0.0.1:${HTTP_PORT}/" >/dev/null

trap - EXIT
