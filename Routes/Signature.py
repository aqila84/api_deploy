from fastapi import APIRouter


router = APIRouter()

@router.post('/signature/post',response_model= schemas.SignatureBase, tags=["Signature"])
def create_signature(signature: schemas.SignatureCreate, db:Session = Depends(get_db)):
    return crud.create_signature(db,signature)

@router.get('/signature/getall',response_model= List[schemas.SignatureBase], tags=["Signature"])
def get_signature( db:Session = Depends(get_db)):
    return crud.get_signature(db)

@router.get('/signature/get/{id}',response_model=schemas.SignatureBase, tags=["Signature"])
def get_signature_by_id(id:int,db: Session = Depends(get_db)):
    return crud.get_signature_by_id(db,id)

@router.patch('/signature/update_signature/{id}',tags=["Signature"])
def update_signature_by_id(id:int, signatureupdate:schemas.SignatureUpdate, db: Session = Depends(get_db)):
    updated_signature = crud.update_signature_by_id(db, id, signatureupdate)
    if not updated_signature:
        raise HTTPException(status_code=404, detail="Signature does not exist")
    return updated_signature

@router.delete('/signature/delete_signature/{id}',tags=["Signature"])
def delete_signature_by_id(id:int,db:Session = Depends(get_db)):
    crud.delete_signature_by_id(db,id)
    return {"message": "Signature Successfully Deleted"}