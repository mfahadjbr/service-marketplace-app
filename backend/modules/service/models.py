from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from modules.provider.models import ProviderProfile

class ServiceBase(SQLModel):
    title: str
    description: str
    price: float
    duration: int  # in minutes
    category_id: int = Field(foreign_key="category.id")
    is_available: bool = Field(default=True)

class Service(ServiceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    provider_id: int = Field(foreign_key="providerprofile.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    provider: Optional["ProviderProfile"] = Relationship(back_populates="services")
    bookings: List["Booking"] = Relationship(back_populates="service")
    category: Optional["Category"] = Relationship(back_populates="services")

class ServiceCreate(ServiceBase):
    pass

class ServiceRead(ServiceBase):
    id: int
    provider_id: int
    created_at: datetime
    updated_at: datetime
    provider: Optional["ProviderProfile"] = None
    category: Optional["Category"] = None
    bookings: List["Booking"] = []

class ServiceWithProvider(ServiceRead):
    provider: ProviderProfile

class ServiceSearchParams(SQLModel):
    category_id: Optional[int] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_rating: Optional[float] = None
    is_available: Optional[bool] = None
    search_query: Optional[str] = None
    sort_by: Optional[str] = None  # price, rating, popularity
    sort_order: Optional[str] = None  # asc, desc

if TYPE_CHECKING:
    from modules.booking.models import Booking
    from modules.category.models import Category 