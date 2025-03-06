from http.client import HTTPException
from requests import Session
from Routes import Documents, Signature
from router import hospital, log, staff, staffrole, user, userrole, transaction, coordinate
from database import SessionLocal,get_db
from objstr import *
from fastapi import FastAPI, File, UploadFile, Request, Depends, Response
import schemas
from fastapi.middleware.cors import CORSMiddleware
import crud
import models
from typing import List

from datetime import datetime
import base64
import requests
import json

# Declare FastAPI
app = FastAPI()

#midtrans
MIDTRANS_SERVER_KEY = "SB-Mid-server-bGHJLsV9znePb4tZqFA7-MSA"  # Ganti dengan Server Key dari Midtrans
MIDTRANS_BASE_URL = "https://app.sandbox.midtrans.com/snap/v1/transactions"


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

#coordinate
app.include_router(coordinate.router, tags=["Coordinate"])


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


@app.post("/create-payment")
def create_payment(hospital_id: int, amount: int, issuer: str, db: Session = Depends(get_db)):
    # Simpan transaksi ke database
    new_transaction = models.Transaction(
        HospitalID=hospital_id,
        amount=amount,
        issuer=issuer,
        payment_type="midtrans",
        transaction_time=datetime.now(),
        status="pending",
        created_at=datetime.now(),
        update_at=datetime.now()
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    # Header dan payload untuk request ke Midtrans Snap
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Basic " + base64.b64encode((MIDTRANS_SERVER_KEY + ":").encode()).decode()
    }

    payload = {
        "transaction_details": {
            "order_id": str(new_transaction.TransactionID),
            "gross_amount": amount
        },
        "customer_details": {
            "first_name": issuer
        }
    }

    response = requests.post(MIDTRANS_BASE_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        midtrans_response = response.json()
        return {
            "order_id": new_transaction.TransactionID,
            "redirect_url": midtrans_response["redirect_url"]  # URL untuk pembayaran di Midtrans Snap
        }
    else:
        return {"error": "Gagal membuat transaksi", "detail": response.text}

    
# @app.post("/midtrans-callback")
# async def midtrans_callback(data: dict, db: Session = Depends(get_db)):
#     order_id = data.get("order_id")
#     transaction_status = data.get("transaction_status")

#     transaction = db.query(models.Transaction).filter(models.Transaction.TransactionID == order_id).first()
#     if transaction:
#         transaction.status = transaction_status
#         transaction.update_at = datetime.now()
#         db.commit()
#         db.refresh(transaction)

#     return {"message": f"Status transaksi {order_id} diperbarui ke {transaction_status}"}

import logging

logging.basicConfig(level=logging.INFO)

@app.post("/midtrans-callback")
async def midtrans_callback(data: dict, db: Session = Depends(get_db)):
    logging.info(f"Received callback: {data}")

    order_id = data.get("order_id")
    transaction_status = data.get("transaction_status")

    if not order_id or not transaction_status:
        logging.error("Invalid callback data")
        return {"error": "Invalid data"}, 400

    transaction = db.query(models.Transaction).filter(models.Transaction.TransactionID == order_id).first()
    
    if transaction:
        transaction.status = transaction_status
        transaction.update_at = datetime.now()
        db.commit()
        db.refresh(transaction)
        return {"message": f"Status transaksi {order_id} diperbarui ke {transaction_status}"}
    else:
        logging.error(f"Transaction {order_id} not found")
        return {"error": "Transaction not found"}, 404


