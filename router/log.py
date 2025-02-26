from fastapi import FastAPI, File, UploadFile, Request, Depends, Response, APIRouter
import crud
import schemas
from requests import Session
from database import get_db
from http.client import HTTPException
from typing import List
from database import get_db

router = APIRouter()

#log
@router.post("/log/post", response_model=schemas.LogResponse, tags=["Log"])
def create_log(log: schemas.LogCreate, db: Session = Depends(get_db)):
    return crud.create_log(db, log)

@router.get("/log/getall", tags=["Log"])
def get_all_log(db: Session = Depends(get_db)):
    return crud.get_all_log(db)

@router.get("/log/get/{StaffID}", response_model=List[schemas.LogResponse], tags=["Log"])
def get_log_by_staff_id(StaffID: int, db: Session = Depends(get_db)):
    log = crud.get_log_by_staff_id(db, StaffID)
    if not log:
        raise HTTPException(status_code=404, detail="No logs found for this StaffID")
    return log

@router.delete("/log/delete", tags=["Log"])
def delete_log_by_id(LogID: int, db: Session = Depends(get_db)):
    deleted_log = crud.delete_log_by_id(db, LogID)
    if not deleted_log:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"message": "Log successfully deleted"}