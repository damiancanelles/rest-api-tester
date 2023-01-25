from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import services
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/apps/", response_model=schemas.App)
def create_user(app: schemas.AppBase, db: Session = Depends(get_db)):
    return services.create_app(db=db, app=app)

@app.get("/apps/", response_model=list[schemas.App])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    apps = services.get_apps(db, skip=skip, limit=limit)
    return apps

@app.post("/apps/{app_id}/request/", response_model=schemas.Request)
def create_request(app_id: int, request: schemas.RequestBase, db: Session = Depends(get_db)):
    return services.create_request(db=db, request=request, app_id=app_id)

@app.get("/apps/{app_id}/request/", response_model=list[schemas.Request])
def list_request(app_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_requests(db=db, skip=skip, limit=limit, app_id=app_id)

@app.get("/request/{request_id}/test", response_model=schemas.Test)
def create_test(request_id: int, db: Session = Depends(get_db)):
    return services.create_test(db=db, request_id=request_id)