from requests import Session
from database import SessionLocal
# from objstr import *
from fastapi import FastAPI, File, UploadFile, Request, Depends, Response
import schemas
from fastapi.middleware.cors import CORSMiddleware
import crud
from typing import List
import bcrypt

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

#UserRole
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

#User    
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

#Hospital
@app.post("/hospital/post", response_model=schemas.HospitalBase, tags=["Hospital"])
def create_hospital(hospital:schemas.HospitalCreate, db:Session = Depends(get_db)):
    return crud.create_hospital(db, hospital)

@app.get("/hospital/get", tags=["Hospital"])
def get_hospital_by_name(HospitalName:str, db: Session = Depends(get_db)):
    hospital =  crud.get_hospital_by_name(db, HospitalName)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital

@app.put("/hospital/update", tags=["Hospital"])
def update_hospital_by_name(HospitalName:str, hospitalupdate:schemas.HospitalUpdate, db: Session = Depends(get_db)):
    updated_hospital = crud.update_hospital_by_name(db, HospitalName, hospitalupdate)
    if not updated_hospital:
        raise HTTPException(status_code=404, detail="Hospital does not exist")
    return updated_hospital

@app.delete("/hospital/delete", tags=["Hospital"])
def delete_hospital_by_name(HospitalName:str, db: Session = Depends(get_db)):
    deleted = crud.delete_hospital_by_name(db, HospitalName)
    if not deleted:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return {"message": "Hospital Successfully Deleted"}

#Staff
@app.post("/staff/post", response_model=schemas.StaffResponse, tags=["Staff"])
def create_staff(staff:schemas.StaffCreate, db: Session = Depends(get_db)):
    return crud.create_staff(db, staff)

@app.get("/staff/get", tags=["Staff"])
def get_staff_by_name(Name:str, db: Session = Depends(get_db)):
    staff = crud.get_staff_by_name(db, Name)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff

@app.put("/staff/update", tags=["Staff"])
def update_staff_by_name(Name:str, staffupdate:schemas.StaffUpdate, db: Session = Depends(get_db)):
    updated_staff = crud.update_staff_by_name(db, Name, staffupdate)
    if not updated_staff:
        raise HTTPException(status_code=404, detail="Staff does not exist")
    return updated_staff

@app.delete("/staff/delete", tags=["Staff"])
def delete_staff_by_name(Name:str, db: Session = Depends(get_db)):
    crud.delete_staff_by_name(db, Name)
    deleted = crud.delete_staff_by_name(db, Name)
    if not deleted:
        raise HTTPException(status_code=404, detail="Staff not found")
    return {"message": "Staff Successfully Deleted"}

#staffrole
@app.post("/staffrole/post", response_model=schemas.StaffRoleResponse, tags=["StaffRole"])
def create_staff_role(staffrole: schemas.StaffRoleCreate, db: Session = Depends(get_db)):
    return crud.create_staff_role(db, staffrole)

@app.get("/staffrole/get/{StaffRoleID}", response_model=schemas.StaffRoleResponse, tags=["StaffRole"])
def get_staff_role_by_id(StaffRoleID: int, db: Session = Depends(get_db)):
    staffrole = crud.get_staff_role_by_id(db, StaffRoleID)
    if not staffrole:
        raise HTTPException(status_code=404, detail="StaffRole not found")
    return staffrole

@app.put("/staffrole/update/{StaffRoleID}", response_model=schemas.StaffRoleResponse, tags=["StaffRole"])
def update_staff_role_by_id(StaffRoleID: int, staffrole_update: schemas.StaffRoleCreate, db: Session = Depends(get_db)):
    updated_role = crud.update_staff_role_by_id(db, StaffRoleID, staffrole_update)
    if not updated_role:
        raise HTTPException(status_code=404, detail="StaffRole not found")
    return updated_role

@app.delete("/staffrole/delete", tags=["StaffRole"])
def delete_staff_role_by_name(StaffRoleName: str, db: Session = Depends(get_db)):
    deleted_role = crud.delete_staff_role_by_name(db, StaffRoleName)
    if not deleted_role:
        raise HTTPException(status_code=404, detail="StaffRole not found")
    return {"message": "StaffRole successfully deleted"}

#log
@app.post("/log/post", response_model=schemas.LogResponse, tags=["Log"])
def create_log(log: schemas.LogCreate, db: Session = Depends(get_db)):
    return crud.create_log(db, log)

@app.get("/log/getall", tags=["Log"])
def get_all_log(db: Session = Depends(get_db)):
    return crud.get_all_log(db)

@app.get("/log/get/{StaffID}", response_model=List[schemas.LogResponse], tags=["Log"])
def get_log_by_staff_id(StaffID: int, db: Session = Depends(get_db)):
    log = crud.get_log_by_staff_id(db, StaffID)
    if not log:
        raise HTTPException(status_code=404, detail="No logs found for this StaffID")
    return log

@app.delete("/log/delete", tags=["Log"])
def delete_log_by_id(LogID: int, db: Session = Depends(get_db)):
    deleted_log = crud.delete_log_by_id(db, LogID)
    if not deleted_log:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"message": "Log successfully deleted"}

# Minio File
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

