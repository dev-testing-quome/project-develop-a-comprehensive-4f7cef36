from sqlalchemy.orm import Session
from schemas import ShowingCreate, Showing
from models import Showing as ShowingModel

def create_showing(db: Session, showing: ShowingCreate) -> Showing:
    db_showing = ShowingModel(property_id=showing.property_id, client_id=showing.client_id, date_time=showing.date_time)
    db.add(db_showing)
    db.commit()
    db.refresh(db_showing)
    return Showing.from_orm(db_showing)

def get_showing(db: Session, showing_id: int) -> Optional[Showing]:
    return db.query(ShowingModel).filter(ShowingModel.id == showing_id).first()
