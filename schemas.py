from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

# UserRole Schemas
class UserRoleBase(BaseModel):
    UserRoleName: str

class UserRoleCreate(UserRoleBase):
    pass

class UserRoleUpdate(UserRoleBase):
    pass

class UserRoleResponse(UserRoleBase):
    UserRoleID: int

    class Config:
        orm_mode = True

# User Schemas
class UserBase(BaseModel):
    Name: str
    DateofBirth: datetime
    Contact: int
    Address: str
    Job: str
    UserRoleID: int

class UserUpdateAddress(BaseModel):
    Address: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserUpdateJob(BaseModel):
    Job: str

class UserResponse(UserBase):
    UserID: UUID
    role: UserRoleResponse

    class Config:
        orm_mode = True

# Documents Schema
class DocumentBase(BaseModel):
    DocumentID: int
    FileName: str
    Filetype: str
    StoragePath: str
    Status: str
    CreatedAt: Optional[datetime]
    SignedAt: Optional[datetime]
    UserID: UUID

class DocumentCreate(DocumentBase):
    pass  # Used when creating a new document

class DocumentResponse(DocumentBase):
    class Config:
        orm_mode = True

# Signature Schema
class SignatureBase(BaseModel):
    SignatureID: int
    SignatureData: str
    ExpiryDate: Optional[datetime]
    UserID: UUID

class SignatureCreate(SignatureBase):
    pass  # Used when creating a new signature

class SignatureResponse(SignatureBase):
    class Config:
        orm_mode = True
