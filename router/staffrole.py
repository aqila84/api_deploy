from fastapi import FastAPI, File, UploadFile, Request, Depends, Response, APIRouter
import crud
import schemas
from requests import Session
from database import get_db
from http.client import HTTPException
from typing import List
from database import get_db

router = APIRouter()

#staffrole
@router.post("/staffrole/post", response_model=schemas.StaffRoleResponse, tags=["StaffRole"])
def create_staff_role(staffrole: schemas.StaffRoleCreate, db: Session = Depends(get_db)):
    return crud.create_staff_role(db, staffrole)

@router.get("/staffrole/get", response_model=List[schemas.StaffRoleBase])
def get_staff_role(db: Session = Depends(get_db)):
    return crud.get_staff_role(db)

@router.get("/staffrole/get/{StaffRoleID}", response_model=schemas.StaffRoleResponse, tags=["StaffRole"])
def get_staff_role_by_id(StaffRoleID: int, db: Session = Depends(get_db)):
    staffrole = crud.get_staff_role_by_id(db, StaffRoleID)
    if not staffrole:
        raise HTTPException(status_code=404, detail="StaffRole not found")
    return staffrole

@router.put("/staffrole/update/{StaffRoleID}", response_model=schemas.StaffRoleResponse, tags=["StaffRole"])
def update_staff_role_by_id(StaffRoleID: int, staffrole_update: schemas.StaffRoleCreate, db: Session = Depends(get_db)):
    updated_role = crud.update_staff_role_by_id(db, StaffRoleID, staffrole_update)
    if not updated_role:
        raise HTTPException(status_code=404, detail="StaffRole not found")
    return updated_role

@router.delete("/staffrole/delete/{StaffRoleName}", tags=["StaffRole"])
def delete_staff_role_by_name(StaffRoleName: str, db: Session = Depends(get_db)):
    deleted_role = crud.delete_staff_role_by_name(db, StaffRoleName)
    if not deleted_role:
        raise HTTPException(status_code=404, detail="StaffRole not found")
    return {"message": "StaffRole successfully deleted"}