import requests
import sys
from ..config import Config
from ..services.notification_service import NotificationService

def check_system_health():
    config = Config.from_env()
    notification = NotificationService(
        config.telegram_bot_token,
        config.telegram_chat_id
    )
    
    checks = {
        'MySQL': check_mysql_connection(),
        'Google Drive': check_gdrive_connection(),
        'Disk Space': check_disk_space(),
        'Backup Directory': check_backup_directory()
    }
    
    failed_checks = {k: v for k, v in checks.items() if not v['status']}
    
    if failed_checks:
        message = "❌ System Health Check Failed:\n\n"
        for service, details in failed_checks.items():
            message += f"• {service}: {details['message']}\n"
        notification.send_alert(message)
        sys.exit(1)
    
    return True

def check_disk_space():
    """Check if there's enough disk space for backups"""
    import shutil
    
    min_space_gb = 10
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    
    return {
        'status': free_gb > min_space_gb,
        'message': f"Only {free_gb}GB free space remaining"
    }

# Add other check functions... 