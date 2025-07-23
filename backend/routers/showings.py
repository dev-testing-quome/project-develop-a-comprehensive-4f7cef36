from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Showing, ShowingCreate, ShowingUpdate
from ..services import showing_service

router = APIRouter(prefix="/api/showings", tags=["Showings"])

@router.post("", response_model=Showing, status_code=status.HTTP_201_CREATED)
def create_showing(showing: ShowingCreate, db: Session = Depends(get_db)):
    return showing_service.create(db, showing)

@router.get("/{showing_id}", response_model=Showing)
def get_showing(showing_id: int, db: Session = Depends(get_db)):
    showing = showing_service.get(db, showing_id)
    if not showing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Showing not found")
    return showing

@router.put("/{showing_id}", response_model=Showing)
def update_showing(showing_id: int, showing: ShowingUpdate, db: Session = Depends(get_db)):
    db_showing = showing_service.get(db, showing_id)
    if not db_showing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Showing not found")
    return showing_service.update(db, db_showing, showing)

@router.delete("/{showing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_showing(showing_id: int, db: Session = Depends(get_db)):
    showing_service.delete(db, showing_id)
