#!/bin/sh

echo "**** File name: Entrypoint.sh Shell Scripts started ... !!"
echo "BACKUP_DB: $BACKUP_DB"
echo "RESTORE_DB: $RESTORE_DB"

echo "Waiting for PostgreSQL..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

# Restore the database if RESTORE_DB is set to "True"
if [ "$RESTORE_DB" = "True" ]; then
  echo "Checking for SQL dump file..."
  if [ -f /docker-entrypoint-initdb.d/db_backup.sql ]; then
    echo "SQL dump file found. Restoring database..."
    # Drop the existing database and create a new one
    PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -h $DB_HOST -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
    PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -h $DB_HOST -d postgres -c "CREATE DATABASE $DB_NAME;"

    # Restore the database from the dump file
    # PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -h $DB_HOST -d $DB_NAME < /docker-entrypoint-initdb.d/db_backup.sql
    PGPASSWORD=$DB_PASSWORD pg_restore -U $DB_USER -h $DB_HOST -d $DB_NAME /docker-entrypoint-initdb.d/db_backup.sql
    echo "Database restoration Successful ..!"
  else
    echo "SQL dump file not found. Skipping database restoration."
  fi
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

if [ "$BACKUP_DB" = "True" ] ; then
    echo "Backing up database..."
    python manage.py backup_db
fi

exec "$@"
