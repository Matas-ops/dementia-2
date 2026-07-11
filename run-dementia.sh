#!/bin/bash
set -euo pipefail

IMAGE_NAME="${IMAGE_NAME:-dementia:latest}"
CONTAINER_NAME="${CONTAINER_NAME:-dementia}"
DOCKERFILE="${DOCKERFILE:-Dockerfile.dev}"
CONTEXT="${CONTEXT:-.}"
PORT_MAPPING="${PORT_MAPPING:-8080:8080}"
ENV_FILE="${ENV_FILE:-.env}"
HOST_DATA_DIR="${HOST_DATA_DIR:-./data}"
CONTAINER_DATA_DIR="${CONTAINER_DATA_DIR:-/app/data}"

echo "Using Dockerfile: ${DOCKERFILE}"
echo "Build context: ${CONTEXT}"
echo "Image: ${IMAGE_NAME}"
echo "Container: ${CONTAINER_NAME}"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker CLI not found in PATH." >&2
  exit 2
fi

echo "Building image ${IMAGE_NAME} from ${DOCKERFILE}..."
docker build -t "${IMAGE_NAME}" -f "${DOCKERFILE}" "${CONTEXT}"

existing_id="$(docker ps -a --filter "name=^/${CONTAINER_NAME}$" --format '{{.ID}}')"
if [ -n "$existing_id" ]; then
  echo "Found existing container ${CONTAINER_NAME} — stopping and removing..."
  docker stop "${CONTAINER_NAME}" || true
  docker rm "${CONTAINER_NAME}" || true
fi

run_args=(
  --name "${CONTAINER_NAME}"
  --restart=always
  -d
  -p "${PORT_MAPPING}"
)

if [ -f "${ENV_FILE}" ]; then
  echo "Using env file: ${ENV_FILE}"
  run_args+=(--env-file "${ENV_FILE}")
fi

if [ -d "${HOST_DATA_DIR}" ]; then
  echo "Mapping host data directory: ${HOST_DATA_DIR} -> ${CONTAINER_DATA_DIR}"
  host_data_abs="$(cd "${HOST_DATA_DIR}" && pwd)"
  run_args+=(-v "${host_data_abs}:${CONTAINER_DATA_DIR}")
fi

echo "Running container ${CONTAINER_NAME}..."
docker run "${run_args[@]}" "${IMAGE_NAME}"

echo "Container started. Streaming logs (Ctrl+C to exit logs, container keeps running)..."
docker logs -f "${CONTAINER_NAME}"