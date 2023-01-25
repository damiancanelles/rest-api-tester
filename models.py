from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import relationship
import datetime

from database import Base

class App(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    requests = relationship("Request", back_populates="owner")


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    url = Column(String, index=True)
    body = Column(JSONB)
    seach_params = Column(ARRAY(JSONB), index=True)

    tests = relationship("Test", back_populates="request")

    owner_id = Column(Integer, ForeignKey("apps.id"))

    owner = relationship("App", back_populates="requests")

class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    passed = Column(Boolean, index=True)
    response = Column(JSONB, index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    request_id = Column(Integer, ForeignKey("requests.id"))

    request = relationship("Request", back_populates="tests")