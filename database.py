from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import *
import os
from minio import Minio
from models import Base

load_dotenv()

client = Minio(endpoint=os.getenv("MINIO_ENDPOINT"), access_key=os.getenv("MINIO_ACCESS_KEY"), secret_key=os.getenv("MINIO_SECRET_KEY"), secure=False)

SQLALCHEMY_DATABASE_URL = "postgresql://postgres.wsxnnpjbicaxjrntomel:YqPy4pKkvydzfpVx@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(engine)