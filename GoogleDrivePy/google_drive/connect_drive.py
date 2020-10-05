from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools
import re
import pandas as pd
import itertools

# Create alphabet for spreadsheet
alphabet = [
		'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
		'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
        ]

test = list(itertools.product(alphabet, alphabet))
list_alphabet = []
for t in test:
    list_alphabet.append(''.join(t))
alphabet.extend(list_alphabet)


class drive_operations:
	def __init__(self, service, verbose=True):
		self.service = service
		self.service_drive = self.service["drive"]
		self.service_doc = self.service["doc"]
		self.service_sheet = self.service["sheet"]
		self.verbose = verbose

	def download_file(self, filename= None, file_id = None):
		if file_id == None:
			file_id = self.find_file_id(file_name = filename, to_print=False)
		request = self.service_drive.files().get_media(fileId=file_id)
		fh = io.BytesIO()
		downloader = MediaIoBaseDownload(fh, request)
		done = False
		while done is False:
		    status, done = downloader.next_chunk()
		    

	def upload_file_root(self, mime_type, file_name, local_path):
		"""
		The function creates a file in the root of Google Drive.
		mime_type: You can use MIME types to filter query results or
		have your app listed in the Chrome Web Store list of apps that
		can open specific file types.
		list
		https://stackoverflow.com/questions/11894772/
		google-drive-mime-types-listing

		"""
		# service = self.service["drive"]
		media_body = MediaFileUpload(local_path,
								 mimetype=mime_type,
								 resumable=True
								 )
		body = {
		'title': file_name,
		'name': file_name,
		'mimeType': mime_type
		}

		upload = self.service_drive.files().create(
			body=body,
			media_body=media_body,
			fields='id').execute()

		file_ID = upload.get('id')
		# print('File ID: {}'.format(file_ID))

		return file_ID

	def find_folder_id(self, folder_name, to_print=True):
		"""
		The function find the ID of a folder. In order to maximize the search
		it is best to give unique name to folder
		"""
		search = "mimeType = 'application/vnd.google-apps.folder'" \
		" and name contains '" + str(folder_name) + "'"
		page_token = None
		while True:
			response = self.service_drive.files().list(
										  q=search,
										  spaces='drive',
										  fields='nextPageToken,'
										  'files(id, name)',
										  pageToken=page_token).execute()
			for file in response.get('files', []):
		# Process change
				folder_id = file.get('id')
				if to_print:
					print('Found file: %s (%s)' % (file.get('name'), folder_id))
				page_token = response.get('nextPageToken', None)
				return folder_id
			if page_token is None:
				break
		print('Folder {} not found'.format(folder_name))

	def find_file_id(self, file_name, to_print=True):
		"""
		The function find the ID of a file. In order to maximize the search
		it is best to give unique name to file.
		"""
		search = "name = '" + str(file_name) + "' and trashed = false"
		page_token = None
		while True:
			response = self.service_drive.files().list(
										  q=search,
										  spaces='drive',
										  fields='nextPageToken,'
										  'files(id, name)',
										  pageToken=page_token).execute()
			for file in response.get('files', []):
		# Process change
				file_id = file.get('id')
				if to_print:
					print('Found file: %s (%s)' % (file.get('name'), file_id))
				page_token = response.get('nextPageToken', None)
				return file_id
			if page_token is None:
				break
		print('File {} not found'.format(file_name))

	def delete_file(self, filename= None, file_id = None):
		"""Permanently delete a file, skipping the trash.

		Args:
		    service: Drive API service instance.
			filename: Default None. If not provided, use file_id
		    file_id: Default None. ID of the file to delete.
		"""
		if file_id == None:
			file_id = self.find_file_id(file_name = filename, to_print=False)
		try:
			self.service_drive.files().delete(fileId=file_id).execute()
		except:
			print('Impossible to move {}'.format(file_id))

	def move_file(self, file_name, folder_name):
		"""
		This function move one file from root to another folder .
		The function uses find_folder_id and find_file_id to get the IDs
		"""
		# get folder ID
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
			return {'file_name':file_name, 'folder_name': folder_name}
		except:
			print('Impossible to move {} in {}'.format(file_name, folder_name))

	def access_google_doc(self, doc_name):
		"""
		The function searches for an existing document. If the
		document is not found, then one is created
		"""
		doc_id = self.find_file_id(file_name = doc_name, to_print = False)
		if doc_id is None:
			title = doc_name
			body = {
				  'title': title
				  }
			doc = self.service_doc.documents() \
			  .create(body=body).execute()
			doc_id = self.find_file_id(file_name = doc_name, to_print = False)
			print('Created document {} with name {}'.format(doc_id, title))
		return doc_id

	def add_image_to_doc(self, image_name, doc_name):
		"""
		The function finds or creates a new Google docs and appends images.
		The image should be saved in Google drive
		image_id: id of the image in the drive
		doc_id: id of the doc in the drive
		"""

		image_id = self.find_file_id(file_name = image_name, to_print = False)
		doc_id = self.access_google_doc(doc_name)

		url = 'http://drive.google.com/uc?export=view&id=' + str(image_id)

		# Get index document
		document = self.service_doc.documents().get(documentId=doc_id).execute()
		content  = document.get('body')
		index = content["content"][1]['paragraph']['elements'][0]['endIndex']
		# Retrieve the documents contents from the Docs service.
		requests = [
			{
			'insertInlineImage': {
			'location': {
				'index': index - 1
			},
			'uri':
				url
			}}
		]

		# Execute the request.
		result = self.service_doc.documents().batchUpdate(
			documentId=doc_id, body={'requests': requests}).execute()
		print('Image added to {}'.format(doc_name))

	def add_bullet_to_doc(self, doc_name, name_bullet= "Hello world"):
		"""
		Shows basic usage of the Docs API.
		Prints the title of a sample document.
		"""
		# Get index document
		doc_id = self.access_google_doc(doc_name)
		document = self.service_doc.documents().get(documentId=doc_id).execute()
		content  = document.get('body')
		index = content["content"][1]['paragraph']['elements'][0]['endIndex']
		requests = [
			 {
				'insertText': {
					'location': {
					'index': 1
					},
					'text': str(name_bullet) + '\n',
					}}, {
				'createParagraphBullets': {
					'range': {
						'startIndex': 1,
						'endIndex':  index + 1
						},
				'bulletPreset': 'BULLET_ARROW_DIAMOND_DISC',
			}
		}
	]

	# Execute the request.
		result = self.service_doc.documents().batchUpdate(
			documentId=doc_id, body={'requests': requests}).execute()
		print('Bullet point added to {}'.format(doc_name))

	def add_data_to_spreadsheet(self, data, sheetID, sheetName,
							detectRange = True, rangeData = None):
		"""
		Add Data to an existing Spreadsheet
		- Data: Pandas Dataframe
		- SheetID: Sheet ID
		- Name of sheet to add the data. If not exist, then a new one is added
		- header: Boolean. If True: Then append Data, else header is dataframe colname
		- detectRange: Boolean: If True, then automatically detect range
		- rangeData: By default None, else User define range 'SHEETNAME$AA00:BB11'
			- Not, it should include one row for the header!
		"""

		# Check if sheetName exit
		sheet_metadata = self.service_sheet.spreadsheets().get(
			  spreadsheetId = sheetID
			  ).execute()

		sheets = sheet_metadata.get('sheets', '')
		list_sheets = [sheets[x].get("properties", {}).get("title", {})
				 for x in range(0, len(sheets))]

		if not sheetName in list_sheets:

			data_s = {'requests': [
				{
					 'addSheet':{
					'properties':{'title': sheetName}
					}
				}
				]}
	# Add new sheet
			self.service_sheet.spreadsheets().batchUpdate(
			  spreadsheetId= sheetID,
			  body=data_s
			).execute()

	# Make Data to list: Google engine needs JSON serialized

		data_list = data.to_numpy().tolist()
		headers_name = list(data)

	# Get size of the data
		total_rows, total_col  = data.shape

	# If detect range
		if detectRange:

		# Get size of the sheet
			nb_cols, n_row = self.getRowAndColumns(sheetID = sheetID,
										  sheetName = sheetName)


		# range does not exist
			if n_row == 1:
			# The sheet is empty so we use the number of columns
			# In the data to know the range
				first_cell = n_row
				nb_cols = total_col
			# add header
				data_list.insert(0, headers_name)
			else:
				nb_cols = nb_cols
				first_cell = n_row + 3
				data_list.insert(0, headers_name)

			for i, letter in enumerate(alphabet):
				if i == nb_cols:
					range_ = letter
				if i + 2 == nb_cols:
					range_ = letter

			last_rows = n_row + total_rows + 3

			range_sprs = '{0}!A{1}:{2}{3}'
		# Add one for the first row to write
			range_sprs = range_sprs.format(sheetName, first_cell,
			 range_, last_rows)
		else:
			range_sprs = rangeData
		# if user add custom range, then need to add headers
			data_list.insert(0, headers_name)

	# Add to Spreadsheet
		data_ = [
			  {
			'range': range_sprs,
			'values': data_list
		  },
	# Additional ranges to update ...
	  ]
		body = {
			'valueInputOption': 'RAW',
			'data': data_
	}

		result = self.service_sheet.spreadsheets().values().batchUpdate(
			spreadsheetId= sheetID, body=body).execute()

		print('Range {0} has been updated.'.format(range_sprs))

	def upload_data_from_spreadsheet(self, sheetID, sheetName,
	 to_dataframe = True):
		"""
		Upload data from Google spreadsheet
		If to_dataframe then return the data to a dataframe.

		The function return automaticall all the data

		"""

		nb_cols, n_row = self.getRowAndColumns(sheetID, sheetName)

		for i, letter in enumerate(alphabet):
			if i == nb_cols:
				range_ = letter
			if i + 2 == nb_cols:
				range_ = letter

		range_sprs = '{0}!A1:{1}{2}'
		range_sprs = range_sprs.format(sheetName, range_, n_row)

		load_spreadsheets = self.service_sheet.spreadsheets().values().get(
			spreadsheetId=sheetID,
			range=range_sprs).execute()

		if to_dataframe:

			load_spreadsheets = pd.DataFrame(
			load_spreadsheets.get('values', []),columns =
						load_spreadsheets['values'][0]).drop([0])

		return load_spreadsheets


	def getLatestRow(self, sheetID, sheetName):
		"""
		The option includeGridData = True in the get elements return a dictionary
		with the row sort_values
		We can count how many elements there are to get the latest row
		"""

		gridData = self.service_sheet.spreadsheets().get(
		spreadsheetId = sheetID, includeGridData = True).execute()

		sheets = gridData.get('sheets', '')
		list_sheets = [sheets[x].get("properties", {}).get("title", {})
			   for x in range(0, len(sheets))]

		index_sheet = list_sheets.index(sheetName)

		try:
			# latestRow = gridData['sheets'][
			# index_sheet]['properties']['gridProperties']['rowCount']
			# Property above includes all rows, empty included
			latestRow = len(gridData['sheets'][index_sheet]['data'][0]['rowData'])
			# len(
			# gridData['sheets'][index_sheet]['data'][0]['rowData'])
		except:
			latestRow = 1

		return latestRow


	def getColumnNumber(self, sheetID, sheetName):
		"""
		The option includeGridData = True in the get elements return a dictionary
		with the row sort_values
		We can count how many elements there are to get the latest row
		"""

		gridData = self.service_sheet.spreadsheets().get(
		spreadsheetId = sheetID, includeGridData = True).execute()

		sheets = gridData.get('sheets', '')
		list_sheets = [sheets[x].get("properties", {}).get("title", {})
			   for x in range(0, len(sheets))]

		index_sheet = list_sheets.index(sheetName)

		try:
			# columnNumber = gridData['sheets'][
			# index_sheet]['properties']['gridProperties']['columnCount']

			# Same a rows, count only non empty cols
			columnNumber = len(gridData['sheets'][
			index_sheet]['data'][0]['rowData'][0]['values'])
		except:
			columnNumber = 1

		return columnNumber

	def getRowAndColumns(self, sheetID, sheetName):
		"""
		The option includeGridData = True in the get elements return a dictionary
		with the row sort_values
		We can count how many elements there are to get the latest row
		"""

		gridData = self.service_sheet.spreadsheets().get(
		spreadsheetId = sheetID, includeGridData = True).execute()

		sheets = gridData.get('sheets', '')
		list_sheets = [sheets[x].get("properties", {}).get("title", {})
			   for x in range(0, len(sheets))]

		index_sheet = list_sheets.index(sheetName)

		try:
			columnNumber = len(gridData['sheets'][
			index_sheet]['data'][0]['rowData'][0]['values'])

			latestRow = len(gridData['sheets'][index_sheet]['data'][0]['rowData'])
		except:
			columnNumber = 1
			latestRow = 1

		return columnNumber, latestRow

	def listSpreadsheet(self, sheetID):
		"""
		The option includeGridData = True in the get elements return a dictionary
		with the row sort_values
		We can count how many elements there are to get the latest row
		"""

		gridData = self.service_sheet.spreadsheets().get(
		spreadsheetId = sheetID, includeGridData = True).execute()

		sheets = gridData.get('sheets', '')

		list_sheets = [sheets[x].get("properties", {}).get("title", {})
			   for x in range(0, len(sheets))]

		return list_sheets
