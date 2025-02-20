from requests import Session
from database import SessionLocal
from objstr import *
from fastapi import FastAPI, File, UploadFile
import schemas
from fastapi.middleware.cors import CORSMiddleware
import crud


# Declare FastAPI
app = FastAPI()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
        
@app.get("/") # Choose CRUD Method - GET, POST, DELETE, PUT, PATCH
async def root(): # root -> Description of your method
    return {"message":"Hello World"} # Output

@app.get("/get/hospital")
def get_hospital_raja():
    return {"message": "Get Hospital"}

@app.post("/create/hospital")
def create_hospital():
    return {"message": "Create Hospital"}

@app.delete("/delete/hospital")
def delete_hospital():
    return {"message":"Delete Hospital"}

@app.put("/put/hospital") # Whole Update
def update_hospital():
    return {"message": "Update Hospital"}

@app.patch("/patch/hospital") # Satu Update
def patch_hospital():
    return {"message": "Update Hospital"}


# @app.post('/user/post', response_model=schemas.UserBase, tags=["Users"])
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

@app.post('/userrole/post', response_model=schemas.UserRoleBase, tags=["User"])
def create_user_role(userrole: schemas.UserRoleCreate, db: Session = Depends(get_db)):
    return crud.create_user_role(db,userrole)

@app.get("/userrole/get", response_model=schemas.UserRoleBase, tags=["User"])
def get_user_role_by_id(id:int, db: Session = Depends(get_db)):
    return crud.get_user_role_by_id(db,id)








# Minio File
@app.post("/uploadfile", tags=["File"])
def upload_file(file: UploadFile):
    upload_document("documents", file)    
    return {"message":"Upload Successful!"}

@app.get("/getfile", tags=["File"])
def get_file(object_name:str):
    return get_document("documents", object_name)

@app.delete("/deletefile", tags=["File"])
def delete_file(object_name:str):
    return delete_document("documents", object_name)