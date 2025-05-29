from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class LocationBase(SQLModel):
    name: str
    address: str
    city: str
    state: str
    country: str
    postal_code: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: bool = Field(default=True)

class Location(LocationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    services: List["Service"] = Relationship(back_populates="location")
    providers: List["ProviderProfile"] = Relationship(back_populates="location")

class LocationCreate(LocationBase):
    pass

class LocationRead(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

class LocationSearchParams(SQLModel):
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = None
    query: Optional[str] = None

if TYPE_CHECKING:
    from modules.service.models import Service
    from modules.provider.models import ProviderProfile 