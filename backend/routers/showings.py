from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import ShowingCreate, Showing
from services import showing_service

router = APIRouter(prefix="/api/showings", tags=["Showings"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Showing, status_code=status.HTTP_201_CREATED)
def create_showing(showing: ShowingCreate, db: Session = Depends(get_db)):
    return showing_service.create_showing(db, showing)

@router.get("/{showing_id}", response_model=Showing)
def get_showing(showing_id: int, db: Session = Depends(get_db)):
    showing = showing_service.get_showing(db, showing_id)
    if not showing:
        raise HTTPException(status_code=404, detail="Showing not found")
    return showing
