from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from pathlib import Path
from typing import List, Dict, Any
from ..models import DriveFile, DriveFileList

class GoogleDriveService:
    def __init__(self, folder_id: str, service_account_file: str):
        self.folder_id = folder_id
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        self.service = build('drive', 'v3', credentials=credentials)
    
    def upload_file(self, file_path: Path) -> str:
        """Upload file to Google Drive and return file ID"""
        file_metadata = {
            'name': file_path.name,
            'parents': [self.folder_id]
        }
        media = MediaFileUpload(str(file_path))
        response = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        return response['id']

    def list_files(self) -> DriveFileList:
        """List files in the backup folder"""
        response = self.service.files().list(
            q=f"'{self.folder_id}' in parents",
            fields="files(id, name, createdTime)"
        ).execute()
        return response.get('files', [])

    def delete_file(self, file_id: str) -> None:
        """Delete a file by ID"""
        self.service.files().delete(fileId=file_id).execute() 