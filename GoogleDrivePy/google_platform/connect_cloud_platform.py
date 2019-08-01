from google.cloud import storage, bigquery

class connect_console:
	def __init__(self, project = None, service_account = None, colab = False):
		self.project = project
		self.service_account = service_account
		self.colab = colab

	def upload_blob(self, bucket_name, destination_blob_name, source_file_name):
		"""
		Uploads a file to the bucket.
		bucket_name: Name of the bucket
		destination_blob_name: Name of the subfolder in the bucket;
		The function save with source file name
		source_file_name: Path source file locally.
		If blob not found, then it is created automatically with blob name
		"""
		destination = str(destination_blob_name) + "/" + str(source_file_name)
		if self.colab:
			storage_client = storage.Client(project = self.project)
		else:
			storage_client = self.service_account['Storage_account']
		try:
			bucket = storage_client.get_bucket(bucket_name)
			blob = bucket.blob(destination)
			blob.upload_from_filename(source_file_name)
			print('File {} uploaded to {}.'.format(
				   source_file_name,
				   destination_blob_name))
		except:
			print("Not found: bucket name {}".format(bucket_name))

	def delete_blob(self, bucket_name, destination_blob_name):
		"""Deletes a blob from the bucket."""
		if self.colab:
			storage_client = storage.Client(project = self.project)
		else:
			storage_client = self.service_account['Storage_account']
		try:
			bucket = storage_client.get_bucket(bucket_name)
			blob = bucket.blob(destination_blob_name)
			blob.delete()
			print('Blob {} deleted.'.format(destination_blob_name))
		except:
			print("Not found: bucket name {}".format(destination_blob_name))

	def download_blob(self, bucket_name, destination_blob_name,
	 source_file_name):
		"""
		Download a file to the bucket.
		bucket_name: Name of the bucket
		destination_blob_name: Name of the subfolder in the bucket;
		The function save with source file name
		source_file_name: Path source file locally.

		"""
		origin = str(destination_blob_name) + "/" + str(source_file_name)
		if self.colab:
			storage_client = storage.Client(project = self.project)
		else:
			storage_client = self.service_account['Storage_account']
		try:
			bucket = storage_client.get_bucket(bucket_name)
			blob = bucket.blob(origin)
			blob.download_to_filename(source_file_name)
			print('File {} uploaded locally'.format(
				   origin
				   ))
		except:
			print("Not found: bucket name {}".format(bucket_name))

	def move_to_bq_autodetect(self, dataset_name, name_table, bucket_gcs):
		"""
		The function upload a csv file from Google Cloud Storage to
		Google BigQuery
		dataset_name: Name of the dataset
		bucket_uri: Folder and subfolder from GCS
		name_table: Name of the table created in the dataset
		"""
		if self.colab:
			client = bigquery.Client(project = self.project)
		else:
			client = self.service_account['bigquery_account']
		dataset_ref = client.dataset(dataset_name)
		job_config = bigquery.LoadJobConfig()
		job_config.autodetect = True
		job_config.skip_leading_rows = 1

  # The source format defaults to CSV, so the line below is optional.

		bucket_uri = 'gs://' + str(bucket_gcs)
		job_config.source_format = bigquery.SourceFormat.CSV
		uri = bucket_uri
		load_job = client.load_table_from_uri(
			uri,
			dataset_ref.table(name_table),
		job_config = job_config)  # API request
		print('Starting job {}'.format(load_job.job_id))
		try:
			load_job.result()  # Waits for table load to complete.
			print('Finished job {}'.format(load_job.job_id))
		except:
			print("Not found: URI {}".format(bucket_uri))


	def upload_bq_predefined_sql(self, dataset_name, name_table,
		bucket_gcs, sql_schema):
		"""
		The function upload a csv file from Google Cloud Storage to
		Google BigQuery with a predefinel SQL format
		dataset_name: Name of the dataset
		bucket_uri: Folder and subfolder from GCS
		name_table: Name of the table created in the dataset
		sql_schema: list of predefined SQL schema
		"""

		if self.colab:
			client = bigquery.Client(project = self.project)
		else:
			client = self.service_account['bigquery_account']
		dataset_ref = client.dataset(dataset_name)
		job_config = bigquery.LoadJobConfig()
		list_bq_schema = []
		for sql in sql_schema:
			list_bq_schema.append(bigquery.SchemaField(sql[0], sql[1]))
		#job_config.autodetect = True
		job_config.schema = list_bq_schema
		job_config.skip_leading_rows = 1
		# The source format defaults to CSV, so the line below is optional.
		job_config.source_format = bigquery.SourceFormat.CSV
		bucket_uri = 'gs://' + str(bucket_gcs)
		load_job = client.load_table_from_uri(
			bucket_uri,
			dataset_ref.table(name_table),
		job_config = job_config)  # API request
		try:
			load_job.result()  # Waits for table load to complete.
			print('Finished job {}'.format(load_job.job_id))
		except:
			print("Not found: URI {}".format(bucket_uri))  # Waits for table load to co

	def upload_data_from_bigquery(self, query, location):
		"""
		Load data from bigquery into a dataframe
		"""

		if self.colab:
			client = bigquery.Client(project = self.project)
		else:
			client = self.service_account['bigquery_account']

		df_bigquery = client.query(query, location="US").to_dataframe()

		return df_bigquery

	def delete_table(self, dataset_name, name_table):
		"""Deletes a table from the dataset."""
		  # from google.cloud import bigquery
		if self.colab:
			client = bigquery.Client(project = self.project)
		else:
			client = self.service_account['bigquery_account']
		# Delete table
		table_ref = client.dataset(dataset_name).table(name_table)
		try:
			client.delete_table(table_ref)  # API request
			print('Table {}:{} deleted.'.format(dataset_name, name_table))
		except:
			print("Not found: dataset/table {}, {}".format(dataset_name,
			 name_table))

	def list_dataset(self):
		"""
		list all datasets
		"""

		if self.colab:
			client = bigquery.Client(project = self.project)
		else:
			client = self.service_account['bigquery_account']

		datasets = list(client.list_datasets())
		project = client.project
		list_datasets = []
		if datasets:
			for dataset in datasets:  # API request(s)
				list_datasets.append(dataset.dataset_id)
			dic_table = {'Dataset': list_datasets}
			return dic_table
		else:
			print('{} project does not contain any datasets.'.format(project))


	def list_tables(self, dataset):
		"""
		List tables in dataset
		"""
		if self.colab:
			client = bigquery.Client(project = self.project)
		else:
			client = self.service_account['bigquery_account']

		tables = list(client.list_tables(dataset))
		project = client.project
		list_table = []
		if tables:
			for table in tables:  # API request(s)
				list_table.append(table.table_id)
			dic_table = {'Dataset': dataset,
				'tables': list_table}
			return dic_table
		else:
			print('{} project does not contain any table.'.format(project))


	def list_bucket(self):
		"""
		List tables in dataset
		"""
		if self.colab:
			client = storage.Client(project = self.project)
		else:
			client = self.service_account['Storage_account']

		buckets = client.list_buckets()
		list_buckets = []
		if buckets:
			for bucket in buckets:  # API request(s)
				list_buckets.append(bucket.name)
			dic_table = {'Bucket': list_buckets}
			return dic_table
		else:
			print('Project does not contain any bucket.')

	def list_blob(self, bucket, prefix = None):
		"""
		List blobs in bucket
		"""
		if self.colab:
			client = storage.Client(project = self.project)
		else:
			client = self.service_account['Storage_account']

		bucket_name = client.get_bucket(bucket)
		list_blobs = []
		if bucket_name:
			for blob in bucket_name.list_blobs(prefix = prefix):  # API request(s)
				list_blobs.append(blob.name)
			dic_table = {'Bucket': bucket,
				'blob': list_blobs}
			return dic_table
		else:
			print('Bucket is empty.')
