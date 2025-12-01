#!/bin/bash
# Database backup script
# Add to crontab: 0 3 * * * /opt/vetclinic/scripts/backup-db.sh

set -e

BACKUP_DIR="/opt/vetclinic/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="vetclinic_backup_${DATE}.sql"
KEEP_DAYS=7

# Create backup directory
mkdir -p ${BACKUP_DIR}

# Create backup
cd /opt/vetclinic
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U ${DB_USER:-vetclinic_user} ${DB_NAME:-vetclinic} > ${BACKUP_DIR}/${BACKUP_FILE}

# Compress backup
gzip ${BACKUP_DIR}/${BACKUP_FILE}

# Delete old backups
find ${BACKUP_DIR} -name "vetclinic_backup_*.sql.gz" -mtime +${KEEP_DAYS} -delete

echo "✅ Backup created: ${BACKUP_FILE}.gz"
echo "📁 Location: ${BACKUP_DIR}"

