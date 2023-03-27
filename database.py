from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DB_CONNECTION_STR","mssql+pyodbc://sa:YourStrongPassword'@localhost:1433/api_tester_db?driver=ODBC+Driver+18+for+SQL+Server")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()