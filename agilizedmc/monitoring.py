from prometheus_client import Counter, Histogram, start_http_server
import time

# Define metrics
BACKUP_DURATION = Histogram(
    'mysql_backup_duration_seconds',
    'Time spent performing MySQL backup'
)

BACKUP_SUCCESS = Counter(
    'mysql_backup_success_total',
    'Number of successful MySQL backups'
)

BACKUP_FAILURE = Counter(
    'mysql_backup_failure_total',
    'Number of failed MySQL backups'
)

UPLOAD_DURATION = Histogram(
    'gdrive_upload_duration_seconds',
    'Time spent uploading to Google Drive'
)

def start_metrics_server(port=8000):
    start_http_server(port) 