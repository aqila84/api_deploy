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
    Email: str
    StaffRoleID: int

class StaffCreate(StaffBase):
    Password: str
    HospitalID: int

class StaffUpdate(StaffBase):
    pass

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

#Transaction Schemas
class TransactionBase(BaseModel):
    HospitalID: int
    amount: int
    issuer: str
    payment_type: str
    transaction_time: datetime
    status: str
    created_at: datetime
    update_at: datetime

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: int
    issuer: str 
    payment_type: str 
    status: str 
    update_at: datetime = datetime.utcnow()

class TransactionResponse(TransactionBase):
    TransactionID: int
    class Config:
        from_attributes = True

#Coordinate Schemas
class CoordinateBase(BaseModel):
    llx: int
    lly: int
    urx: int
    ury: int
    page: int
    status: str
    created_at: datetime
    update_at: datetime

class CoordinateCreate(CoordinateBase):
    pass

class CoordinateUpdate(BaseModel):
    llx: int 
    lly: int 
    urx: int
    ury: int 
    page: int 
    status: str 
    update_at: datetime = datetime.utcnow()

class CoordinateResponse(CoordinateBase):
    CoordinateID: int
    class Config:
        from_attributes = True
