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

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    UserID: UUID
    role: UserRoleResponse

    class Config:
        orm_mode = True

