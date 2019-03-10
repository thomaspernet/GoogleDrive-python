

```
#!pip install git+git://github.com/thomaspernet/GoogleDrive-python
#!pip install --upgrade git+git://github.com/thomaspernet/GoogleDrive-python
```

# Connect service


```
from GoogleDrivePy.google_authentification import connect_service
```


```
pathcredential = '/content/gdrive/My Drive/Projects/Google_code_n_Oauth/Client_Oauth/Google_auth/'
scopes = ['https://www.googleapis.com/auth/documents.readonly',
            'https://www.googleapis.com/auth/drive']
cs = connect_service.connect_service(pathcredential, scopes)
```


```
cs.get_auth()
```

    Drive already mounted at /content/gdrive; to attempt to forcibly remount, call drive.mount("/content/gdrive", force_remount=True).



```
service = cs.get_service()
```

    Service Google Drive and Google Docs are now connected. 
    Service Google Drive is stored as <googleapiclient.discovery.Resource object at 0x7fa748bbf240> and accessible with "drive" 
    Service Google Doc is stored as <googleapiclient.discovery.Resource object at 0x7fa748b1ef60>and accessible with "doc"


# Google Drive

## Create test file


```
f = open("test.txt","w+")
for i in range(10):
     f.write("This is line %d\r\n" % (i+1))
f.close() 
```


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
    test.csv
    test.txt
    sample_data


## Upload to Drive


```
from GoogleDrivePy.google_drive import connect_drive
```


```
cdr = connect_drive.connect_drive(service)
```


```
mime_type = "text/plain"
name = "test.txt"
```

    File ID: 10a2atdnggjT75ZwNYFRlmgHPtdeiDJlQ





    '10a2atdnggjT75ZwNYFRlmgHPtdeiDJlQ'




```
cdr.upload_file_root(mime_type, name)
```

### Find file or folder

**Folder**


```
cdr.find_folder_id(folder_name = "Compute_quality")
```

    Found file: Compute_quality (1JlLWiJ7slc8rVjBgzjxy0aN8xt9uEYqp)





    '1JlLWiJ7slc8rVjBgzjxy0aN8xt9uEYqp'




```
cdr.find_folder_id(folder_name = "Compute_quality1")
```

    File Compute_quality1 not found


**File**


```
cdr.find_file_id(file_name = "Quality_HS_12.png")
```

    Found file: Quality_HS_12.png (1nnN6riJcRK9c-4jRt6NB__xsFR7GLEu4)





    '1nnN6riJcRK9c-4jRt6NB__xsFR7GLEu4'




```
file_id = cdr.find_file_id(file_name = "test1.txt")
```

    File test1.txt not found


## Move file to folder


```
cdr.move_file(file_name = 'test.txt', folder_name = 'Compute_quality')
```

    Found file: Compute_quality (1JlLWiJ7slc8rVjBgzjxy0aN8xt9uEYqp)
    Found file: test.txt (10a2atdnggjT75ZwNYFRlmgHPtdeiDJlQ)
    File test.txt move to Compute_quality


## Add image to Google doc


```
cdr.add_image_to_doc(image_name = 'Quality_HS_12.png', doc_name = 'document_test')
```

    Image added to document_test


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

