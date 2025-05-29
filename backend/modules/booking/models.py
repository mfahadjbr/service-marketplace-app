from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from enum import Enum

class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class BookingBase(SQLModel):
    service_id: int = Field(foreign_key="service.id")
    customer_id: int = Field(foreign_key="customerprofile.id")
    booking_date: datetime
    status: str
    notes: Optional[str] = None
    total_price: float

class Booking(BookingBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    service: Optional["Service"] = Relationship(back_populates="bookings")
    customer: Optional["CustomerProfile"] = Relationship(back_populates="bookings")
    review: Optional["Review"] = Relationship(back_populates="booking")

class BookingCreate(BookingBase):
    pass

class BookingRead(BookingBase):
    id: int
    created_at: datetime
    updated_at: datetime
    service: Optional["ServiceRead"] = None
    customer: Optional["CustomerProfileRead"] = None
    review: Optional["ReviewRead"] = None

class BookingWithDetails(BookingRead):
    service: "ServiceRead"
    customer: "CustomerProfileRead"

class BookingSearchParams(SQLModel):
    status: Optional[BookingStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    service_id: Optional[int] = None
    customer_id: Optional[int] = None
    provider_id: Optional[int] = None

if TYPE_CHECKING:
    from modules.service.models import Service, ServiceRead
    from modules.customer.models import CustomerProfile, CustomerProfileRead
    from modules.review.models import Review, ReviewRead 