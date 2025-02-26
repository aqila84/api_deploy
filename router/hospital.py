from requests import Session
from database import SessionLocal
# from objstr import *
from fastapi import FastAPI, File, UploadFile, Request, Depends, Response
import schemas
from fastapi.middleware.cors import CORSMiddleware
import crud
from typing import List
import bcrypt

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