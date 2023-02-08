from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = "postgresql://api_tester_db_user:FpFhjhpWPysRDfJLVcczpxY0RZz4b5X5@dpg-cfhshfg2i3murcbq41pg-a.oregon-postgres.render.com/api_tester_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()