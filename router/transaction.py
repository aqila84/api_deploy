from fastapi import FastAPI, File, UploadFile, Request, Depends, Response, APIRouter
import crud
import schemas
from requests import Session
from database import get_db
from http.client import HTTPException
from typing import List
from database import get_db

router = APIRouter()

@router.post("/transaction/post", response_model=schemas.TransactionResponse, tags=["Transaction"])
def create_transaction(transaction:schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db, transaction)

@router.get("/transaction/get", response_model=List[schemas.TransactionBase], tags=["Transaction"])
def get_transaction(db: Session = Depends(get_db)):
    return crud.get_transaction(db)

@router.get("/transaction/get/{HospitalID}")
def get_transaction_by_hospital(HospitalID: int, db: Session = Depends(get_db)):
    transaction = crud.get_transaction_by_hospital(db, HospitalID)
    if not transaction:
        raise HTTPException(status_code=404, detail="No hospital found")
    return transaction

@router.put("/transaction/put/{TransactionID}", response_model=schemas.TransactionResponse)
def update_transaction(TransactionID: int, transaction_data: schemas.TransactionUpdate, db: Session = Depends(get_db)):
    updated_transaction = crud.update_transaction(db, TransactionID, transaction_data)
    if updated_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction data not found")
    return updated_transaction

@router.delete("/transaction/delete/{TransactionID}", tags=["Transaction"])
def delete_transaction_by_id(TransactionID: int, db: Session = Depends(get_db)):
    delete_transaction = crud.delete_transaction_by_id(db, TransactionID)
    if not delete_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction successfully deleted"}
