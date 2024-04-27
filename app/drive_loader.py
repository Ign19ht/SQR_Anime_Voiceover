from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
import pandas as pd
import io
import os


# Scope for reading (and optionally writing) files
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

TOKEN_FILE = os.getenv("TOKEN_FILE")
CLIENT_API_SECRET = os.getenv("CLIENT_API_SECRET")

class DriveReader:
    def __init__(self) -> None:
        self.service = self.__authenticate()

    def __authenticate(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        creds = service_account.Credentials.from_service_account_file( os.path.join(script_directory, CLIENT_API_SECRET), scopes=SCOPES )
        return build('drive', 'v3', credentials=creds)
    
    def read_transcripts(self, folder_id):
        query = f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        results = self.service.files().list(
            q=query,
            fields="nextPageToken, files(id, name, mimeType, parents)",
            spaces='drive'
        ).execute()

        items = results.get('files', [])
        file_dict = {}
        for item in items:
            if item['mimeType'] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                # Download the file as previously
                request = self.service.files().get_media(fileId=item['id'])
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                fh.seek(0)
                df = pd.read_excel(fh)
                file_dict[item['name']] = df

        return file_dict


