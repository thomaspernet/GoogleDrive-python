#from oauth2client import file, client, tools
from googleapiclient.discovery import build
import pickle, shutil
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
#from httplib2 import Http
from google.cloud import storage, bigquery

class get_authorization:
	def __init__(self,
	path_credential_drive = None,
	path_credential_gcp = None,
	scope = None,
	verbose = False):
		"""
		path_credential: connect to Google Drive and associated project:
		GSpreadhseet/GDoc. This is the pickle file containing the token
		path_service_account: connect to google cloud Service: BQ/GCS. This is
		the json file containing the credentials
		"""
		self.path_credential_drive = path_credential_drive
		self.path_credential_gcp = path_credential_gcp
		self.scope = scope
		self.verbose = verbose


	def authorization_gcp(self):
		"""
		This function gives access to Google Cloud platform by passing the credential
		to from_service_account_json
		The path_service_account needs to be the full name. It can be downloaded
		from the API authorization
		"""
		storage_client = storage.Client.from_service_account_json(
		self.path_credential_gcp)
		bigquery_client = bigquery.Client.from_service_account_json(
		self.path_credential_gcp)
		service_account = {
			"Storage_account" : storage_client,
			"bigquery_account" : bigquery_client,
			}
		if self.verbose:
			print("""
			Service account storage and Bigquery are now connected.\n
		'Service account storage is stored as {} and accessible with
		"Storage_account"
		'Service account Bigquery is stored as {} and accessible with
		"bigquery_account"""
		.format(
		service_account["Storage_account"],
		service_account["bigquery_account"])
		)
		return service_account

	def authorization_drive(self,save_credential = True, verbose = False, path_secret = None):
		"""
		This function gives access to Google drive and currently Google doc
		The path to access the token and credential can be locally
		or in Googe Drive. By default, the token is stored as 'token' and the
		credential as 'credentials.json'. They need to have this name.

		The scope tells the app what action it can do. ie read only, write, etc

		path_json is where the token is stored. If Google cannot find the token
		is the defined path, then he will search for the credential. After that
		you will be prompt to give Google access to your "scope". The token is
		stored in the same folder as the credential. Feel free to move the
		token anywhere you want, and point the init to this path in the future.

		ADD ERROR MESSAGE
		path_secret: path to credential.json include full path
		"""
		creds = None
		updated = False

		path_pickle = os.path.join(self.path_credential_drive, 'token.pickle')
		if os.path.exists(path_pickle):
			with open(path_pickle, 'rb') as token:
				creds = pickle.load(token)
		# If there are no (valid) credentials available, let the user log in.

		if not creds or not creds.valid:
			updated = True
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					path_secret, self.scope,
					redirect_uri='urn:ietf:wg:oauth:2.0:oob')
				creds = flow.run_local_server()
	# Save the credentials for the next run
		if save_credential:

			with open('token.pickle', 'wb') as token:
				pickle.dump(creds, token)

			shutil.move(
			os.path.join(os.getcwd(), 'token.pickle'),
			path_pickle)
			### Move the credential to the same path_credential_drive


		service = build('drive', 'v3', credentials= creds)
		service_doc = build('docs', 'v1', credentials= creds)
		service_excel = build('sheets', 'v4', credentials= creds)
		service = {
			"drive" : service,
			"doc": service_doc,
			"sheet": service_excel
			}
		if self.verbose:
			try:
				if creds.valid and not updated:
					print("The statut credential from {} is valid".format(
					path_pickle))
				else:
					print("""
					The statut credential from {} is not valid.\n
				A new credential has been created/updated
					""".format(
					path_pickle))
			except:
				pass
			print("""
			Service Google Drive and Docs, Sheet are now connected.\n
			'Service Google Drive is stored as {} and accessible with "drive"\n
			'Service Google Doc is stored as {} and accessible with "doc"\n
			'Service Google Sheet is stored as {}and accessible with "sheet"""
			.format(
			service["drive"],
			service["doc"],
			service["sheet"])
			)
		return service
