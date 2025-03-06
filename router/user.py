from fastapi import FastAPI, File, UploadFile, Request, Depends, Response, APIRouter
import crud
import schemas
from requests import Session
from database import get_db
from http.client import HTTPException
from typing import List
from database import get_db

router = APIRouter()

#user
@router.post("/user/post", response_model=schemas.UserBase,tags=["User"] )
def create_user(user:schemas.UserCreate, db:Session =Depends(get_db)):
    return crud.create_user(db,user)
    # return {"message":"user has been created"}

@router.get("/user/get", response_model=List[schemas.UserBase])
def get_user(db: Session = Depends(get_db)):
    return crud.get_user(db)

@router.get("/user/get/{Name}", tags=["User"])
def get_user_by_name(Name:str,db:Session =Depends(get_db)):
    return crud.get_user_by_name(db,Name)

@router.put("/user/update/{Name}", tags=["User"])
def update_user_by_name(Name:str, userupdate:schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user_by_name(db, Name, userupdate)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return updated_user
 
# @router.patch('/user/patch/{Name}', tags=["User"])
# def update_user_job_by_name(Name:str,userjob:schemas.UserUpdateJob, db:Session =Depends(get_db)):
#     updated_job = crud.update_user_job_by_name(db,Name,userjob)
#     if not updated_job:
#         raise HTTPException(status_code=404, detail="User does not exist")
#     return updated_job

# @router.patch("/user/patch/address/{Name}", tags=["User"])
# def update_user_address_by_name(Name:str, userupdate:schemas.UserUpdateAddress, db: Session = Depends(get_db)):
#     updated_user = crud.update_user_address_by_name(db, Name, userupdate)
#     if not updated_user:
#         raise HTTPException(status_code=404, detail="User does not exist")
#     return updated_user

@router.delete("/user/delete/{Name}", tags=["User"])
def delete_user_by_name(Name:str, db: Session = Depends(get_db)):
    crud.delete_user_by_name(db, Name)
    return {"message": "User Successfully Deleted"}