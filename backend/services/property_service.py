from sqlalchemy.orm import Session
from ..models import Property
from ..schemas import PropertyCreate, PropertyUpdate

def create(db: Session, property: PropertyCreate) -> Property:
    db_property = Property(**property.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

def get(db: Session, property_id: int) -> Property:
    return db.query(Property).filter(Property.id == property_id).first()

def update(db: Session, db_property: Property, property: PropertyUpdate) -> Property:
    db_property.address = property.address
    db_property.city = property.city
    db_property.state = property.state
    db_property.zip_code = property.zip_code
    db_property.price = property.price
    db_property.description = property.description
    db_property.mls_id = property.mls_id
    db.commit()
    db.refresh(db_property)
    return db_property

def delete(db: Session, property_id: int):
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if db_property:
        db.delete(db_property)
        db.commit()
