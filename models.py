from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime, Enum, BigInteger, Table, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, Boolean
import bcrypt
from datetime import datetime

Base = declarative_base()

# User class
class User(Base):
    __tablename__ = "user"
    
    UserID = Column(UUID(as_uuid=True), primary_key=True)
    Name = Column(String(50))
    DateofBirth = Column(DateTime)
    Contact = Column(Integer())
    Address = Column(String(200))
    Job = Column(String(100))
    UserRoleID = Column(Integer(), ForeignKey("userrole.UserRoleID"))
    HospitalID = Column(Integer(), ForeignKey("hospital.HospitalID"))
    
    userrole = relationship("UserRole", back_populates="user")
    hospital = relationship("Hospital", back_populates="user")
    documents = relationship("Documents",back_populates="user")
    signature = relationship("Signature",back_populates="user",uselist=False)
    
# UserRole class
class UserRole(Base):
    __tablename__ = "userrole" 
    
    UserRoleID = Column(Integer(), primary_key=True)
    UserRoleName = Column(String(20))
    
    # Back-reference to user
    user = relationship("User", back_populates="userrole")

class Hospital(Base):
    __tablename__ = "hospital"

    HospitalID = Column(Integer(), primary_key=True)
    HospitalName = Column(String(50))
    Address = Column(String(100))
    TTEQuota = Column(Integer())
    UsedTTEQuota = Column(Integer())
    
    user = relationship("User", back_populates="hospital")
    staff = relationship("Staff", back_populates="hospital")
    transaction = relationship("Transaction",  back_populates="hospital")

class Staff(Base):
    __tablename__ = "staff"

    StaffID = Column(Integer(), primary_key=True)
    Name = Column(String(50))
    Contact = Column(Integer())
    Email = Column(String(50))
    Password = Column(String(255))
    HospitalID = Column(Integer(), ForeignKey("hospital.HospitalID"))
    StaffRoleID = Column(Integer(), ForeignKey("staffrole.StaffRoleID"))

    hospital = relationship("Hospital", back_populates="staff")
    staffrole = relationship("StaffRole", back_populates="staff")
    log = relationship("Log", back_populates="staff", cascade="all, delete")

    # def set_password(self, plain_password: str):
    #     salt = bcrypt.gensalt()
    #     self.Password = bcrypt.hashpw(plain_password.encode(), salt).decode()

    # def check_password(self, plain_password: str) -> bool:
    #     return bcrypt.checkpw(plain_password.encode(), self.Password.encode())

class StaffRole(Base):
    __tablename__ = "staffrole"

    StaffRoleID = Column(Integer(), primary_key=True)
    StaffRoleName = Column(String(20))

    staff = relationship("Staff", back_populates="staffrole")

class Log(Base):
    __tablename__ = "log"

    LogID = Column(Integer(), primary_key=True)
    Action = Column(String(100))
    Timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    StaffID = Column(Integer(), ForeignKey("staff.StaffID"), nullable=False)

    staff = relationship("Staff", back_populates="log")
#Documents class
class Documents(Base):
    __tablename__ = "document"

    DocumentID = Column(Integer(),primary_key=True)
    FileName = Column(String(100))
    Filetype = Column(String(20))
    StoragePath = Column(String(50))
    Status = Column(String(20))
    CreatedAt = Column(DateTime)
    SignedAt = Column(DateTime)
    UserID = Column(UUID(as_uuid=True),ForeignKey("user.UserID"))

    #Relationship to user 
    user = relationship("User",back_populates="documents")

#Signature class
class Signature(Base):
    __tablename__ = "signature"

    SignatureID = Column(Integer(),primary_key=True)
    SignatureData = Column(String(100))
    ExpiryDate = Column(DateTime)
    UserID = Column(UUID(as_uuid=True),ForeignKey("user.UserID"),unique=True)


    user = relationship("User",back_populates="signature")

    

class Transaction(Base):
    __tablename__ = "transaction"

    TransactionID = Column(Integer(), primary_key=True)
    HospitalID = Column(Integer(), ForeignKey("hospital.HospitalID"))
    amount = Column(Integer())
    issuer = Column(String(100))
    payment_type = Column(String(100))
    transaction_time = Column(DateTime())
    status = Column(String(100))
    created_at = Column(DateTime())
    update_at = Column(DateTime())

    hospital = relationship("Hospital", back_populates="transaction")


class coordinate(Base):
    __tablename__ = "coordinate"

    CoordinateID = Column(Integer(), primary_key=True)
    llx = Column(Integer())
    lly = Column(Integer())
    urx = Column(Integer())
    ury = Column(Integer())
    page = Column(Integer())
    status = Column(String(100))
    created_at = Column(DateTime())
    update_at = Column(DateTime())
