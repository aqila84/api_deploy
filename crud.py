from sqlalchemy import cast, Date, and_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from datetime import datetime, timedelta    
from fastapi import HTTPException, Depends
from sqlalchemy.sql import func
from typing import List
import models
import schemas
import uuid

def create_user(db: Session, user: schemas.UserCreate):
    user_uuid = uuid.uuid4()
    db_user = models.User(**user.dict(), UserID=user_uuid)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_role(db: Session, userrole: schemas.UserRoleCreate):
    db_user_role = models.UserRole(**userrole.dict())
    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)
    return db_user_role

def get_user_role_by_id(db: Session, id: int):
    return db.query(models.UserRole).filter(models.UserRole.UserRoleID == id).first()

def delete_user_role_by_name(db: Session, UserRoleName:str):
    db_user = db.query(models.UserRole).filter(models.UserRole.UserRoleName == UserRoleName).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

# * -> .all()

def get_user_role(db:Session):
    return db.query(models.UserRole).all()

def delete_user_by_name(db: Session, Name:str):
    db_user = db.query(models.User).filter(models.User.Name == Name).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def get_user_by_name(db:Session, Name:str):
    return db.query(models.User).filter(models.User.Name == Name).first()

def update_user_role_by_id(db: Session, UserRoleID:int, user_role_update: schemas.UserRoleUpdate):
    userrole = db.query(models.UserRole).filter(models.UserRole.UserRoleID == UserRoleID).first()
    if not userrole:
        return None
    userrole.UserRoleName = user_role_update.UserRoleName

    db.commit()
    db.refresh(userrole)
    
    return userrole

def update_user_address_by_name(db: Session, Name:str, user_update: schemas.UserUpdateAddress):
    user = db.query(models.User).filter(models.User.Name == Name).first()
    if not user:
        return None
    user.Address = user_update.Address

    db.commit()
    db.refresh(user)

    return user
        
def update_user_by_name(db: Session, Name:str, user_update: schemas.UserUpdate):
    user = db.query(models.User).filter(models.User.Name == Name).first()
    
    if not user:
        return None
    
    user.Name = user_update.Name
    user.DateofBirth = user_update.DateofBirth
    user.Contact = user_update.Contact
    user.Address = user_update.Address
    user.Job = user_update.Job
    user.UserRoleID = user_update.UserRoleID

    db.commit()
    db.refresh(user)

    return user

def update_user_job_by_name(db: Session, Name:str, user_update: schemas.UserUpdateJob):
    user = db.query(models.User).filter(models.User.Name == Name).first()
    
    if not user:
        return None
    
    user.Job = user_update.Job
    
    db.commit()
    db.refresh(user)

    return user
 
# Documents 

def create_document(db: Session, documents : schemas.DocumentCreate):
    db_document = models.Documents(**documents.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_document(db:Session):
    return db.query(models.Documents).all()

def get_document_by_id(db: Session, id: int):
    return db.query(models.Documents).filter(models.Documents.DocumentID == id).first()

def get_document_by_name(db:Session, FileName:str):
    return db.query(models.Documents).filter(models.Documents.FileName == FileName).first()

# def get_document_by_created_date(db:Session,CreatedAt:datetime):
#     return db.query(models.Documents).filter(models.Documents.CreatedAt == CreatedAt).first()

def update_document_by_name(db: Session, FileName:str, document_update: schemas.DocumentUpdate):
    document = db.query(models.Documents).filter(models.Documents.FileName == FileName).first()
    
    if not document:
        return None
    
    document.FileName = document_update.FileName
    document.Filetype = document_update.Filetype
    document.StoragePath = document_update.StoragePath
    document.Status  = document_update.Status 
    document.CreatedAt = document_update. CreatedAt
    document.SignedAt = document_update. SignedAt
    document.UserID = document_update.UserID

    db.commit()
    db.refresh(document)

    return document

def delete_document_by_name(db: Session, FileName:str):
    db_document = db.query(models.Documents).filter(models.Documents.FileName == FileName).first()
    if db_document:
        db.delete(db_document)
        db.commit()
        return True
    return False

#Signature

def create_signature(db: Session, signature : schemas.SignatureCreate):
    db_signature = models.Signature(**signature.dict())
    db.add(db_signature)
    db.commit()
    db.refresh(db_signature)
    return db_signature

def get_signature(db:Session):
    return db.query(models.Signature).all()

def get_signature_by_id(db: Session, id: int):
    return db.query(models.Signature).filter(models.Signature.SignatureID == id).first() 

def update_signature_by_id(db: Session, id:int, signature_update: schemas.SignatureUpdate):
    signature = db.query(models.Signature).filter(models.Signature.SignatureID == id).first()
    
    if not signature:
        return None
    
    signature.SignatureData = signature_update.SignatureData
    signature.ExpiryDate = signature_update.ExpiryDate
    signature.UserID = signature_update.UserID


    db.commit()
    db.refresh(signature)

    return signature

def delete_signature_by_id(db: Session, id:int):
    db_signature = db.query(models.Signature).filter(models.Signature.SignatureID == id).first()
    if db_signature:
        db.delete(db_signature)
        db.commit()
        return True
    return False