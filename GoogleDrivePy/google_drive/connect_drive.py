from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools

class connect_drive:
    def __init__(self, service):
        self.service = service

    def create_file_root(self, mime_type, name):
        """
        The function creates a file in the root of Google Drive.
        mime_type: You can use MIME types to filter query results or
        have your app listed in the Chrome Web Store list of apps that
        can open specific file types.
        list
        https://stackoverflow.com/questions/11894772/
        google-drive-mime-types-listing

        """
        service = self.service["drive"]
        media_body = MediaFileUpload(name,
                                 mimetype=mime_type,
                                 resumable=True
                                 )
        body = {
        'title': name,
        'name': name,
        'mimeType': mime_type
        }

        upload = service.files().create(
            body= body,
            media_body=media_body,
            fields='id').execute()

        file_ID = upload.get('id')
        print('File ID: {}'.format(file_ID))

        return file_ID
