from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Property, PropertyCreate, PropertyUpdate
from ..services import property_service

router = APIRouter(prefix="/api/properties", tags=["Properties"])

@router.post("", response_model=Property, status_code=status.HTTP_201_CREATED)
def create_property(property: PropertyCreate, db: Session = Depends(get_db)):
    return property_service.create(db, property)

@router.get("/{property_id}", response_model=Property)
def get_property(property_id: int, db: Session = Depends(get_db)):
    property = property_service.get(db, property_id)
    if not property:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return property

@router.put("/{property_id}", response_model=Property)
def update_property(property_id: int, property: PropertyUpdate, db: Session = Depends(get_db)):
    db_property = property_service.get(db, property_id)
    if not db_property:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return property_service.update(db, db_property, property)

@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(property_id: int, db: Session = Depends(get_db)):
    property_service.delete(db, property_id)
