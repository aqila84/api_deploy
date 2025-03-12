from http.client import HTTPException
from requests import Session
from Routes import Documents, Signature
from router import hospital, log, staff, staffrole, user, userrole, transaction, coordinate, payment, auth
from database import SessionLocal,get_db
from objstr import *
from fastapi import FastAPI, File, UploadFile, Request, Depends, Response
import schemas
from fastapi.middleware.cors import CORSMiddleware
import crud
import models
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000", "http://localhost:3000"],
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

# app.include_router(role.router, tags=["User Role"])


# @app.post('/user/post', response_model=schemas.UserBase, tags=["Users"])
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

#User
app.include_router(user.router, tags=["User"])

#UserRole
app.include_router(userrole.router, tags=["Role"])

#Hospital
app.include_router(hospital.router, tags=["Hospital"])

#Staff
app.include_router(staff.router, tags=["Staff"])

#staffrole
app.include_router(staffrole.router, tags=["StaffRole"])

#log
app.include_router(log.router, tags=["Log"])

#Document Endpoint
app.include_router(Documents.router, tags=["Document"])

#Signature Endpoint
app.include_router(Signature.router, tags=["Signature"])

#transaction
app.include_router(transaction.router, tags=["Transaction"])

#payment
app.include_router(payment.router, tags=["Payment Gateway"])

#coordinate
app.include_router(coordinate.router, tags=["Coordinate"])

#auth
app.include_router(auth.router, tags=["Authentication"])


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

