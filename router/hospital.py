from fastapi import FastAPI, File, UploadFile, Request, Depends, Response, APIRouter, HTTPException
import crud
import schemas
from requests import Session
from database import get_db
from typing import List
from database import get_db

router = APIRouter()

#Hospital
@router.post("/hospital/post", response_model=schemas.HospitalBase, tags=["Hospital"])
def create_hospital(hospital:schemas.HospitalCreate, db:Session = Depends(get_db)):
    return crud.create_hospital(db, hospital)

@router.get("/hospital/get/{HospitalName}", tags=["Hospital"])
def get_hospital_by_name(HospitalName:str, db: Session = Depends(get_db)):
    hospital =  crud.get_hospital_by_name(db, HospitalName)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital

@router.put("/hospital/update/{HospitalName}", tags=["Hospital"])
def update_hospital_by_name(HospitalName:str, hospitalupdate:schemas.HospitalUpdate, db: Session = Depends(get_db)):
    updated_hospital = crud.update_hospital_by_name(db, HospitalName, hospitalupdate)
    if not updated_hospital:
        raise HTTPException(status_code=404, detail="Hospital does not exist")
    return updated_hospital

@router.delete("/hospital/delete/{HospitalName}", tags=["Hospital"])
def delete_hospital_by_name(HospitalName:str, db: Session = Depends(get_db)):
    deleted = crud.delete_hospital_by_name(db, HospitalName)
    if not deleted:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return {"message": "Hospital Successfully Deleted"}

# @router.delete("/hospital/delete/{HospitalID}", tags=["Hospital"])
# def delete_hospital_by_id(HospitalID:int, db: Session = Depends(get_db)):
#     deleted = crud.delete_hospital_by_id(db, HospitalID)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Hospital not found")
#     return {"message": "Hospital Successfully Deleted"}