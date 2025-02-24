import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from agilizedmc.services.google_drive_service import GoogleDriveService

@pytest.fixture
def drive_service():
    with patch('google.oauth2.service_account.Credentials'), \
         patch('googleapiclient.discovery.build'):
        return GoogleDriveService("test_folder", "test.json")

def test_upload_file(drive_service):
    with patch('googleapiclient.http.MediaFileUpload'), \
         patch.object(drive_service.service.files(), 'create') as mock_create:
        mock_create.return_value.execute.return_value = {'id': 'test_id'}
        result = drive_service.upload_file(Path("test.txt"))
        assert result == 'test_id'