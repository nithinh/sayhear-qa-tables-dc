from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from os import listdir
from os.path import isfile, join



# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']

def download_file(service,file_id,file_name,folder_id):
    file_id = '' + file_id
    print(file_id)
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(folder_id + '/'+file_name, mode='w')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))

def set_up_service():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def download_files_in_folder(src_folder_id,service,tgt_folder):
    # Call the Drive v3 API
    q = "'" + src_folder_id + "' in parents and trashed = false" 
    results = service.files().list(q=q,
        pageSize=1000, fields="nextPageToken, files(id, name)",supportsTeamDrives=True,
       includeTeamDriveItems=True).execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            download_file(service,item['id'],item['name'],tgt_folder)

def export_to_drive_folder(service,src_path="tables",folder_id='1ZG4cIctPwOYvtD1ISUftqvdJKheQ12PR'):
    onlyfiles = [f for f in listdir(src_path) if isfile(join(src_path, f))]
    for f in onlyfiles:
        file_metadata = {
            'name': f,
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'parents': [folder_id]
        }
        media = MediaFileUpload(src_path + '/'+f,
                                mimetype='text/csv',
                                resumable=True)
        file = service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
    


def main():
    
    service = set_up_service()
    download_files_in_folder('1ZG4cIctPwOYvtD1ISUftqvdJKheQ12PR',service,"tables")
    export_to_drive_folder(service,"tables",'1pUYcXUumh7yMqyDj8zORPwzZUcP-cNkM')
    

if __name__ == '__main__':
    main()