#!/bin/bash

# Exit on error
set -e

# Configuration
APP_DIR="/opt/agilizedmc"
BACKUP_USER="backup-user"
BACKUP_GROUP="backup-user"

# Create backup user if not exists
if ! id "$BACKUP_USER" &>/dev/null; then
    useradd -r -s /bin/false "$BACKUP_USER"
fi

# Create application directory
mkdir -p "$APP_DIR"
chown "$BACKUP_USER:$BACKUP_GROUP" "$APP_DIR"

# Install uv if not present
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create and activate virtual environment
uv venv "$APP_DIR/.venv"

# Install dependencies using uv
uv pip install -r requirements.txt

# Copy systemd service file
cp deploy/mysql-backup.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable mysql-backup
systemctl start mysql-backup

# Set up log rotation
cat > /etc/logrotate.d/mysql-backup << EOF
/opt/agilizedmc/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 backup-user backup-user
}
EOF

echo "Deployment completed successfully!" 