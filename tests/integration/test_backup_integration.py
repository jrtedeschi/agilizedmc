import pytest
from pathlib import Path
import mysql.connector
from agilizedmc.services.backup_service import BackupService
from agilizedmc.config import Config

@pytest.mark.integration
class TestBackupIntegration:
    @pytest.fixture(scope="class")
    def test_database(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="test_password"
            )
            cursor = conn.cursor()
            
            cursor.execute("CREATE DATABASE IF NOT EXISTS test_db")
            cursor.execute("USE test_db")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id INT PRIMARY KEY,
                    name VARCHAR(50)
                )
            """)
            
            cursor.execute("INSERT INTO test_table VALUES (1, 'test')")
            conn.commit()
            
            yield
            
            cursor.execute("DROP DATABASE test_db")
            conn.close()
        except mysql.connector.Error as e:
            pytest.skip(f"MySQL not available: {str(e)}")

    def test_full_backup_cycle(self, test_database, tmp_path):
        config = Config.from_env()
        notification = Mock()
        service = BackupService(config, notification)
        success = service.backup_and_upload()
        assert success
        
        # Verify backup was created and uploaded
        notification.send_message.assert_called_once()
        
        # Verify backup was cleaned up locally
        backup_files = list(Path(config.backup_dir).glob("backup_*.sql"))
        assert len(backup_files) == 0 