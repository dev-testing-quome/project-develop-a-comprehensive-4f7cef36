from sqlalchemy.orm import Session
from schemas import UserCreate, User
from models import User as UserModel

def create_user(db: Session, user: UserCreate) -> User:
    db_user = UserModel(username=user.username, email=user.email, password=user.password) # Add password hashing here
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User.from_orm(db_user)

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(UserModel).filter(UserModel.id == user_id).first()
