from os import getenv
from google.cloud.storage import Client, Blob
from google.oauth2.service_account import Credentials
from google.cloud.exceptions import GoogleCloudError
from tempfile import SpooledTemporaryFile
from os.path import isfile

GCP_CREDENTIALS_FILE = getenv('GCP_CREDENTIALS_FILE', "./challenge-387912-828b9649a280.json")
if not GCP_CREDENTIALS_FILE:
    raise Exception("GCP_CREDENTIALS_FILE environment variable not set")
print("GCP_CREDENTIALS_FILE: {}".format(GCP_CREDENTIALS_FILE))

if isfile(GCP_CREDENTIALS_FILE):
    print("GCP_CREDENTIALS_FILE exists")
    GCP_CREDENTIALS = Credentials.from_service_account_file(GCP_CREDENTIALS_FILE) 
    client = Client(credentials=GCP_CREDENTIALS)
else:
    client = Client()

GCP_BUCKET = getenv('GCP_BUCKET', "friendface-challenge2")
if not GCP_BUCKET:
    raise Exception("GCP_BUCKET environment variable not set")
print(f"GCP_BUCKET={GCP_BUCKET}")

client = client.bucket(GCP_BUCKET)

def find(filename: str) -> Blob:
    print(f"----> Finding {filename}")
    blob = client.blob(filename)
    if not blob.exists():
        raise FileNotFoundError(f"File blob {filename} not found")
    return blob

def upload(source, destination):
    try:
        print(f"Uploading {source} to {destination}")
        blob = client.blob(f"{destination}")
        result = blob.upload_from_file(source)
        return result
    except GoogleCloudError as e:
        print(e)
        return None

def download_blob(blob):
    tmp = SpooledTemporaryFile()
    blob.download_to_file(tmp)
    tmp.seek(0)
    return tmp


def download_file(filename):
    blob = find(filename)
    return download_blob(blob)

def list_objects(prefix=''):
    objects = {}
    for b in client.list_blobs(prefix=prefix):
        objects[b.id] = {
                'name': b.name,
                'crc32c': b.crc32c,
                'content_type': b.content_type,
                'metadata': b.metadata 
                }
    print(objects)

#print(list_objects())
