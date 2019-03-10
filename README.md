
This library proposes to define a very simple data workflow between Google Colab, Google Drive and Google Cloud Platform. The library contains three modules:

- `google_authentification`: Gives authorization to access Google Drive and Google Cloud Platform through Google Colab
- `google_drive`: Provides the basic operations on Google Drive such as creating files, moving files, add images to a Google Docs
- `google_platform`: Provides a Workflow to add/deletes files in Google Cloud Storage but also from GCS to BigQuery

```
#!pip install git+git://github.com/thomaspernet/GoogleDrive-python
#!pip install --upgrade git+git://github.com/thomaspernet/GoogleDrive-python
```

The motivation behinds this library is to automatize the data workflow as follow: 

![](https://github.com/thomaspernet/thomaspernet/blob/master/static/img/workflow.png)

One particular objective is to archive the summary statistics or output of explanatory data analysis in Google drive.

# Connect service module

The module `connect_service` authorizes Google to perform operation on Google Drive. Note that, the primary purposes is to use Google Colab, and run everything on the cloud. To access the credential, the module mounts Google Drive inside Google Colab. 

```
from GoogleDrivePy.google_authentification import connect_service
```

So far, the module gives access to the Drive and Google Docs.

```
pathcredential = '/content/gdrive/My Drive/PATH TO CREDENTIAL/'
scopes = ['https://www.googleapis.com/auth/documents.readonly',
            'https://www.googleapis.com/auth/drive']
cs = connect_service.connect_service(pathcredential, scopes)
```

The function below mounts Google Drive in Google Colab and gives access to the Cloud SDK (ie. Big Query in our case)

```
cs.get_auth()
```

The function  `get_service()` returns the Service Google Drive and the Service Google Doc. 

```
service = cs.get_service()
```

    Service Google Drive and Google Docs are now connected. 
    Service Google Drive is stored as <googleapiclient.discovery.Resource object at 0x7fa748bbf240> and accessible with "drive" 
    Service Google Doc is stored as <googleapiclient.discovery.Resource object at 0x7fa748b1ef60>and accessible with "doc"


# Quickstart 

## Create a text file in Google Colab

Open Google Colab and write a random text file

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

    .config
    gdrive
    adc.json
    test.txt
    sample_data

## Google Drive module

## Upload to Drive

```
from GoogleDrivePy.google_drive import connect_drive
```

To upload the file in the root of Google Drive, we can use the function `upload_file_root`. The function has two arguments.
- `mime_type`: You can use MIME types to filter query results or have your app listed in the Chrome Web Store list of apps that can open specific file types. list https://stackoverflow.com/questions/11894772/google-drive-mime-types-listing
- file_name: Name of the file

It returns the ID of the file newly created.

```
cdr = connect_drive.connect_drive(service)
```

```
mime_type = "text/plain"
name = "test.txt"
```

```
cdr.upload_file_root(mime_type, file_name)
```

### Find file or folder

**Folder**


```
cdr.find_folder_id(folder_name = "FOLDER_NAME")
```


```
cdr.find_folder_id(folder_name = "FOLDER_NAME")
```

**File**


```
cdr.find_file_id(file_name = "FILE_NAME")
```

```
file_id = cdr.find_file_id(file_name = "FILE_NAME")
```



## Move file to folder


```
cdr.move_file(file_name = 'FILE_NAME, folder_name = 'FOLDER_NAME')
```


## Add image to Google doc

This function adds an image to a google docs

```
cdr.add_image_to_doc(image_name = 'FILE_NAME', doc_name = 'DOC_NAME')
```
    
Example output

![](https://github.com/thomaspernet/thomaspernet/blob/master/static/img/example_append.png)width=30%}


## Add bullet point


```
cdr.add_bullet_to_doc(doc_name = 'document_test', name_bullet = 'This is a long test')
```

    Bullet point added to document_test


# Google Cloud

Before to run the function in google_console module, it is mandatory to run `get_auth()` from authentification module. If not, the module cannot upload the credential

## Google Storage


```
import pandas as pd
x = pd.Series([1,2, 3, 4], name = 'x')
x.to_csv("test.csv")
```


```
files = os.listdir(path)
for name in files:
    print(name)
```

    .config
    gdrive
    adc.json
    test.csv
    test.txt
    sample_data


## Import file


```
from GoogleDrivePy.google_console import connect_cloud_platform
```


```
ccp = connect_cloud_platform.connect_console(project = 'valid-pagoda-132423')
```

Uploads a file to the bucket.
- bucket_name: Name of the bucket
- destination_blob_name: Name of the subfolder in the bucket;
The function save with source file name
- source_file_name: Path source file locally.
If blob not found, then it is created automatically with blob name

```
bucket_name = 'machine_learning_teaching'
destination_blob_name = 'test_library'
source_file_name = 'test.csv'
ccp.upload_blob(bucket_name, destination_blob_name,  source_file_name)
```

    File test.csv uploaded to test_library.


## Try if not exist


```
bucket_name = 'machine_learning_teaching_1'
destination_blob_name = 'test_library'
source_file_name = 'test.csv'
ccp.upload_blob(bucket_name, destination_blob_name,  source_file_name)
```

    Not found: URI test_library/test.csv


## Big Query

The function upload a csv file from Google Cloud Storage to Google BigQuery
- dataset_name: Name of the dataset
- bucket_uri: Folder and subfolder from GCS
- name_table: Name of the table created in the dataset

```
dataset_name = 'tuto'
name_table = 'test'
bucket_gcs = 'machine_learning_teaching/test_library/test.csv'
```


```
ccp.move_to_bq_autodetect(dataset_name, name_table, bucket_gcs)
```

    Starting job c8fc839b-5665-490e-945b-ec9ad64b9a23
    Finished job c8fc839b-5665-490e-945b-ec9ad64b9a23


## Test if not found


```
bucket_gcs = 'machine_learning_teaching/Quality/test.csv'
```


```
ccp.move_to_bq_autodetect(dataset_name, name_table, bucket_gcs)
```

    Starting job d8a4b9ec-af29-4e38-90d4-d1b9c42b1521
    Not found: URI gs://machine_learning_teaching/Quality/test.csv


## Delete files from GCS & Big Query


```
bucket_name = 'machine_learning_teaching'
destination_blob_name = 'test_library/test.csv'
ccp.delete_blob(bucket_name, destination_blob_name)
```

    Blob test_library/test.csv deleted.



```
dataset_name = 'tuto'
name_table = 'test'
ccp.delete_dataset(dataset_name, name_table)
```

    Table tuto:test deleted.

