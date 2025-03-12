import base64
import json
from datetime import datetime
from http.client import HTTPException
from typing import List

import requests
from fastapi import (APIRouter, Depends, FastAPI, File, Request, Response,
                     UploadFile)
from requests import Session

import crud
import models
import schemas
from database import get_db

router = APIRouter()

#midtrans
MIDTRANS_SERVER_KEY = "SB-Mid-server-bGHJLsV9znePb4tZqFA7-MSA"  # Ganti dengan Server Key dari Midtrans
MIDTRANS_BASE_URL = "https://app.sandbox.midtrans.com/snap/v1/transactions"

#create transaction
@router.post("/create-payment")
def create_payment(hospital_id: int, quota:int, issuer: str, db: Session = Depends(get_db)):
    """Rp.1000,00 per Quota"""
    # Simpan transaksi ke database
    new_transaction = models.Transaction(
        HospitalID=hospital_id,
        quota=quota,
        amount=quota*1000,
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
            "gross_amount": new_transaction.amount
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


#callback
import logging

logging.basicConfig(level=logging.INFO)

@router.post("/midtrans-callback")
async def midtrans_callback(data: dict, db: Session = Depends(get_db)):
    logging.info(f"Received callback: {data}")

    order_id = data.get("order_id")
    transaction_status = data.get("transaction_status")
    # channel = data.get("channel")

    if not order_id or not transaction_status:
        logging.error("Invalid callback data")
        return {"error": "Invalid data"}, 400

    transaction = db.query(models.Transaction).filter(models.Transaction.TransactionID == order_id).first()
    
    if transaction:
        transaction.status = transaction_status
        transaction.update_at = datetime.now()

        if transaction_status in ["settlement", "success", "capture"]: 
            hospital = db.query(models.Hospital).filter(models.Hospital.HospitalID == transaction.HospitalID).first()
            if hospital:
                print("Hospital exists")
                hospital.TTEQuota += transaction.quota
                db.commit()
                db.refresh(hospital)
            else:
                print("Hospital doesn't exist")
        # transaction.payment_type = channel
        db.commit()
        db.refresh(transaction)
        return {"message": f"Status transaksi {order_id} diperbarui ke {transaction_status}"}
    else:
        logging.error(f"Transaction {order_id} not found")
        return {"error": "Transaction not found"}, 404


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