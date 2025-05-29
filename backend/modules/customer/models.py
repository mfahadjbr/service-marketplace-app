from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from modules.auth.models import User
from sqlalchemy import Column, JSON

class CustomerProfileBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    address: Optional[str] = None
    phone: Optional[str] = None
    preferences: Optional[dict] = Field(default_factory=dict, sa_column=Column(JSON))

class CustomerProfile(CustomerProfileBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="customer_profile")
    bookings: List["Booking"] = Relationship(back_populates="customer")
    reviews: List["Review"] = Relationship(back_populates="customer")
    favorite_providers: List["ProviderProfile"] = Relationship(back_populates="favorited_by")

class CustomerProfileCreate(CustomerProfileBase):
    pass

class CustomerProfileRead(CustomerProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime
    bookings: List["BookingRead"] = []
    reviews: List["ReviewRead"] = []
    favorite_providers: List["ProviderProfileRead"] = []

class CustomerDashboard(SQLModel):
    active_bookings: int
    past_bookings: int
    favorite_providers: List["ProviderProfileRead"]
    recent_bookings: List["BookingRead"]
    recent_reviews: List["ReviewRead"]

if TYPE_CHECKING:
    from modules.booking.models import Booking, BookingRead
    from modules.review.models import Review, ReviewRead
    from modules.provider.models import ProviderProfile, ProviderProfileRead 