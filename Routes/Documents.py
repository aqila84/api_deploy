from fastapi import APIRouter


router = APIRouter()
@router.post('/document/post', response_model=schemas.DocumentBase, tags=["Document"])
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    return crud.create_document(db,document)

@router.get('/document/getall', response_model=List[schemas.DocumentBase], tags=["Document"])
def get_document(db: Session = Depends(get_db)):
    return crud.get_document(db)

@router.get("/document/get/{id}", response_model=schemas.DocumentBase, tags=["Document"])
def get_document_by_id(id:int, db: Session = Depends(get_db)):
    return crud.get_document_by_id(db,id)

@router.get("/document/get_name/{FileName}", tags=["Document"])
def get_document_by_name(FileName:str,db:Session =Depends(get_db)):
    return crud.get_document_by_name(db,FileName)

@router.patch("/document/update_name/{FileName}", tags=["Document"])
def update_document_by_name(FileName:str, documentupdate:schemas.DocumentUpdate, db: Session = Depends(get_db)):
    updated_document = crud.update_document_by_name(db, FileName, documentupdate)
    if not updated_document:
        raise HTTPException(status_code=404, detail="User does not exist")
    return updated_document

@router.delete("/document/delete_name/{FileName}", tags=["Document"])
def delete_document_by_name(FileName:str, db: Session = Depends(get_db)):
    crud.delete_document_by_name(db, FileName)
    return {"message": "Document Successfully Deleted"}