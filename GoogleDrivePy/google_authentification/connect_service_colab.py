from google.colab import drive
from google.colab import auth

class connect_service_colab:
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
