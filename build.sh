#!/usr/bin/env bash
# Render.com build script — runs once before the app starts on every deploy.
# Make executable: git update-index --chmod=+x build.sh
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# Create superuser (idempotent — skips if already exists)
python manage.py create_admin \
    --username  "${ADMIN_USERNAME:-admin}" \
    --email     "${ADMIN_EMAIL:-admin@example.com}" \
    --password  "${ADMIN_PASSWORD:-changeme123}"

# Load sample data so the site isn't empty on first visit (idempotent)
python manage.py seed
