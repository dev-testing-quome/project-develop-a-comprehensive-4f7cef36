from sqlalchemy.orm import Session
from ..models import Client
from ..schemas import ClientCreate, ClientUpdate

def create(db: Session, client: ClientCreate) -> Client:
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get(db: Session, client_id: int) -> Client:
    return db.query(Client).filter(Client.id == client_id).first()

def update(db: Session, db_client: Client, client: ClientUpdate) -> Client:
    db_client.first_name = client.first_name
    db_client.last_name = client.last_name
    db_client.email = client.email
    db_client.phone = client.phone
    db.commit()
    db.refresh(db_client)
    return db_client

def delete(db: Session, client_id: int):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client:
        db.delete(db_client)
        db.commit()
