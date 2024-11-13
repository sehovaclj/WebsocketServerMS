#!/bin/bash

# Constants
IMAGE_NAME="ws_server_ms_simulation_image"
CONTAINER_NAME="ws_server_ms_simulation_container_1"

# Function to print messages with UTC timestamp
log() {
    echo "$(date -u +'%Y-%m-%d %H:%M:%S.%3N') $1"
}

# Run pylint for linting checks
log "Running pylint..."
if ! pylint . ; then
    log "Pylint failed. Exiting..."
    exit 1
fi
log "Pylint completed successfully."

# Run unit tests
log "Running unit tests..."
if ! pytest -v ; then
    log "Unit tests failed. Exiting..."
    exit 1
fi
log "Unit tests completed successfully."

# Remove existing container if it exists
log "Removing existing container (if any)..."
if sudo docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    if ! sudo docker rm -f "$CONTAINER_NAME" ; then
        log "Failed to remove container $CONTAINER_NAME. Exiting..."
        exit 1
    fi
    log "Container $CONTAINER_NAME removed successfully."
else
    log "No existing container $CONTAINER_NAME found. Continuing..."
fi

# Remove the image if it exists
log "Removing existing image (if any)..."
if sudo docker images -q "${IMAGE_NAME}" ; then
    if ! sudo docker rmi -f "${IMAGE_NAME}" ; then
        log "Failed to remove image ${IMAGE_NAME}. Exiting..."
        exit 1
    fi
    log "Image ${IMAGE_NAME} removed successfully."
else
    log "No image ${IMAGE_NAME} found. Continuing..."
fi

# Build the Docker image with no cache
log "Building the Docker image with no cache..."
if ! sudo docker build --no-cache -t "${IMAGE_NAME}" . ; then
    log "Docker build failed. Exiting..."
    exit 1
fi
log "Docker image built successfully."

# Start the container
log "Starting container $CONTAINER_NAME..."
if ! sudo docker run -d --name "$CONTAINER_NAME" --network="host" "${IMAGE_NAME}" ; then
    log "Failed to start container $CONTAINER_NAME. Exiting..."
    exit 1
fi
log "Container $CONTAINER_NAME started successfully."

log "All steps completed successfully."
exit 0
