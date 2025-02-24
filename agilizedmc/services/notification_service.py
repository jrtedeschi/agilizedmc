import requests
from ..utils.logging import setup_logger

logger = setup_logger()

class NotificationService:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        
    def send_message(self, message: str) -> bool:
        """Send regular message to Telegram"""
        try:
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "HTML"
                }
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {str(e)}")
            return False
            
    def send_alert(self, error_message: str) -> bool:
        """Send error alert to Telegram"""
        alert = f"🚨 ALERT!\n\n{error_message}"
        return self.send_message(alert) 