from fastapi import FastAPI, File, UploadFile, Request, Depends, Response, APIRouter
import crud
import schemas
from requests import Session
from database import get_db
from http.client import HTTPException
from typing import List
from database import get_db

router = APIRouter()

@router.post("/coordinate/post", response_model=schemas.CoordinateResponse, tags=["Coordinate"])
def create_coordinate(coordinate: schemas.CoordinateCreate, db: Session = Depends(get_db)):
    return crud.create_coordinate(db, coordinate)

@router.get("/coordinate/get", response_model=List[schemas.CoordinateBase], tags=["Coordinate"])
def get_coordinate(db: Session = Depends(get_db)):
    return crud.get_coordinate(db)

@router.get("/coordinate/get/{DocumentID}")
def get_coordinate_by_document(DocumentID: int, db: Session = Depends(get_db)):
    coordinate = crud.get_coordinate_by_document(db, DocumentID)
    if not coordinate:
         raise HTTPException(status_code=404, detail="No documentfound")
    return coordinate

@router.put("/coordinate/put/{CoordinateID}", response_model=schemas.CoordinateResponse)
def update_coordinate_by_id(CoordinateID: int, coordinate_update: schemas.CoordinateUpdate, db: Session = Depends(get_db)):
    updated_coordinate = crud.update_coordinate_by_id(db, CoordinateID, coordinate_update)
    if updated_coordinate is None:
        raise HTTPException(status_code=404, detail="Coordinate data not found")
    return updated_coordinate

@router.delete("/coordinate/delete/{CoordinateID}", tags=["Coordinate"])
def delete_coordinate_by_id(CoordinateID: int, db: Session = Depends(get_db)):
    delete_coordinate = crud.delete_coordinate_by_id(db, CoordinateID)
    if not delete_coordinate:
        raise HTTPException(status_code=404, detail="Coordinate not found")
    return {"message": "Transaction successfully deleted"}