from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from modules.auth.models import User

class ProviderProfileBase(SQLModel):
    business_name: str
    service_type: str
    hourly_rate: float
    location: str
    working_hours: str
    description: str
    is_verified: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id")
    bio: Optional[str] = None
    rating: Optional[float] = None

class ProviderProfile(ProviderProfileBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    services: List["Service"] = Relationship(back_populates="provider")
    bookings: List["Booking"] = Relationship(back_populates="provider")
    reviews: List["Review"] = Relationship(back_populates="provider")
    favorited_by: List["CustomerProfile"] = Relationship(back_populates="favorite_providers")

    # Relationships
    user: User = Relationship(back_populates="provider_profile")

class ProviderProfileCreate(ProviderProfileBase):
    pass

class ProviderProfileRead(ProviderProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime
    services: List["Service"] = []
    bookings: List["BookingRead"] = []
    reviews: List["ReviewRead"] = []
    favorited_by: List["CustomerProfileRead"] = []

class ProviderDashboard(SQLModel):
    today_earnings: float
    upcoming_bookings: int
    average_rating: float
    total_reviews: int
    recent_bookings: List["BookingRead"]
    recent_reviews: List["ReviewRead"]

if TYPE_CHECKING:
    from modules.service.models import Service
    from modules.booking.models import Booking, BookingRead
    from modules.review.models import Review, ReviewRead
    from modules.customer.models import CustomerProfile, CustomerProfileRead 