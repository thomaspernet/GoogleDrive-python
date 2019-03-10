from google.cloud import storage, bigquery

class connect_console:
	def __init__(self, project):
		self.project = project

	def upload_blob(self, bucket_name, destination_blob_name, source_file_name):
		"""
		Uploads a file to the bucket.
		bucket_name: Name of the bucket
		destination_blob_name: Name of the subfolder in the bucket;
		The function save with source file name
		source_file_name: Path source file locally.
		"""
		destination = str(destination_blob_name) + "/" + str(source_file_name)
		storage_client = storage.Client(project = self.project)
		bucket = storage_client.get_bucket(bucket_name)
		blob = bucket.blob(destination)
		try:
			blob.upload_from_filename(source_file_name)
			print('File {} uploaded to {}.'.format(
				   source_file_name,
				   destination_blob_name))
		except:
			print("Not found: URI {}".format(destination))

	def delete_blob(bucket_name, destination_blob_name):
		"""Deletes a blob from the bucket."""
		storage_client = storage.Client(project = self.project)
		bucket = storage_client.get_bucket(bucket_name)
		blob = bucket.blob(destination_blob_name)
		try:
			blob.delete()
			print('Blob {} deleted.'.format(destination_blob_name))
		except:
			print("Not found: URI {}".format(destination_blob_name))

	def move_to_bq_autodetect(self, dataset_name, name_table, bucket_gcs):
		"""
		The function upload a csv file from Google Cloud Storage to
		Google BigQuery
		dataset_name: Name of the dataset
		bucket_uri: Folder and subfolder from GCS
		name_table: Name of the table created in the dataset
		"""
		client = bigquery.Client(project = self.project)
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

		client = bigquery.Client(project = self.project)
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

	def delete_dataset(self, dataset_name, name_table):
		"""Deletes a table from the dataset."""
		  # from google.cloud import bigquery
		client = bigquery.Client(project = self.project)
		# Delete table
		table_ref = client.dataset(dataset_name).table(name_table)
		try:
			client.delete_table(table_ref)  # API request
			print('Table {}:{} deleted.'.format(dataset_name, name_table))
		except:
			print("Not found: dataset/table {}, {}".format(dataset_name,
			 name_table))
