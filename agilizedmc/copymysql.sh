#!/bin/bash

# Get credentials from the environment
DB_USER=$MYSQL_USER
DB_PASSWORD=$MYSQL_PASSWORD
# DB_NAME=$MYSQL_DATABASE

DB_BACKUP_DIR=$MYSQL_BACKUP_DIR

# Create the backup directory if it doesn't exist
mkdir -p $DB_BACKUP_DIR

# Create a backup file name with the current date
BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d).sql"

# Perform the MySQL database backup
mysqldump -u $DB_USER -p$DB_PASSWORD > $BACKUP_FILE

# Zip the backup file
gzip $BACKUP_FILE

# Encrypt the zipped backup file using GPG
gpg --output $DB_BACKUP_DIR/$BACKUP_FILE.gz.gpg --symmetric --cipher-algo AES256 $BACKUP_FILE.gz

echo "saving to $DB_BACKUP_DIR/$BACKUP_FILE.gz.gpg"


#write the results into a log file in the format of date and time YYYY-MM-DD HH:MM:SS filename status
echo "$(date +%Y-%m-%d) $(date +%H:%M:%S) $BACKUP_FILE.gz.gpg success" >> $DB_BACKUP_DIR/backup.log

# Remove the unencrypted backup file
rm $BACKUP_FILE.gz

echo "MySQL database backup completed successfully!"