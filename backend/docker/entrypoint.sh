#!/bin/sh
set -e

uv run python manage.py migrate --noinput
uv run python manage.py collectstatic --noinput

if [ "$DJANGO_CREATE_SUPERUSER" = "True" ]; then
  uv run python manage.py initadmin \
    --username "${DJANGO_SUPERUSER_USERNAME:-admin}" \
    --password "${DJANGO_SUPERUSER_PASSWORD:-admin123}" \
    --email "${DJANGO_SUPERUSER_EMAIL:-admin@blogweb.com}"
fi

exec "$@"
