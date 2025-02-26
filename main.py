from http.client import HTTPException
from requests import Session
from TTE_BE.Routes import Documents, Signature
from database import SessionLocal
from objstr import *
from fastapi import FastAPI, File, UploadFile
import schemas
from fastapi.middleware.cors import CORSMiddleware
import crud
from typing import List


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

@app.post('/userrole/post', response_model=schemas.UserRoleBase, tags=["Role"])
def create_user_role(userrole: schemas.UserRoleCreate, db: Session = Depends(get_db)):
    return crud.create_user_role(db,userrole)

@app.get("/userrole/get/{id}", response_model=schemas.UserRoleBase, tags=["Role"])
def get_user_role_by_id(id:int, db: Session = Depends(get_db)):
    return crud.get_user_role_by_id(db,id)


@app.delete("/userrole/delete",tags=["Role"])
def delete_user_role_by_name(UserRoleName:str,db:Session =Depends(get_db)):
    deleted_user = crud.delete_user_role_by_name(db,UserRoleName)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return {"message": "Role succesfully deleted"}

@app.get("/userrole/getall", tags=["Role"])
def get_user_role(db: Session = Depends(get_db)):
    return crud.get_user_role(db)

@app.put("/userrole/update", tags=["Role"])
def update_user_role_by_id(id:int, userroleupdate:schemas.UserRoleUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user_role_by_id(db, id, userroleupdate)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return updated_user
    
@app.put("/user/update", tags=["User"])
def update_user_by_name(Name:str, userupdate:schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user_by_name(db, Name, userupdate)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return updated_user

@app.patch("/user/patch/address", tags=["User"])
def update_user_address_by_name(Name:str, userupdate:schemas.UserUpdateAddress, db: Session = Depends(get_db)):
    updated_user = crud.update_user_address_by_name(db, Name, userupdate)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return updated_user


@app.delete("/user/delete", tags=["User"])
def delete_user_by_name(Name:str, db: Session = Depends(get_db)):
    crud.delete_user_by_name(db, Name)
    return {"message": "User Successfully Deleted"}

@app.post("/user/post", response_model=schemas.UserBase,tags=["User"] )
def create_user(user:schemas.UserCreate, db:Session =Depends(get_db)):
    return crud.create_user(db,user)
    # return {"message":"user has been created"}

@app.get("/user/get", tags=["User"])
def get_user_by_name(Name:str,db:Session =Depends(get_db)):
    return crud.get_user_by_name(db,Name)
    
@app.patch('/user/patch', tags=["User"])
def update_user_job_by_name(Name:str,userjob:schemas.UserUpdateJob, db:Session =Depends(get_db)):
    updated_job = crud.update_user_job_by_name(db,Name,userjob)
    if not updated_job:
        raise HTTPException(status_code=404, detail="User does not exist")
    return updated_job

#Document Endpoint

app.include_router(Documents.router, tags=["Document"])


#Signature Endpoint

app.include_router(Signature.router, tags=["Signature"])





# # Minio File
# @app.post("/uploadfile", tags=["File"])
# def upload_file(file: UploadFile):
#     upload_document("documents", file)    
#     return {"message":"Upload Successful!"}

# @app.get("/getfile", tags=["File"])
# def get_file(object_name:str):
#     return get_document("documents", object_name)

# @app.delete("/deletefile", tags=["File"])
# def delete_file(object_name:str):
#     return delete_document("documents", object_name)

