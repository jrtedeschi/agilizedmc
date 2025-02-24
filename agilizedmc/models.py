from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from datetime import datetime

# Simple type aliases for Google Drive API responses
DriveFile = Dict[str, Any]
DriveFileList = List[DriveFile]

class DriveFile(TypedDict, total=False):
    id: str
    name: str
    created_time: str

class DriveFileList(TypedDict):
    files: List[DriveFile] 