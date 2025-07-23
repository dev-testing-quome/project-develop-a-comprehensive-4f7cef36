from sqlalchemy.orm import Session
from ..models import Showing
from ..schemas import ShowingCreate, ShowingUpdate

def create(db: Session, showing: ShowingCreate) -> Showing:
    db_showing = Showing(**showing.dict())
    db.add(db_showing)
    db.commit()
    db.refresh(db_showing)
    return db_showing

def get(db: Session, showing_id: int) -> Showing:
    return db.query(Showing).filter(Showing.id == showing_id).first()

def update(db: Session, db_showing: Showing, showing: ShowingUpdate) -> Showing:
    db_showing.property_id = showing.property_id
    db_showing.client_id = showing.client_id
    db_showing.scheduled_time = showing.scheduled_time
    db_showing.notes = showing.notes
    db_showing.confirmed = showing.confirmed
    db.commit()
    db.refresh(db_showing)
    return db_showing

def delete(db: Session, showing_id: int):
    db_showing = db.query(Showing).filter(Showing.id == showing_id).first()
    if db_showing:
        db.delete(db_showing)
        db.commit()
