from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, Query
from uuid import uuid4
from utils import bucket
from utils import local_storage
from tempfile import SpooledTemporaryFile
import urllib
import os

from models.models import Files, Tags, FileTags
from utils.dotenv import load_env
load_env()

## Change this to a return value from upload function
GCP_BUCKET = "friendface-challenge2"
#GCP_BUCKET = os.f"https://storage.googleapis.com/{GCP_BUCKET}/"
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000/")

def create_file(
        file: UploadFile, 
        tags: list[str],
        ses: Session,
        storage_driver: str = "local"
        ):
    """Create a file in the database and upload the file to the storage
    """
    uuid = uuid4()
    if storage_driver == "gcp":
        print("storing gcp storage file")
        bucket.upload(file.file, str(uuid))
        service = "gcp-bucket"

    elif storage_driver == "local":
        print("storing local file")
        local_storage.upload(file, str(uuid))
        service = "local"

    else:
        raise ValueError("storage_driver must be either 'gcp' or 'local'")

    file = Files(
            name=uuid, 
            media_type=file.content_type,
            service=service,
            )
    
    ses.add(file)
    ses.commit()
    ses.refresh(file)

    for tag in tags:
        filetag = FileTags(tag_id=tag.id, file_id=file.id)
        ses.add(filetag)
    ses.commit()

    return file

def download_file(
        file: Files, 
        ses: Session
        ) -> SpooledTemporaryFile:
    """ Given a file return the spooled object
    """
    return bucket.download_file(str(file.name))


def stream_file(
        ses: Session,
        **kwargs
        ) -> SpooledTemporaryFile:
    """ Stream a file
    """
    ## 1. Get the file from the database
    #file = file_get(ses, **kwargs)
    if "filename" in kwargs:
        filename = kwargs["filename"]
        file = ses.query(Files).filter(Files.name == filename).one_or_none()
        if file is None:
            raise Exception(f"File {uuid} not found")
    else:
        ## TODO filters here
        raise Exception("uuid must be provided")
    
    if file.service == "local":
        print("storing local file")
        tmp = local_storage.get_file(file.name)
    
    elif file.service == "gcp-bucket":
        print("storing gcp storage file")
        # 2. Download the file from the bucke
        tmp = download_file(file, ses)
        if tmp is None:
            raise Exception(f"File not found in bucket")
     
    def iterfile():
        yield tmp.read()
    
    content_disposition = "attachment"
    headers={"Content-Disposition": f"{content_disposition}; filename={file.name}"}

    return StreamingResponse(
            iterfile(),
            headers=headers,
            media_type=file.media_type,
        )

def files_from_tags(
        tagnames: list[str],
        ses: Session
        ) -> Query:
    """ Given a list of tags return the files
    """
    ## get tag objects
    tags = ses.query(Tags).filter(Tags.name.in_(tagnames)).all()
    if len(tags) == 0:
        raise Exception("No tags found")

    files = []
    for tag in tags:
        print(tag.name, tag.files[0].file.name)
        files.extend([f.file.name for f in tag.files])

    ## generate download urls 
    download_urls = [urllib.parse.urljoin(BASE_URL, f"file/{filename}") for filename in files]
    return download_urls

