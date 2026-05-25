#!/usr/bin/env bash
set -euo pipefail

# deploy.sh - simples deploy via rsync + ssh
# Usage: ./deploy/deploy.sh user@host /remote/path [branch]
# Example: ./deploy/deploy.sh ubuntu@1.2.3.4 /srv/bikebeach main
# Notes:
# - Requires `rsync` and `ssh` available locally and on remote.
# - Remote sudo is required to copy system files and restart services.
# - Adjust paths and service names in deploy/ files if necessary.

REMOTE=${1:-}
REMOTE_DIR=${2:-/srv/bikebeach}
BRANCH=${3:-main}

if [ -z "$REMOTE" ]; then
  echo "Usage: $0 user@host /remote/path [branch]"
  exit 1
fi

echo "Preparing local branch: $BRANCH"
git fetch origin
git checkout $BRANCH
git pull --ff-only origin $BRANCH

echo "Generating requirements.txt"
python -m pip freeze > requirements.txt

echo "Syncing files to $REMOTE:$REMOTE_DIR"
rsync -az --delete --exclude '.git' --exclude '.venv' --exclude '__pycache__' ./ "$REMOTE:$REMOTE_DIR/"

echo "Running remote setup on $REMOTE"
ssh "$REMOTE" bash -s <<'SSH'
set -euo pipefail
REMOTE_DIR="${REMOTE_DIR}"

# Ensure python3 and venv exist on remote
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found on remote. Install Python 3 and retry." >&2
  exit 2
fi

# Create virtualenv if missing
if [ ! -d "$REMOTE_DIR/.venv" ]; then
  python3 -m venv "$REMOTE_DIR/.venv"
fi

source "$REMOTE_DIR/.venv/bin/activate"
pip install -r "$REMOTE_DIR/requirements.txt" || true
pip install gunicorn || true

# Create /etc/default/bikebeach (requires sudo)
sudo bash -c "cat > /etc/default/bikebeach <<'ENV'
WORKDIR=$REMOTE_DIR
VENV_BIN=$REMOTE_DIR/.venv/bin
USER=www-data
GROUP=www-data
GUNICORN_BIND=127.0.0.1:8000
GUNICORN_WORKERS=3
ENV"

# Copy systemd service and nginx config into place
sudo cp "$REMOTE_DIR/deploy/bikebeach.service" /etc/systemd/system/bikebeach.service
sudo cp "$REMOTE_DIR/deploy/nginx_bikebeach.conf" /etc/nginx/sites-available/bikebeach
sudo ln -sf /etc/nginx/sites-available/bikebeach /etc/nginx/sites-enabled/bikebeach

# Migrate and collectstatic
source "$REMOTE_DIR/.venv/bin/activate"
python "$REMOTE_DIR/manage.py" migrate --noinput
python "$REMOTE_DIR/manage.py" collectstatic --noinput

# Start/Reload services
sudo systemctl daemon-reload
sudo systemctl enable --now bikebeach
sudo systemctl restart bikebeach || true
sudo nginx -t && sudo systemctl restart nginx || true

echo "Remote deploy finished."
SSH

echo "Deploy completed. Visit the site or check journalctl -u bikebeach for logs." 
