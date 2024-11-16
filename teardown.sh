#!/bin/bash

# Constants
IMAGE_NAME="ws_server_ms_simulation_image"
CONTAINER_NAME="ws_server_ms_simulation_container_1"

# Function to print messages with UTC timestamp
log() {
    echo "$(date -u +'%Y-%m-%d %H:%M:%S.%3N') $1"
}

# Stop and remove the specific container
log "Stopping and removing container '${CONTAINER_NAME}'..."
if sudo docker ps -a --filter "name=${CONTAINER_NAME}" | grep -q "${CONTAINER_NAME}"; then
    if ! sudo docker stop "${CONTAINER_NAME}"; then
        log "Failed to stop container ${CONTAINER_NAME}. Exiting..."
        exit 1
    fi
    log "Container ${CONTAINER_NAME} stopped successfully."

    if ! sudo docker rm "${CONTAINER_NAME}"; then
        log "Failed to remove container ${CONTAINER_NAME}. Exiting..."
        exit 1
    fi
    log "Container ${CONTAINER_NAME} removed successfully."
else
    log "Container ${CONTAINER_NAME} not found. Continuing..."
fi

# Remove the specific image
log "Removing image '${IMAGE_NAME}' (if it exists)..."
if sudo docker images -q "${IMAGE_NAME}" > /dev/null; then
    if ! sudo docker rmi -f "${IMAGE_NAME}"; then
        log "Failed to remove image ${IMAGE_NAME}. Exiting..."
        exit 1
    fi
    log "Image ${IMAGE_NAME} removed successfully."
else
    log "Image ${IMAGE_NAME} not found. Continuing..."
fi

log "Container and image removal process completed successfully."
exit 0
