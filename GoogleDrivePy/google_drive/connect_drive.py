from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools

class connect_drive:
	def __init__(self, service):
		self.service = service
		self.service_drive = self.service["drive"]
		self.service_doc = self.service["doc"]

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
		#service = self.service["drive"]
		media_body = MediaFileUpload(name,
								 mimetype=mime_type,
								 resumable=True
								 )
		body = {
		'title': name,
		'name': name,
		'mimeType': mime_type
		}

		upload = self.service_drive.files().create(
			body= body,
			media_body=media_body,
			fields='id').execute()

		file_ID = upload.get('id')
		print('File ID: {}'.format(file_ID))

		return file_ID

	def find_folder_id(self, folder_name, to_print = True):
		"""
		The function find the ID of a folder. In order to maximize the search
		it is best to give unique name to folder
		"""
		search = "mimeType = 'application/vnd.google-apps.folder'" \
		" and name contains '" + str(folder_name) + "'"
		page_token = None
		while True:
			response = self.service_drive.files().list(
										  q= search,
										  spaces='drive',
										  fields='nextPageToken,' \
										  'files(id, name)',
										  pageToken=page_token).execute()
			for file in response.get('files', []):
		# Process change
				folder_id =  file.get('id')
				if to_print:
					print('Found file: %s (%s)' % (file.get('name'), folder_id))
				page_token = response.get('nextPageToken', None)
				return folder_id
			if page_token is None:
				break
		print('Folder {} not found'.format(folder_name))


	def find_file_id(self, file_name, to_print = True):
		"""
		The function find the ID of a file. In order to maximize the search
		it is best to give unique name to file.
		"""
		search  = "name = '" + str(file_name) + "' and trashed = false"
		page_token = None
		while True:
			response = self.service_drive.files().list(
										  q= search,
										  spaces='drive',
										  fields='nextPageToken,' \
										  'files(id, name)',
										  pageToken=page_token).execute()
			for file in response.get('files', []):
		# Process change
				file_id =  file.get('id')
				if to_print:
					print('Found file: %s (%s)' % (file.get('name'), file_id))
				page_token = response.get('nextPageToken', None)
				return file_id
			if page_token is None:
				break
		print('File {} not found'.format(file_name))

	def move_file(self, file_name, folder_name):
		"""
		This function move one file from root to another folder .
		The function uses find_folder_id and find_file_id to get the IDs
		"""
		### get folder ID
		try:
			folder_id = self.find_folder_id(folder_name)
		###
			file_id = self.find_file_id(file_name)
		# Retrieve the existing parents to remove
			file = self.service_drive.files().get(fileId = file_id,
								 fields = 'parents').execute()
			previous_parents = ",".join(file.get(
								 'parents'))
		# Move the file to the new folder
			file = self.service_drive.files().update(fileId = file_id,
									addParents = folder_id,
									removeParents = previous_parents,
									fields = 'id, parents').execute()
			print('File {} moved to {}'.format(file_name, folder_name))
		except:
			print('Impossible to move {} in {}'.format(file_name, folder_name))
	def access_google_doc(self, file_name):
		"""
		The function searches for an existing document. If the
		document is not found, then one is created
		"""
		doc_id = self.find_file_id(file_name = file_name, to_print = False)
		if doc_id is None:
			title = file_name
			body = {
				  'title': title
				  }
			doc = self.service_doc.documents() \
			  .create(body=body).execute()
			doc_id = self.find_file_id(file_name = file_name, to_print = False)
		print('Created document {} with name {}'.format(doc_id, title))
		return doc_id
