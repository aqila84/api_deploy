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
import bcrypt
from datetime import datetime

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

#hospital
def create_hospital(db: Session, hospital: schemas.HospitalCreate):
    db_hospital = models.Hospital(**hospital.dict())
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

def get_hospital_by_name(db: Session, HospitalName:str):
    return db.query(models.Hospital).filter(models.Hospital.HospitalName == HospitalName).first()

def update_hospital_by_name(db: Session, HospitalName:str, hospital_update: schemas.HospitalUpdate):
    hospital = db.query(models.Hospital).filter(models.Hospital.HospitalName == HospitalName).first()

    if not hospital:
        return None

    hospital.HospitalName = hospital_update.HospitalName
    hospital.Address = hospital_update.Address
    hospital.TTEQuota = hospital_update.TTEQuota
    hospital.UsedTTEQuota = hospital_update.UsedTTEQuota

    db.commit()
    db.refresh(hospital)

    return hospital

def delete_hospital_by_name(db: Session, HospitalName:str):
    hospital = db.query(models.Hospital).filter(models.Hospital.HospitalName == HospitalName).first()

    print(hospital)

    if not hospital:
        return None

    db.delete(hospital)
    db.commit()
    return hospital

def delete_hospital_by_id(db: Session, id:int):
    hospital = db.query(models.Hospital).filter(models.Hospital.HospitalID == id).first()

    if not hospital:
        return None

    db.delete(hospital)
    db.commit()

    return hospital


#staff
def create_staff(db: Session, staff: schemas.StaffCreate):
    hashed_password = bcrypt.hashpw(staff.Password.encode(), bcrypt.gensalt()).decode()
    db_staff = models.Staff(**staff.model_dump(exclude={"Password"}), Password=hashed_password)
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

def get_staff_by_name(db: Session, Name:str):
    return db.query(models.Staff).filter(models.Staff.Name == Name).first()

def update_staff_by_name(db: Session, Name:str, staff_update: schemas.StaffUpdate):
    staff = db.query(models.Staff).filter(models.Staff.Name == Name).first()

    if not staff:
        return None

    update_data = staff_update.model_dump(exclude_unset=True)
    
    if "Password" in update_data:
        update_data["Password"] = bcrypt.hashpw(update_data["Password"].encode(), bcrypt.gensalt()).decode()

    for key, value in update_data.items():
        setattr(staff, key, value)
    
    # staff.Name = staff_update.Name
    # staff.Contact = staff_update.Contact
    # staff.Email = staff_update.Email
    # staff.Password = staff_update.Password
    # staff.StaffRoleID = staff_update.StaffRoleID
    # staff.HospitalID = staff_update.HospitalID

    db.commit()
    db.refresh(staff)

    return staff

def delete_staff_by_name(db: Session, Name:str):
    db_staff = db.query(models.Staff).filter(models.Staff.Name == Name).first()
    if db_staff:
        db.delete(db_staff)
        db.commit()
        return True
    return False

#staffrole
def create_staff_role(db: Session, staffrole: schemas.StaffRoleCreate):
    new_role = models.StaffRole(**staffrole.model_dump())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

def get_all_staff_roles(db: Session):
    return db.query(models.StaffRole).all()

def get_staff_role_by_id(db: Session, StaffRoleID: int):
    return db.query(models.StaffRole).filter(models.StaffRole.StaffRoleID == StaffRoleID).first()

def update_staff_role_by_id(db: Session, StaffRoleID: int, staffrole_update: schemas.StaffRoleCreate):
    staffrole = db.query(models.StaffRole).filter(models.StaffRole.StaffRoleID == StaffRoleID).first()
    if not staffrole:
        return None
    staffrole.StaffRoleName = staffrole_update.StaffRoleName
    db.commit()
    db.refresh(staffrole)
    return staffrole

def delete_staff_role_by_name(db: Session, StaffRoleName: str):
    staffrole = db.query(models.StaffRole).filter(models.StaffRole.StaffRoleName == StaffRoleName).first()
    if not staffrole:
        return None
    db.delete(staffrole)
    db.commit()
    return staffrole

#log
def create_log(db: Session, log: schemas.LogCreate):
    new_log = models.Log(**log.dict())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

def get_all_log(db: Session):
    return db.query(models.Log).all()

def get_log_by_staff_id(db: Session, StaffID: int):
    return db.query(models.Log).filter(models.Log.StaffID == StaffID).all()
 
def delete_log_by_id(db: Session, LogID: int):
    log = db.query(models.Log).filter(models.Log.LogID == LogID).first()
    if not log:
        return None
    db.delete(log)
    db.commit()
    return log