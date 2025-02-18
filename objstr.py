from fastapi.responses import FileResponse, StreamingResponse
from minio import Minio
from fastapi import *
import mimetypes
from dotenv import *
import os

load_dotenv()

client = Minio(endpoint=os.getenv("MINIO_ENDPOINT"), access_key=os.getenv("MINIO_ACCESS_KEY"), secret_key=os.getenv("MINIO_SECRET_KEY"), secure=False)

def upload_document_path(bucket_name:str, object_name:str, file_name, content_type:str):
    return client.fput_object(bucket_name, object_name, file_name, content_type)

async def upload_document(bucket_name:str, file:UploadFile):
    file_content = await file.read()
    return client.put_object(bucket_name, file.filename, file.file, length=file_content, content_type=file.content_type)

def get_document(bucket_name: str, object_name: str):
    # Get the file stream from MinIO
    response = client.get_object(bucket_name, object_name)

    # Guess MIME type based on file extension
    content_type, _ = mimetypes.guess_type(object_name)
    if content_type is None:
        content_type = "application/octet-stream"  # Default for unknown file types

    # Stream the file directly to the client
    return StreamingResponse(response, media_type=content_type) 

def delete_document(bucket_name:str, object_name):
    return client.remove_object(bucket_name, object_name)


