#!/usr/bin/env bash
set -euo pipefail

# Resolve repository root (script is located in scripts/)
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd -- "${SCRIPT_DIR}/.." && pwd)
ENV_FILE="${REPO_ROOT}/.env"

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "[publish] Missing .env file at ${ENV_FILE}." >&2
  echo "Copy .env.example to .env and provide the required variables." >&2
  exit 1
fi

# shellcheck source=/dev/null
set -a
source "${ENV_FILE}"
set +a

TWINE_USERNAME=${TWINE_USERNAME:-}
TWINE_PASSWORD=${TWINE_PASSWORD:-}
PYPI_REPOSITORY_URL=${PYPI_REPOSITORY_URL:-https://upload.pypi.org/legacy/}
PYPI_SKIP_UPLOAD=${PYPI_SKIP_UPLOAD:-false}

if [[ -z "${TWINE_USERNAME}" ]]; then
  echo "[publish] TWINE_USERNAME is not set in .env" >&2
  exit 1
fi

if [[ -z "${TWINE_PASSWORD}" ]]; then
  echo "[publish] TWINE_PASSWORD is not set in .env" >&2
  exit 1
fi

cd "${REPO_ROOT}"

echo "[publish] Upgrading pip and installing build dependencies"
python3 -m pip install --upgrade pip
python3 -m pip install build twine

if [[ "${INSTALL_PROJECT:-true}" == "true" ]]; then
  echo "[publish] Installing project in editable mode"
  python3 -m pip install -e .
fi

echo "[publish] Running static import check"
python3 -m compileall src

echo "[publish] Cleaning old build artifacts"
rm -rf dist build

mkdir -p dist

echo "[publish] Building source distribution and wheel"
python3 -m build

if [[ "${PYPI_SKIP_UPLOAD}" == "true" ]]; then
  echo "[publish] PYPI_SKIP_UPLOAD=true; skipping upload"
  exit 0
fi

echo "[publish] Uploading artifacts to ${PYPI_REPOSITORY_URL}"
twine upload --repository-url "${PYPI_REPOSITORY_URL}" dist/*

echo "[publish] Done"
