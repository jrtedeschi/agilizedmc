from datetime import datetime
from pathlib import Path
import subprocess
from typing import Optional
import os

from ..utils.logging import setup_logger, log_execution_time
from ..config import Config
from .notification_service import NotificationService
from .google_drive_service import GoogleDriveService

logger = setup_logger()

class BackupService:
    def __init__(self, config: Config, notification_service: NotificationService):
        self.config = config
        self.notification = notification_service
        self.drive_service = GoogleDriveService(
            config.google_drive_folder_id,
            config.service_account_file
        )
        
    @log_execution_time
    def create_backup(self) -> Optional[Path]:
        """Create MySQL backup and return path to backup file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = Path(self.config.backup_dir) / f"backup_{timestamp}.sql"
        
        try:
            # Ensure backup directory exists with proper permissions
            backup_path.parent.mkdir(parents=True, exist_ok=True, mode=0o750)
            
            # Create backup using mysqldump with proper permissions
            cmd = [
                'mysqldump',
                f'-u{self.config.database.user}',
                f'-p{self.config.database.password}',
                f'-h{self.config.database.host}',
                f'-P{self.config.database.port}',
                '--single-transaction',  # For InnoDB tables
                '--quick',  # For large databases
                '--compress',  # Network compression
                self.config.database.database,
                f'--result-file={backup_path}'
            ]
            
            # Set umask for secure file creation
            old_umask = os.umask(0o077)
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
            finally:
                os.umask(old_umask)
            
            if result.returncode != 0:
                raise Exception(f"Backup failed: {result.stderr}")
                
            logger.info(f"Backup created successfully at {backup_path}")
            return backup_path
            
        except Exception as e:
            error_msg = f"Failed to create backup: {str(e)}"
            logger.error(error_msg)
            self.notification.send_alert(error_msg)
            return None
            
    @log_execution_time
    def backup_and_upload(self) -> bool:
        """Create backup and upload to Google Drive"""
        try:
            # Create backup
            backup_path = self.create_backup()
            if not backup_path:
                return False
                
            # Upload to Google Drive
            file_id = self.drive_service.upload_file(backup_path)
            
            success_msg = f"Backup successfully created and uploaded to Google Drive. File ID: {file_id}"
            logger.info(success_msg)
            self.notification.send_message(success_msg)
            
            # Cleanup local backup
            backup_path.unlink()
            return True
            
        except Exception as e:
            error_msg = f"Backup and upload failed: {str(e)}"
            logger.error(error_msg)
            self.notification.send_alert(error_msg)
            return False 