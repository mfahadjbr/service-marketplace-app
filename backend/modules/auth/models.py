from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    PROVIDER = "provider"
    CUSTOMER = "customer"

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: str
    phone: str
    role: UserRole

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime 