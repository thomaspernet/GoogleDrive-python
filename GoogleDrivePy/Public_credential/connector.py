from GoogleDrivePy.google_authentification import connect_service_local
import os
import json
import urllib

class open_connection:
    def __init__(self, public_connection=None):
        self.public_connection = public_connection

    def save_json(self):
        """
        save the token and credential into
        the root folder.

        uploaded file can only have two names:
        token and the second one is the GCC project name.

        To open GCS/BQ we need the project name's json file
        We can get easily since it is not the token.json

        """

        uploads = self.public_connection

        for key, value in uploads.value.items():
            # Get the value of token.json
            js = uploads.value[key]['content']

            # Convert byte to string
            js = js.decode("utf-8")

            # Load as json
            data = json.loads(js)

            # Save json
            with open(key, 'w') as outfile:
                json.dump(data, outfile)

            if key != 'token.json':
                return key

    def download_creds(self):
        """
        Downloads credential from GitHub
        """

        url = 'https://raw.githubusercontent.com/thomaspernet/DataLab-JupyterNotebooks'

        dict_creds = {
            'token':
            [url + '/master/Public_credential/token.json', 'token.json'],
            'service': [
                url +
                '/master/Public_credential/valid-pagoda-132423-da5a5f070e64.json',
                'service.json'
            ]
        }

        for key, value in dict_creds.items():
            req = urllib.request.Request(value[0])
            r = urllib.request.urlopen(req).read()
            token = json.loads(r.decode('utf-8'))
            with open(value[1], 'w') as outfile:
                json.dump(token, outfile)

        return 'service.json'

    def connect_remote(self):
        """
        Connect to Google services
        """

        if self.public_connection != None:
            project_name = self.save_json()
        else:
            project_name = self.download_creds()
        scopes = [
            'https://www.googleapis.com/auth/documents.readonly',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets.readonly'
        ]

        pathcredential = os.getcwd() + '/'
        serviceaccount = pathcredential + project_name

        cs = connect_service_local.connect_service_local(
            path_json=pathcredential,
            path_service_account=serviceaccount,
            scope=scopes)
        service = cs.get_service()
        return service
