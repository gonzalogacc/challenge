from fastapi import UploadFile
from pathlib import Path
import shutil

BASE_PATH = "/data"
BASE_PATH = "/Users/ggarcia/Documents/challenge/data"

def upload(
        upload_file: UploadFile, 
        file_name: str,
        base_path: str = BASE_PATH
    ):
    try:
        ## TODO: check volume exists
        destination = Path(base_path) / file_name
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

    finally:
        upload_file.file.close()


def get_file(
        file_name: str,
        base_path: str = BASE_PATH
    ):
    ## TODO: check volume exists
    destination = Path(base_path) / file_name
    print(destination)
    if not destination.exists():
        return None
    
    return destination.open("rb")
