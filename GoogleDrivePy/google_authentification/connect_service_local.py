from oauth2client import file, client, tools
from googleapiclient.discovery import build
from httplib2 import Http
from google.cloud import storage, bigquery
class connect_service_local:
	def __init__(self, path_json,path_service_account, scope):
		self.path_json = path_json
		self.path_service_account = path_service_account
		self.scope = scope

	def get_storage_client(self):
		"""
		This function gives access to Google platform by passing the credential
		to from_service_account_json
		The path_service_account needs to be the full name. It can be downloaded
		from the API authentification
		"""
		storage_client = storage.Client.from_service_account_json(self.path_service_account)
		bigquery_client = bigquery.Client.from_service_account_json(self.path_service_account)
		service_account = {
			"Storage_account" : storage_client,
			"bigquery_account" : bigquery_client,
			}
		print('Service account storage and Bigquery are now connected. \n' \
		'Service account storage is stored as {} and accessible with "Storage_account" \n' \
		'Service account Bigquery is stored as {} and accessible with "bigquery_account"'.format(
		service_account["Storage_account"],
		service_account["bigquery_account"])
		)
		return service_account

	def get_service(self):
		"""
		This function gives access to Google drive and currently Google doc
		The path to access the token and credential can be locally
		or in Googe Drive. By default, the token is stored as 'token' and the
		credential as 'credentials.json'. They need to have this name.

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
		service_excel = build('sheets', 'v4', http=creds.authorize(Http()))
		service = {
			"drive" : service,
			"doc": service_doc,
			"sheet": service_excel
			}
		print('Service Google Drive and Docs, Sheet are now connected. \n' \
		'Service Google Drive is stored as {} and accessible with "drive" \n' \
		'Service Google Doc is stored as {} and accessible with "doc" \n' \
		'Service Google Sheet is stored as {}and accessible with "sheet"'.format(
		service["drive"],
		service["doc"],
		service["sheet"])
		)
		return service
