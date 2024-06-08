"""Main module."""
# import gdrive 
import os
import sys
import json
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request


def upload_file(file_path, folder_id, service_account_file):
    """
    Upload a file to a Google Drive folder.

    Parameters
    ----------
    file_path : str
        The path to the file to upload.
    folder_id : str
        The ID of the folder to upload the file to.
    service_account_file : str
        The path to the service account file.

    Returns
    -------
    dict
        The response from the Google Drive API.
    """
    # Load the service account credentials
    creds = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=['https://www.googleapis.com/auth/drive']
    )

    # Build the Google Drive service
    service = build('drive', 'v3', credentials=creds)

    # Create the file metadata
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }

    # Create the media upload
    media = MediaFileUpload(file_path)

    # Upload the file
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return file

if __name__ == '__main__':
    file_path = sys.argv[1]
    folder_id = sys.argv[2]
    service_account_file = sys.argv[3]


    if not os.path.exists(file_path):
        raise FileNotFoundError(f'File not found: {file_path}')
    
    if not os.path.exists(service_account_file):
        raise FileNotFoundError(f'File not found: {service_account_file}')
    
    if not folder_id:
        raise ValueError('Folder ID is required')
    
    
    print(upload_file(file_path, folder_id, service_account_file))
    