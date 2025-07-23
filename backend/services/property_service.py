from sqlalchemy.orm import Session
from schemas import PropertyCreate, Property
from models import Property as PropertyModel

def create_property(db: Session, property: PropertyCreate) -> Property:
    db_property = PropertyModel(owner_id=property.owner_id, address=property.address, price=property.price, description=property.description)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return Property.from_orm(db_property)

def get_property(db: Session, property_id: int) -> Optional[Property]:
    return db.query(PropertyModel).filter(PropertyModel.id == property_id).first()
