#!/bin/sh
set -e

echo "Waiting for postgres..."
while ! python -c "import psycopg2; psycopg2.connect(
    dbname='$POSTGRES_DB',
    user='$POSTGRES_USER',
    password='$POSTGRES_PASSWORD',
    host='$POSTGRES_HOST',
    port='$POSTGRES_PORT'
)" 2>/dev/null; do
    sleep 1
done
echo "PostgreSQL is ready."

python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py seed_data || true

exec python manage.py runserver 0.0.0.0:8000
