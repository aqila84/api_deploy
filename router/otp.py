from fastapi import FastAPI, File, UploadFile, Request, Depends, Response, APIRouter
import crud
import schemas
from requests import Session
from database import get_db
from http.client import HTTPException
from typing import List
from database import get_db

router = APIRouter()

# @router.post("/request-otp/{user_id}")
# def request_otp(user_id: int, db: Session = Depends(get_db)):
#     """Buat dan kirim OTP ke user"""
#     otp = create_otp(db, user_id)
#     return {"message": f"OTP {otp.Code} telah dibuat untuk user {user_id}", "expiry": otp.Expiry}

# @router.post("/verify-otp/{user_id}")
# def verify_otp_api(user_id: int, otp_code: str, db: Session = Depends(get_db)):
#     """Verifikasi OTP"""
#     is_valid, message = verify_otp(db, user_id, otp_code)
    
#     if not is_valid:
#         raise HTTPException(status_code=400, detail=message)
    
#     return {"message": message}