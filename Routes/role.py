from fastapi import APIRouter


router = APIRouter()

@router.get("/role/baru")
def role_baru():
    return {"message":"Role Baru"}