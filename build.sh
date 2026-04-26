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

# Seed sample data.
# Normal deploys: skips if data already exists (idempotent).
# To replace all data on next deploy: set RESEED=true in Render env vars,
# then clear it after the deploy completes.
if [ "${RESEED:-false}" = "true" ]; then
    echo "RESEED=true — wiping and replacing all sample data..."
    python manage.py seed --reset
else
    python manage.py seed
fi
