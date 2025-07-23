from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PropertyCreate(BaseModel):
    owner_id: int
    address: str
    price: int
    description: str

class Property(BaseModel):
    id: int
    owner_id: int
    address: str
    price: int
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ShowingCreate(BaseModel):
    property_id: int
    client_id: int
    date_time: datetime

class Showing(BaseModel):
    id: int
    property_id: int
    client_id: int
    date_time: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
