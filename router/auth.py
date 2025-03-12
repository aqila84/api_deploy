from fastapi import FastAPI, File, UploadFile, Request, Depends, Response, APIRouter, Security
import crud
import schemas
from requests import Session
from database import get_db
from http.client import HTTPException
from typing import List
from database import get_db
import bcrypt
from datetime import datetime
import os
import jwt
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import models

router = APIRouter()


load_dotenv()

SECRET_KEY = os.getenv("28dn13u71y80hfh3f01ħnf1g7fv18v4f891gsbhdj7941y9obv2", "your_default_secret")

router = APIRouter(prefix="/auth", tags=["Authentication"])

def create_jwt_token(data: dict):
    """Generate JWT Token"""
    payload = data.copy()
    payload.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)})  # Token valid 1 jam
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

#login
@router.post("/login")
def login_staff(auth_data: schemas.StaffLogin, db: Session = Depends(get_db)):
    """Login hanya butuh Email & Password"""
    staff = db.query(models.Staff).filter(models.Staff.Email == auth_data.Email).first()

    if not staff or not bcrypt.checkpw(auth_data.Password.encode(), staff.Password.encode()):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = jwt.encode({"StaffID": staff.StaffID, "Email": staff.Email}, SECRET_KEY, algorithm="HS256")
    
    return {"access_token": token, "token_type": "bearer"}


#verif token & return staff data
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_staff(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    """Verifikasi Token & Return Data Staff"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        staff = db.query(models.Staff).filter(models.Staff.StaffID == payload["StaffID"]).first()
        if not staff:
            raise HTTPException(status_code=401, detail="Invalid token")
        return staff
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/profile", response_model=schemas.StaffResponse)
def get_staff_profile(current_staff: models.Staff = Depends(get_current_staff)):
    """Get Profile Staff yang sedang login"""
    return current_staff
