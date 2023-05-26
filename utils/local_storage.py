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
        ## check volume exists
        destination = Path(base_path) / file_name
        print(destination)
        print(file_name)
        print(upload_file)
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file, buffer)

    finally:
        upload_file.close()


