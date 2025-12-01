#!/bin/bash
# Database restore script
# Usage: ./restore-db.sh backup_file.sql.gz

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <backup_file.sql.gz>"
    echo "Available backups:"
    ls -la /opt/vetclinic/backups/
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "⚠️  WARNING: This will replace all data in the database!"
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

cd /opt/vetclinic

echo "🛑 Stopping web container..."
docker-compose -f docker-compose.prod.yml stop web

echo "📦 Restoring database..."
gunzip -c ${BACKUP_FILE} | docker-compose -f docker-compose.prod.yml exec -T db psql -U ${DB_USER:-vetclinic_user} -d ${DB_NAME:-vetclinic}

echo "🚀 Starting web container..."
docker-compose -f docker-compose.prod.yml start web

echo "✅ Database restored successfully!"

