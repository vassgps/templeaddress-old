# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Copy the requirements file
COPY requirements.txt /code/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY . /code/

# Run migrations and collect static files
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Expose port 8000 for the application
EXPOSE 8000

# Start the application
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
