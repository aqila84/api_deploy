from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime, Enum, BigInteger, Table, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, Boolean

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
    
    userrole = relationship("UserRole", back_populates="user")
    documents = relationship("Documents",back_populates="user")
    signature = relationship("Signature",back_populates="user",uselist=False)
    
# UserRole class
class UserRole(Base):
    __tablename__ = "userrole" 
    
    UserRoleID = Column(Integer(), primary_key=True)
    UserRoleName = Column(String(20))
    
    # Back-reference to user
    user = relationship("User", back_populates="userrole")

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

    