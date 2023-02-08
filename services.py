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

def update_app(db: Session, app: schemas.AppBase, app_id: int):
    db_query = db.query(models.App).filter(models.App.id == app_id)
    db_data = db_query.first()
    db_query.filterfilter(models.App.id == app_id).update(app,synchronize_session=False)
    db.commit()
    db.refresh(db_data)
    return db_data

def delete_app(db: Session, app_id: int):
    db_app = db.query(models.App).filter(models.App.id == app_id).first()
    db.delete(db_app)
    db.commit()
    return {
        "success": True
    }

def get_requests(db: Session, skip: int = 0, limit: int = 100, app_id: int = 0):
    if app_id == 0:
        return db.query(models.Request).offset(skip).limit(limit).all()
    else:
        return db.query(models.Request).filter(models.Request.owner_id == app_id).offset(skip).limit(limit).all()

def get_request(db: Session, request_id:int):
    return db.query(models.Request).filter(models.Request.id == request_id).first()

def create_request(db: Session, request: schemas.RequestBase, app_id: int = 0):
    if app_id == 0:
        return None
    db_request = models.Request(**request.dict(), owner_id=app_id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def update_request(db: Session, request: schemas.RequestBase, request_id: int):
    db_query = db.query(models.Request).filter(models.Request.id == request_id)
    db_data = db_query.first()
    update_data = request.dict(exclude_unset=True)
    db_query.filter(models.Request.id == request_id).update(update_data,synchronize_session=False)
    db.commit()
    db.refresh(db_data)
    return db_data

def delete_request(db: Session, request_id: int):
    db_app = db.query(models.Request).filter(models.Request.id == request_id).first()
    db.delete(db_app)
    db.commit()
    return {
        "success": True
    }

def get_tests(db: Session, skip: int = 0, limit: int = 100, request_id: int = 0):
    if request_id == 0:
        return db.query(models.Test).offset(skip).limit(limit).all()
    else:
        return db.query(models.Test).filter(models.Test.request_id == request_id).order_by(models.Test.id.desc()).offset(skip).limit(limit).all()
def create_test(db: Session,request_id: int = 0):
    if request_id == 0:
        return None
    db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
    passed, response = utils.test_request(db_request)
    db_test = models.Test(passed=passed, request_id=request_id)
    db.add(db_test)
    db.commit()
    db.refresh(db_request)
    db_test.response = response
    return db_test

def test_app(db: Session,app_id: int = 0):
    if app_id == 0:
        return None
    db_requests = db.query(models.Request).filter(models.Request.owner_id == app_id).all()
    print(schemas.Test(db_requests[0]))
    list = []
    for request in db_requests:
        passed, response = utils.test_request(request)
        db_test = models.Test(passed=passed, response=response, request_id=request.id)
        db.add(db_test)
        db.commit()
        db.refresh(request)
        list.append((db_test))
    return list