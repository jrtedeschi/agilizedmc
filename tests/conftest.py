import pytest
import os
from pathlib import Path
import tempfile
import yaml
from unittest.mock import Mock

from agilizedmc.config import Config, DatabaseConfig

@pytest.fixture
def test_config():
    """Load test configuration"""
    config_path = Path(__file__).parent / 'config' / 'test_config.yml'
    with open(config_path) as f:
        config_data = yaml.safe_load(f)
    return Config(
        database=DatabaseConfig(**config_data['database']),
        google_drive_folder_id=config_data['google_drive_folder_id'],
        backup_dir=config_data['backup_dir'],
        ssh_config={},
        telegram_bot_token=config_data['telegram']['bot_token'],
        telegram_chat_id=config_data['telegram']['chat_id'],
        service_account_file=config_data['service_account_file']
    )

@pytest.fixture
def temp_backup_dir():
    """Create temporary backup directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def mock_google_drive():
    """Mock Google Drive service"""
    return Mock()

@pytest.fixture
def mock_telegram():
    """Mock Telegram notification service"""
    return Mock()

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables"""
    os.environ['MYSQL_HOST'] = 'localhost'
    os.environ['MYSQL_PORT'] = '3306'
    os.environ['MYSQL_USER'] = 'root'
    os.environ['MYSQL_PASSWORD'] = 'test_password'
    os.environ['MYSQL_DATABASE'] = 'test_db'
    yield
    # Cleanup environment after tests
    for key in ['MYSQL_HOST', 'MYSQL_PORT', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE']:
        os.environ.pop(key, None) 