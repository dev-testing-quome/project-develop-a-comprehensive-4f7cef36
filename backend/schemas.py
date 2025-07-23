from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ClientBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    properties: list[int] = []
    showings: list[int] = []

    class Config:
        orm_mode = True

class PropertyBase(BaseModel):
    address: str
    city: str
    state: str
    zip_code: str
    price: Optional[int] = None
    description: Optional[str] = None
    mls_id: Optional[str] = None

class PropertyCreate(PropertyBase):
    client_id: int

class PropertyUpdate(PropertyBase):
    pass

class Property(PropertyBase):
    id: int
    client_id: int
    created_at: datetime
    updated_at: datetime
    showings: list[int] = []

    class Config:
        orm_mode = True

class ShowingBase(BaseModel):
    property_id: int
    client_id: int
    scheduled_time: datetime
    notes: Optional[str] = None
    confirmed: Optional[bool] = False

class ShowingCreate(ShowingBase):
    pass

class ShowingUpdate(ShowingBase):
    pass

class Showing(ShowingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
