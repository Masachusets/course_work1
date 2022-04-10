from __future__ import print_function

import io
import os
import requests
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apiclient.http import MediaIoBaseUpload
from tqdm import tqdm

# If modifying these scopes, delete the file token.json.


class GoogleObject:
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self):
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def main(self):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        try:
            service = build('drive', 'v3', credentials=self.creds)
            # Call the Drive v3 API
            results = service.files().list(
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
        except HttpError as error:
            print(f'An error occurred: {error}')

    def upload_file(self, link, name, drive_folder_id, mimetype='image/jpg'):
        service = build('drive', 'v3', credentials=self.creds)
        file_content = requests.get(link).content
        fh = io.BytesIO(file_content)
        media = MediaIoBaseUpload(fh, mimetype=mimetype)
        service.files().create(body={'name': name, 'parents': [drive_folder_id]},
                               media_body=media,
                               fields='id').execute()
        fh.seek(0)

    def import_photos_to_disk(self, photos):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        try:
            service = build('drive', 'v3', credentials=self.creds)
            direct = time.strftime('%y_%m_%d', time.gmtime(time.time()))
            dir_metadata = {'name': direct,
                            'mimeType': 'application/vnd.google-apps.folder'}
            drive_folder_id = service.files().create(body=dir_metadata,
                                                     fields='id').execute().get('id')
            for file_name, photo in tqdm(photos.items()):
                link = photo['url']
                name = file_name
                self.upload_file(link, name, drive_folder_id)
        except HttpError as error:
            print(f'An error occurred: {error}')
        print('Upload complite!')
