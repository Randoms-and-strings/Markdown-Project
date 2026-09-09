#!/usr/bin/env bash
set -euo pipefail

# Wait until mongod is accepting connections
until mongosh --eval "db.adminCommand('ping')" >/dev/null 2>&1; do
  sleep 1
done

# Use runtime environment variables with sensible defaults
DB_NAME="${MONGO_INITDB_DATABASE:-mydatabase}"
CUSTOM_USERNAME="${CUSTOM_USERNAME:-randoms_and_strings}"
CUSTOM_PASSWORD="${CUSTOM_PASSWORD:-changeme}"

# Create the user in the target database
mongosh <<EOF
use ${DB_NAME}
db.createUser({
  user: "${CUSTOM_USERNAME}",
  pwd: "${CUSTOM_PASSWORD}",
  roles: [{ role: "dbOwner", db: "${DB_NAME}" }]
})
EOF
