from google.colab import drive
from google.colab import auth
from oauth2client import file, client, tools
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from httplib2 import Http

class connect_service:
	def __init__(self, path_json, scope):
		self.path_json = path_json
		self.scole = scope
	def get_auth(self):
		"""
		This function mounts a Google Drive in Google Colab. The objective is
		to access the json credential directly from Google Drive since Google
		Colab creates new instance each time, there is no other way to locate
		the credentialself

		The function also gives access to SDK
		"""

		drive.mount('/content/gdrive')
		auth.authenticate_user()
	def get_service(self):
		"""
		This function gives access to Google drive and currently Google doc
		The path to access the token and credential can be locally
		or in Googe Drive. By default, the token is stored as 'token' and the
		credential as 'credentials.json'. They need to have this nameself.

		The scope tells the app what action it can do. ie read only, write, etc

		ADD ERROR MESSAGE
		"""

		path_token = self.path_json + "token.json"
		path_credential = self.path_json + "credentials.json"
		store = file.Storage(path_token)
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets(path_credential, self.scope)
			creds = tools.run_flow(flow, store)
		service = build('drive', 'v3', http=creds.authorize(Http()))
		service_doc = build('docs', 'v1', http=creds.authorize(Http()))
		service = {
            "drive" : service,
            "doc": service_doc
			}
		print('Service Google Drive and Google Docs are now connected. \n' \
		'Service Google Drive is stored as {} and accessible with "drive" \n' \
		'Service Google Doc is stored as {}and accessible with "doc"'.format(
		service["drive"],
		service["doc"])
		)
		return service
