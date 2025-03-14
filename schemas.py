from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr

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
    HospitalID: Optional[int]

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    Name: Optional[str]
    DateofBirth: Optional[datetime] 
    Contact: Optional[int]
    Address: Optional[str] 
    Job: Optional[str] 
    UserRoleID: Optional[int] 
    HospitalID: Optional[int] 
class UserResponse(UserBase):
    UserID: UUID
    role: UserRoleResponse

    class Config:
        orm_mode = True


#Hospital Schemas
class HospitalBase(BaseModel):
    HospitalName: str
    Address: str
    TTEQuota: int
    UsedTTEQuota: int

class HospitalCreate(HospitalBase):
    pass

class HospitalUpdate(HospitalBase):
    pass

class HospitalResponse(HospitalBase):
    HospitalID: int

    class Config:
        from_attributes = True


#Staff Schemas
class StaffBase(BaseModel):
    Name: str
    Contact: int
    Email: EmailStr
    StaffRoleID: int

class StaffCreate(StaffBase):
    Password: str
    HospitalID: int

class StaffUpdate(StaffBase):
    pass

class StaffLogin(BaseModel):
    Email: EmailStr
    Password: str

class StaffResponse(StaffBase):
    StaffID: int
    HospitalID: int

    class Config:
        from_attributes = True


#StaffRole Schemas
class StaffRoleBase(BaseModel):
    StaffRoleName: str

class StaffRoleCreate(StaffRoleBase):
    pass

class StaffRoleResponse(StaffRoleBase):
    StaffRoleID: int
    
    class Config:
        from_attributes = True

#Log Schemas
class LogBase(BaseModel):
    Action: str
    StaffID: int

class LogCreate(LogBase):
    pass

class LogResponse(LogBase):
    LogID: int
    Timestamp: datetime
    
    class Config:
        from_attributes = True

# Documents Schema
class DocumentBase(BaseModel):
    FileName: str
    Filetype: str
    StoragePath: str
    Status: str
    CreatedAt: datetime
    SignedAt: Optional[datetime]
    UserID: UUID
    StaffID: int
    SignatureID: Optional[int]

class DocumentCreate(DocumentBase):
    pass 

class DocumentUpdate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    DocumentID: int

    class Config:
        orm_mode = True

# Signature Schema
class SignatureBase(BaseModel):
    SignatureData: str
    ExpiryDate: Optional[datetime]
    UserID: UUID

class SignatureCreate(SignatureBase):
    pass  # Used when creating a new signature

class SignatureUpdate(SignatureBase):
    pass

class SignatureResponse(SignatureBase):
    SignatureID: int

    class Config:
        orm_mode = True

#Transaction Schemas
class TransactionBase(BaseModel):
    HospitalID: int
    quota: int
    amount: int
    issuer: str
    payment_type: str
    transaction_time: datetime
    status: str
    created_at: datetime = datetime.utcnow()
    update_at: datetime = datetime.utcnow()

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    quota: Optional[int]
    amount: Optional[int]
    issuer: Optional[str] 
    payment_type: Optional[str] 
    status: Optional[str] 
    update_at: datetime = datetime.utcnow()

class TransactionResponse(TransactionBase):
    TransactionID: int
    class Config:
        from_attributes = True

#Coordinate Schemas
class CoordinateBase(BaseModel):
    DocumentID: int
    llx: int
    lly: int
    urx: int
    ury: int
    page: int
    status: str
    created_at: datetime = datetime.utcnow()
    update_at: datetime = datetime.utcnow()

class CoordinateCreate(CoordinateBase):
    pass

class CoordinateUpdate(BaseModel):
    llx: Optional[int]
    lly: Optional[int] 
    urx: Optional[int]
    ury: Optional[int] 
    page: Optional[int] 
    status: Optional[str] 
    update_at: datetime = datetime.utcnow()

class CoordinateResponse(CoordinateBase):
    CoordinateID: int
    class Config:
        from_attributes = True

#Otp Schemas
class OtpBase(BaseModel):
    OtpID: int
    UserID: int
    Code: str 
    created_at: datetime = datetime.utcnow()
    expired_at: datetime

class OtpCreate(BaseModel):
    pass

class OtpResponse(OtpBase):
    OtpID: int 
    created_at: datetime

    class Config:
        from_attributes = True