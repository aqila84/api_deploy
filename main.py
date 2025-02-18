from objstr import *
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.post("/uploadfile")
def upload_file(file: UploadFile):
    upload_document("documents", file)    
    return {"message":"Upload Successful!"}

@app.get("/getfile")
def get_file(object_name:str):
    return get_document("documents", object_name)



@app.get("/test")
async def test():
    return {"gitu"}