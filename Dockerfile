# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    netcat-openbsd

# Set the working directory
WORKDIR /code

# Copy the requirements file
COPY requirements.txt /code/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY . /code/

# Conditionally copy .env file if it exists
RUN if [ -f .env ] && [ ! -f /code/.env ]; then cp .env /code/.env; fi

# Copy the backup SQL file
# COPY db_backup.sql /docker-entrypoint-initdb.d/

# Check if db_backup.sql exists and copy it if it does
RUN mkdir -p /docker-entrypoint-initdb.d && \
    if [ -f db_backup.sql ]; then cp db_backup.sql /docker-entrypoint-initdb.d/; fi

# Copy the entrypoint script and ensure it's executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 8000 for the application
EXPOSE 8000

# Set the entrypoint and command
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
