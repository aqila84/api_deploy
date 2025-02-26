from fastapi import FastAPI, File, UploadFile, Request, Depends, Response, APIRouter
import crud
import schemas
from requests import Session
from database import get_db
from http.client import HTTPException
from typing import List
from database import get_db

router = APIRouter()

#UserRole
@router.post('/userrole/post', response_model=schemas.UserRoleBase, tags=["Role"])
def create_user_role(userrole: schemas.UserRoleCreate, db: Session = Depends(get_db)):
    return crud.create_user_role(db,userrole)

@router.get("/userrole/getall", tags=["Role"])
def get_user_role(db: Session = Depends(get_db)):
    return crud.get_user_role(db)

@router.get("/userrole/get/{id}", response_model=schemas.UserRoleBase, tags=["Role"])
def get_user_role_by_id(id:int, db: Session = Depends(get_db)):
    return crud.get_user_role_by_id(db,id)

@router.put("/userrole/update", tags=["Role"])
def update_user_role_by_id(id:int, userroleupdate:schemas.UserRoleUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user_role_by_id(db, id, userroleupdate)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return updated_user

@router.delete("/userrole/delete",tags=["Role"])
def delete_user_role_by_name(UserRoleName:str,db:Session =Depends(get_db)):
    deleted_user = crud.delete_user_role_by_name(db,UserRoleName)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return {"message": "Role succesfully deleted"}