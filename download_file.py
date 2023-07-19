from __future__ import print_function

import io
import os.path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def download_file(real_file_id):
    """Downloads a file
    Args:
        real_file_id: ID of the file to download
    Returns : IO object with location.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_id = real_file_id

        # Make a request to get the file metadata
        file_metadata = service.files().get(fileId=file_id).execute()

        # Get the file's name and download URL
        file_name = file_metadata["name"]

        # Make a request to download the file
        request = service.files().get_media(fileId=file_id)
        response = request.execute()

        # Save the file to the desired location on your local machine
        with io.open(file_name, "wb") as file:
            file.write(response)

        print(f"File '{file_name}' downloaded successfully.")

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None



if __name__ == '__main__':
    file_id = '1gN0TJMXlcAp47m5XmHAADSfWIl_aRU1u'
    download_file(real_file_id=file_id)