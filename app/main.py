from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Optional
from . import models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Incident API",   
    description="API для учёта инцидентов",
    version="1.0.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db                                
    finally:
        db.close()

@app.post("/incidents/", response_model=schemas.Incident)
def create_incident(incident: schemas.IncidentCreate, db: SessionLocal = Depends(get_db)):
    """Создать новый инцидент"""
    db_incident = models.Incident(
        description=incident.description,
        source=incident.source
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@app.get("/incidents/", response_model=List[schemas.Incident])
def get_incidents(
    status: Optional[str] = Query(None, description="Фильтр по статусу"),
    db: SessionLocal = Depends(get_db)
):
    """Получить список инцидентов с фильтром по статусу"""
    query = db.query(models.Incident)
    if status:
        query = query.filter(models.Incident.status == status)
    return query.all()

@app.get("/incidents/{incident_id}", response_model=schemas.Incident)
def get_incident(incident_id: int, db: SessionLocal = Depends(get_db)):
    """Получить инцидент по ID"""
    incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Инцидент не найден")
    return incident

@app.patch("/incidents/{incident_id}", response_model=schemas.Incident)
def update_incident_status(
    incident_id: int, 
    status_update: schemas.IncidentStatusUpdate,
    db: SessionLocal = Depends(get_db)
):
    """Обновить статус инцидента"""
    incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Инцидент не найден")
    
    incident.status = status_update.status
    db.commit()
    db.refresh(incident)
    return incident

@app.get("/")
def read_root():
    return {"message": "Incident API работает"}