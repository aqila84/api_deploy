from fastapi import FastAPI, File, UploadFile, Request, Depends, Response, APIRouter
import crud
import schemas
from requests import Session
from database import get_db
from http.client import HTTPException
from typing import List
from database import get_db

router = APIRouter()

#Staff
@router.post("/staff/post", response_model=schemas.StaffResponse, tags=["Staff"])
def create_staff(staff:schemas.StaffCreate, db: Session = Depends(get_db)):
    return crud.create_staff(db, staff)

@router.get("/staff/get/{Name}", tags=["Staff"])
def get_staff_by_name(Name:str, db: Session = Depends(get_db)):
    staff = crud.get_staff_by_name(db, Name)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff

@router.put("/staff/update/{Name}", tags=["Staff"])
def update_staff_by_name(Name:str, staffupdate:schemas.StaffUpdate, db: Session = Depends(get_db)):
    updated_staff = crud.update_staff_by_name(db, Name, staffupdate)
    if not updated_staff:
        raise HTTPException(status_code=404, detail="Staff does not exist")
    return updated_staff

@router.delete("/staff/delete/{Name}", tags=["Staff"])
def delete_staff_by_name(Name:str, db: Session = Depends(get_db)):
    crud.delete_staff_by_name(db, Name)
    deleted = crud.delete_staff_by_name(db, Name)
    if not deleted:
        raise HTTPException(status_code=404, detail="Staff not found")
    return {"message": "Staff Successfully Deleted"}