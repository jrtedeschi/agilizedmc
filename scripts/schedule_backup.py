from apscheduler.schedulers.blocking import BlockingScheduler
from agilizedmc.services.backup_service import BackupService
from agilizedmc.config import Config
from agilizedmc.services.notification_service import NotificationService

def run_backup():
    config = Config.from_env()
    notification = NotificationService(
        bot_token=config.telegram_bot_token,
        chat_id=config.telegram_chat_id
    )
    
    backup_service = BackupService(config, notification)
    backup_service.backup_and_upload()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(run_backup, 'cron', hour=2)  # Run at 2 AM daily
    scheduler.start() 