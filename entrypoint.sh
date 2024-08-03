#!/bin/bash

# entrypoint.sh

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Restore the database if it doesn't exist
if psql -U $DB_USER -d $DB_NAME -c '\dt' 2>/dev/null | grep -q 'No relations found.'; then
  echo "Restoring the database..."
  psql -U $DB_USER -d $DB_NAME < /docker-entrypoint-initdb.d/db_backup.sql
else
  echo "Database already exists, skipping restore"
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput


exec "$@"
