from pathlib import Path
from datetime import datetime, timedelta
from typing import List
import logging
from ..config import Config
from ..services.google_drive_service import GoogleDriveService

logger = logging.getLogger(__name__)

def cleanup_old_backups(config: Config, days_to_keep: int = 30) -> None:
    """Clean up backups older than specified days"""
    try:
        drive_service = GoogleDriveService(
            config.google_drive_folder_id,
            config.service_account_file
        )
        
        # Get list of backups
        files = drive_service.list_files()
        
        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        # Delete old backups
        for file in files:
            created_time = datetime.fromisoformat(file['createdTime'].replace('Z', '+00:00'))
            if created_time < cutoff_date:
                drive_service.delete_file(file['id'])
                logger.info(f"Deleted old backup: {file['name']}")
                
    except Exception as e:
        logger.error(f"Failed to cleanup old backups: {str(e)}")
        raise 