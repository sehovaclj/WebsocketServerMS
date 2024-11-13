# Use Python 3.12 slim image as the base
FROM python:3.12-slim

# Set environment variables for Python and timezone configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    TZ=America/Toronto \
    DEBIAN_FRONTEND=noninteractive

# Set the working directory
WORKDIR /app

# Copy Pipfile and Pipfile.lock first to leverage Docker cache
COPY Pipfile Pipfile.lock /app/

# Install dependencies, including Paho MQTT for Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tzdata && \
    pip install pipenv && \
    pipenv install --system --deploy && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code
COPY . /app

# Start the application
CMD ["python", "-m", "src.main"]
