from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi import File, UploadFile
from sqlalchemy.orm import Session, Query

from utils.depends import get_session
from controllers.file_controllers import create_file, stream_file, files_from_tags
from controllers.tag_controllers import process_name_tags, get_or_create_tag

from models.models import Base
from models.db_engine import engine
Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/files/{dataset_name}")
def POST_upload_files(
    dataset_name: str,
    upload_file: UploadFile = File(...),
    ses: Session = Depends(get_session)
        ):
    """Upload files to the server
    """
    #try:
    tags = process_name_tags(upload_file.filename, ses)
    dataset_tag = get_or_create_tag(dataset_name, ses)
    tags.append(dataset_tag)
    file = create_file(upload_file, tags, ses, storage_driver="local")
    return {"message": "File uploaded successfully"}

    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=str(e))


@app.post("/filter/")
def POST_list_files_tags(
        q: list[str],
        ses: Session = Depends(get_session)
    ):
    """ Returns a list of files matching this tag
    """
    #try:
    print(f"tagnames: {q}")
    files = files_from_tags(q, ses)
    return dict(filter_tags=q, files=files, count=len(files))

    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=str(e))

@app.get("/file/{file_name}")
def GET_list_files(
        file_name: str,
        ses: Session = Depends(get_session)
    ) -> StreamingResponse:
    """List files on the server
    """
    # Download
    return stream_file(ses, filename=file_name)
