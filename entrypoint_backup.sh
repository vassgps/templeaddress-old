#entrypoint.sh
#!/bin/bash
set -e

# Wait for the PostgreSQL server to be ready
until pg_isready -h db -p 5432 -U "$POSTGRES_USER"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

# Initialize database if empty
if [ $(psql -U $POSTGRES_USER -d $POSTGRES_DB -c '\dt' | grep -c "(0 rows)") -eq 1 ]; then
  psql -U $POSTGRES_USER -d $POSTGRES_DB < /code/db_backup.sql
fi

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the application
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
