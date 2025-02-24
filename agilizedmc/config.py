from dataclasses import dataclass
from typing import Optional
import os
import yaml

@dataclass
class DatabaseConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

@dataclass
class Config:
    database: DatabaseConfig
    google_drive_folder_id: str
    backup_dir: str
    ssh_config: dict
    telegram_bot_token: str
    telegram_chat_id: str
    service_account_file: str
    
    @classmethod
    def from_env(cls) -> 'Config':
        return cls(
            database=DatabaseConfig(
                host=os.getenv('DB_HOST'),
                port=int(os.getenv('DB_PORT', 3306)),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            ),
            google_drive_folder_id=os.getenv('GDRIVE_FOLDER_ID'),
            backup_dir=os.getenv('BACKUP_DIR'),
            ssh_config={
                'host': os.getenv('SSH_HOST'),
                'port': int(os.getenv('SSH_PORT', 22)),
                'username': os.getenv('SSH_USER'),
                'password': os.getenv('SSH_PASSWORD')
            },
            telegram_bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
            telegram_chat_id=os.getenv('TELEGRAM_CHAT_ID'),
            service_account_file=os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        )
