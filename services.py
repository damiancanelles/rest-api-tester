from sqlalchemy.orm import Session

import models
import schemas
import utils


def get_apps(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.App).offset(skip).limit(limit).all()

def create_app(db: Session, app: schemas.AppBase):
    db_app = models.App(name=app.name)
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def get_requests(db: Session, skip: int = 0, limit: int = 100, app_id: int = 0):
    if app_id == 0:
        return db.query(models.Request).offset(skip).limit(limit).all()
    else:
        return db.query(models.Request).filter(models.Request.owner_id == app_id).offset(skip).limit(limit).all()

def create_request(db: Session, request: schemas.RequestBase, app_id: int = 0):
    if app_id == 0:
        return None
    db_request = models.Request(**request.dict(), owner_id=app_id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def create_test(db: Session,request_id: int = 0):
    if request_id == 0:
        return None
    db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
    print(db_request)
    passed, response = utils.test_request(db_request)
    db_test = models.Test(passed=passed, response=response, request_id=request_id)
    db.add(db_test)
    db.commit()
    db.refresh(db_request)
    return db_test