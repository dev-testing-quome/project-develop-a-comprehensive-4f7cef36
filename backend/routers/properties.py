from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import PropertyCreate, Property
from services import property_service

router = APIRouter(prefix="/api/properties", tags=["Properties"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Property, status_code=status.HTTP_201_CREATED)
def create_property(property: PropertyCreate, db: Session = Depends(get_db)):
    return property_service.create_property(db, property)

@router.get("/{property_id}", response_model=Property)
def get_property(property_id: int, db: Session = Depends(get_db)):
    property = property_service.get_property(db, property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property
