from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime, Enum, BigInteger, Table, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, Boolean

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    
    UserID = Column(UUID, primary_key=True)
    Name = Column(String(50))
    DateofBirth = Column(DateTime)
    Contact = Column(Integer())
    Address = Column(String(200))
    Job = Column(String(100))
    UserRoleID = Column(Integer(), ForeignKey("userrole.UserRoleID"))
    
    userrole = relationship("UserRole", back_populates="user")
    
class UserRole(Base):
    __tablename__ = "userrole" 
    
    UserRoleID = Column(Integer(), primary_key=True)
    UserRoleName = Column(String(20))
    
    # Back-reference to user
    user = relationship("User", back_populates="userrole")
    