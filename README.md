
This library proposes a straightforward data workflow between Jupyter notebook, Google Drive, and Google Cloud Platform. The library contains three modules:

- `google_authentification`: Gives authorization to access Google Drive and Google Cloud Platform
- `google_drive`: Provides the necessary operations on **Google Drive** such as creating files, moving files, add images to a **Google Docs**, add/load data to/from **Google Spreadsheet**
- `google_platform`:  Add/Load/deletes files in **Google Cloud Storage** but also **BigQuery**

Install library
```
!pip install git+git://github.com/thomaspernet/GoogleDrive-python
```

Update library
```
!pip install --upgrade git+git://github.com/thomaspernet/GoogleDrive-python
```

The motivation behinds this library is to automatize the data workflow as follow: 

![](https://github.com/thomaspernet/thomaspernet/blob/master/static/img/workflow.png)

One particular objective is to archive the summary statistics or output of explanatory data analysis in Google drive.

# Connect service module

The module `connect_service` authorizes Google to perform operations on Google Drive. To connect to Google module, you need to download a credential and a service account files with the appropriate authorization. 

The credential file gives the authorization to view, read, or write in files from Google Drive. Service account permits to perform the same operation in Google Cloud Storage and BigQuery. Note that, you can change that authorization in [GCP](https://console.cloud.google.com/) 

## Configurate authorization

There are two different files to create to give access to Google Cloud:

- credential and token
- service_account

### Credential and token


To connect to Google product, you need a credential. The only way to get this credential is to accept data consent.

Here are the steps:

1.  Go to  [this page](https://console.developers.google.com/apis/)  to create your credentials 
2.  At the top of the page, select the  **OAuth consent screen**  tab. Select an  **Email address**, enter an **App name**  if not already set, and click the  **Save**  button.
4.  Select the  **Credentials**  tab, click the  **Create credentials**  button and select  **OAuth client ID**.
5.  Select the application type  **Other**, enter the name "Google Sheets API Quickstart," and click the  **Create**  button.
6.  Click  **OK**  to dismiss the resulting dialog.
7.  Click the  file_download  (Download JSON) button to the right of the client ID.
8.  Move this file to your working directory and rename it  `credential.json.`

The first time you use the library, you will use `credential.json` to generate a unique token through the Google authentification windows. During the authentification, Google prompts warning information the app is not verified. Click advanced and proceed. The app's name is the one you defined previously. If the authentification is a success, you should see `The authentication flow has completed, you may close this window.`

After Google authenticates you, you'll get a new file named `token.pickle` in the current directory. You need this token every time to connect to the library. Store it in a safe but accessible place. 

### Service account

To create a service account, go to the IAM tab in the [iam-admin](https://console.cloud.google.com/iam-admin) panel. 

1. Click **Add**
2. Add three roles:
	3. BigQuery Data Viewer
	4. BigQuery Job User
	5. Viewer
3. Go to **service account**
4. Select the user you've just created
5. Look the three dots at the right side of the windows and click **Create**
6. Select **JSON** and click **Create**

The service account JSON file is downloaded. You need this file each time you want to connect to GCS. The filename looks like `valid-pagoda-XXXXXX.json`

It will give enough flexibility to read data in GCS and BigQuery. You can tailor-made the role for each user. For instance, allow only certain users to access some data.

## Connect to Google drive/GCP

Now that you have downloaded the authorization, you can create the connection. The module `connect_service_local` provides a quick way to connect with Google Drive and Google Cloud platform.

- To connect to Google Drive, use the function  `get_service`:
- To connect to GCP, use the function `get_storage_client`


```
from GoogleDrivePy.google_authentification import connect_service_local
```

You need to initialize the connection with `connect_service_local`. There are three arguments:

- `path_credential:` Path to the credential and the token. Required to connect to Google Drive
- `path_service_account`: Path to the service account file. Needed to connect to GCP
- `scope`: Required to set up the first connection, i.e., download the token

### Google Drive

During your first first connection, define the path to the credential and the scope. 
```
#pathcredential = '/content/gdrive/My Drive/PATH TO CREDENTIAL/'
pathcredential = '/PATH TO CREDENTIAL/'
scopes = ['https://www.googleapis.com/auth/documents.readonly',
            'https://www.googleapis.com/auth/drive', 
         'https://www.googleapis.com/auth/spreadsheets.readonly']
```

To initialize the connection to Google Drive only. Use scope only if the token is not available.

```
cs = connect_service_local.connect_service_local(path_credential =pathcredential,
                                                 scope = scopes)
```

The function  `get_service()` returns the Service Google Drive,  Service Google Doc., and Service Google spreadsheet. 

```
service_drive = cs.get_service()
```

### GCS

To initialize the connection to GCS only. Note that the path should include the filename. The filename looks like `valid-pagoda-XXXXXX.json`

```
path_serviceaccount = '/PATH TO CREDENTIAL/FILENAME.json'
cs = connect_service_local.connect_service_local(path_service_account =path_serviceaccount)
```

The function  `get_storage_client()` returns the Service Google Cloud Storage and Google BigQuery.

```
service_gcp = cs.get_storage_client()
```
You can create a connection for both service:

```
### Scope is not required since the token is already created
cs = connect_service_local.connect_service_local(path_credential =pathcredential,
                                                 path_service_account =path_serviceaccount)
```

Then use `get_service` and `get_storage_client` to connect to the different service.

There is a module `connect_service_colab` to connect to Google Drive or GCP from Google Colab.

# Quickstart 

## Google Drive Service

After the connection with Google Drive is done, you can use the module `connect_drive` to perform the following operation:

- Google Drive:
	- Upload file: `upload_file_root`
	- Find folder ID: `find_folder_id`
	- Find file ID: `find_file_id`
	- Move file: `move_file`
- Google Doc
	- Find/create doc: `access_google_doc`
	- Add image to doc: `add_image_to_doc`
	- Add bullet point: `add_bullet_to_doc`
- Google Spreadsheet
	- Add data: `add_data_to_spreadsheet`
	- Upload data: `upload_data_from_spreadsheet`
	- Find latest row: `getLatestRow`
	- Find number columns: `getColumnNumber`
	- Both columns and rows: `getRowAndColumns`


All functions are in the `connect_drive` module
```
from GoogleDrivePy.google_drive import connect_drive
```

To use one of the functions above, you need to use the authorization defined with `get_service` 

```
gdr = connect_drive.connect_drive(service_drive)
```

### Google Drive

1. Upload file

```
f = open("test.txt","w+")
for i in range(10):
     f.write("This is line %d\r\n" % (i+1))
f.close() 
```

Check if the file is created locally.

```
from __future__ import print_function
import os
 
path = '.'
 
files = os.listdir(path)
for name in files:
    print(name)
```


To upload the file in the root of Google Drive, we can use the function `upload_file_root`. The function has two arguments.
- `mime_type`: You can use MIME types to filter query results or have your app listed in the Chrome Web Store list of apps that can open specific file types. list [mime-types](https://developers.google.com/drive/api/v3/mime-types)
- `file_name`: Name of the file

It returns the ID of the file newly created.

```
mime_type = "text/plain"
file_name = "test.txt"
gdr.upload_file_root(mime_type, file_name)
```

2.  Find Folder

**Folder**


```
gdr.find_folder_id(folder_name = "FOLDER_NAME")
```


```
gdr.find_folder_id(folder_name = "FOLDER_NAME")
```

3.  Find file


```
gdr.find_file_id(file_name = "FILE_NAME")
```

```
file_id = gdr.find_file_id(file_name = "FILE_NAME")
```



4. Move the file to a folder


```
gdr.move_file(file_name = 'FILE_NAME, folder_name = 'FOLDER_NAME')
```


##  Google doc

1. Find doc

```
gdr.access_google_doc(doc_name = 'FILE_NAME')
```

2. Add image to doc

This function adds an image to google docs.

```
gdr.add_image_to_doc(image_name = 'FILE_NAME', doc_name = 'DOC_NAME')
```
    

2. Add bullet point


```
gdr.add_bullet_to_doc(doc_name = 'document_test',
 name_bullet = 'This is a long test')
```

## Google Spreadsheet

1. Add data

Currently, you need to add the range into a spreadsheet to write the data. In a future version, the function will automatically detect where to paste the data. `rangeData` includes the header. If your data has 99 rows, then you need to add 100 rows to the range. You need to write the sheet name as well. Example `Sheet1!A1:E10`

You need to define the header as a list. It is quickly done with  `list(dataframe_name)`

```
gdr.add_data_to_spreadsheet(data, sheetID, sheetName, rangeData,
	 headers)
```
2. Upload data

Load data. If `to_dataframe = False`, it returns a JSON file else a Pandas dataframe
```
upload_data_from_spreadsheet(sheetID, sheetName,
	 to_dataframe = False)
```
3. Find latest row
```
getLatestRow(sheetID, sheetName)
```
4. Find number columns
```
getColumnNumber(sheetID, sheetName)
```
5. Find both latest row and number columns
```
getRowAndColumns(sheetID, sheetName)
```


# Google Cloud Platform

Google Cloud platform functions are available in the module `connect_cloud_platform` and accessible from `get_storage_client`

- Google Cloud Storage
	- Upload file to a bucket: `upload_blob`
	- Delete file from bucket: `delete_blob`
	- download file from bucket: `download_blob`
	- List buckets: `list_bucket`
	- list all files in a bucket: `list_blob`
- Big Query
	- Add data to table automatic format detection: `move_to_bq_autodetect`
	- Add data to table predefined SQL: `upload_bq_predefined_sql`
	- Load data: `upload_data_from_bigquery`
	- delete table: `delete_table`
	- list dataset: `list_dataset`
	- list table in dataset: `list_tables`

```
from GoogleDrivePy.google_platform import connect_cloud_platform
```

To access the GCP, you need explicitly tells which to use and add the authorization

```
project = 'PROJECT NAME'
gcp = connect_cloud_platform.connect_console(project = project, 
                                             service_account = service_gcp)
```

Note, this service is also accessible from Colab. If you use Colab, add `colab = True` 

```
gcp = connect_cloud_platform.connect_console(project = project, 
                                             service_account = service_gcp,
                                             colab = True)
```


## Google Storage

To try the function, create a pandas dataframe
```
import pandas as pd
x = pd.Series([1,2, 3, 4], name = 'x')
x.to_csv("test.csv")
```

Go to GCS, create a bucket name `machine_learning_teaching` and a subfolder `library_test`


1. Uploads a file to a bucket.

To upload files to GCS, you need to add more privilege to the user. Go to [iam-admin](https://console.cloud.google.com/iam-admin), select the user and add new role: **Storage Admin**

Note that, we didn't add the error yet if the user does not have the privilege to write to a bucket. If the user gets this message, `Not found: bucket name BUCKET_NAME` it's mostly because of privilege restriction. 

```
upload_blob(bucket_name, destination_blob_name, source_file_name)
```

- `bucket_name`: Name of the bucket
- `destination_blob_name`: Name of the subfolder in the bucket;
The function save with source file name
- `source_file_name`: Path source file locally.
If blob not found, then it is created automatically with blob name.

```
bucket_name = 'machine_learning_teaching'
destination_blob_name = 'test_library'
source_file_name = 'test.csv'
gcp.upload_blob(bucket_name, destination_blob_name,  source_file_name)
```

2. List bucket
```
gcp.list_bucket()
```

3. List files in bucket
```
gcp.list_blob(bucket = 'machine_learning_teaching')
```

4. Download file

```
gcp.download_blob(bucket_name = 'machine_learning_teaching',
                  destination_blob_name = 'test_library',
                  source_file_name = 'test.csv')
```
5. Delete file

Only the user with full control of GCS  storage can delete files.

```
delete_blob(bucket_name, destination_blob_name)
```
## Big Query

1. Add file to a dataset

You need to create a dataset in BigQuery. You can add a table to the dataset.

There is two way to transfer data from GCS to Bigquery. 

- `move_to_bq_autodetect`:  Auto detect format of the variables
- `upload_bq_predefined_sql`:  User predefined format of the variables using SQL

Once again, make sure the user has the right to create a table in the dataset. Go to [iam-admin](https://console.cloud.google.com/iam-admin) and change the role **BigQuery Data Viewer** to **BigQuery Admin**

### Auto detect

```
move_to_bq_autodetect(dataset_name, name_table, bucket_gcs)
```


The function upload a CSV file from Google Cloud Storage to Google BigQuery
- dataset_name: Name of the dataset
- - name_table: Name of the table created in the dataset
- bucket_gcs: Folder and subfolder from GCS

```
dataset_name = 'tuto'
name_table = 'test'
bucket_gcs = 'machine_learning_teaching/test_library/test.csv'
gcp.move_to_bq_autodetect(dataset_name, name_table, bucket_gcs)
```

### Predefined SQL

We saved the data frame with

```
SQL_schema = [
    ['A', 'INTEGER'],
    ['B', 'INTEGER'],
    ['C', 'INTEGER'],
    ['D', 'INTEGER']
]
gcp.upload_bq_predefined_sql(dataset_name='library',
                             name_table='test_1',
                             bucket_gcs='machine_learning_teaching/test_library/test.csv',
                             sql_schema=SQL_schema)
```

Other formats are available:

- `STRING`
- `FLOAT`


Make sure to choose the right format, and the data does not have an issue. Otherwise, the uploading will fail.

3. Load data from BigQuery

- Each SQL line should be a wrap by quotes and with whitespace before the last quote
- The location must match that of the dataset(s) referenced in the query.

```
query = (
  "SELECT * "
    "FROM library.test_1 "

)
gcp.upload_data_from_bigquery(query = query, location = 'US')
```

4. List dataset

```
gcp.list_dataset()
```

5. List tables

```
gcp.list_tables(dataset = 'library')
```

6. Delete table

```
gcp.delete_table(dataset_name = 'library', name_table = 'test')
```
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTAxOTEyMjkxNiwtNjcwOTI0NjIyLDEwMT
kxMjI5MTYsLTE4MzYxMzMyMjYsMjg4NjA1MzAyLC0zMTIzNDgz
MzksMTMxMDg0MTAyNiw3MzAxOTE5MDksLTIwOTYyMzE2MDAsND
k0NzkzMjMyLC0xNTIyMjk0MTQ2LDI5Mjg3MDI2NCwxMDc2MjQ1
OSwyMTcwMzU4NzAsLTE2ODQ4ODEwMDcsLTEwMTg1MjQ1MTMsLT
U2MDIwNTk1Myw3Mzk0NzcxMSwxMjk0MjA5MzI5XX0=
-->