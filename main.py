from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import services
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/apps/", response_model=schemas.App)
def create_app(app: schemas.AppBase, db: Session = Depends(get_db)):
    return services.create_app(db=db, app=app)

@app.post("/apps/", response_model=schemas.App)
def update_app(app: schemas.AppBase, db: Session = Depends(get_db)):
    return services.update_app(db=db, app=app)

@app.get("/apps/", response_model=list[schemas.App])
def list_apps(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    apps = services.get_apps(db, skip=skip, limit=limit)
    return apps

@app.delete("/apps/{app_id}/", response_model=None)
def delete_app(app_id: int, db: Session = Depends(get_db)):
    app = services.delete_app(db, app_id)
    return app

@app.post("/apps/{app_id}/request/", response_model=schemas.Request)
def create_request(app_id: int, request: schemas.RequestBase, db: Session = Depends(get_db)):
    return services.create_request(db=db, request=request, app_id=app_id)

@app.patch("/requests/{request_id}/", response_model=schemas.Request)
def update_request(request_id: int, request: schemas.RequestBase, db: Session = Depends(get_db)):
    return services.update_request(db=db, request=request, request_id=request_id)

@app.delete("/apps/request/{request_id}/", response_model=None)
def delete_request(request_id: int, db: Session = Depends(get_db)):
    return services.delete_request(db=db, request_id=request_id)

@app.get("/apps/{app_id}/request/", response_model=list[schemas.Request])
def list_request(app_id: int, db: Session = Depends(get_db)):
    return services.get_requests(db=db, app_id=app_id)

@app.get("/apps/{app_id}/test/", response_model=list[schemas.Request])
def create_all_test(app_id: int, db: Session = Depends(get_db)):
    return services.test_app(db=db, app_id=app_id)

@app.get("/requests/{request_id}/test/", response_model=schemas.Test)
def create_test(request_id: int, db: Session = Depends(get_db)):
    return services.create_test(db=db, request_id=request_id)

@app.get("/requests/{request_id}/", response_model=schemas.Request)
def get_request(request_id: int, db: Session = Depends(get_db)):
    return services.get_request(db=db, request_id=request_id)

@app.get("/requests/{request_id}/tests/", response_model=list[schemas.Test])
def list_tests(request_id: int, skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    return services.get_tests(db=db, skip=skip, limit=limit, request_id=request_id)