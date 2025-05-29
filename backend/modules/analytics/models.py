from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime

class ProviderAnalytics(SQLModel):
    provider_id: int
    total_services: int
    total_bookings: int
    completed_bookings: int
    cancelled_bookings: int
    total_revenue: float
    average_rating: float
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None

class ServiceAnalytics(SQLModel):
    service_id: int
    total_bookings: int
    completed_bookings: int
    cancelled_bookings: int
    total_revenue: float
    average_rating: float
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None

class PlatformAnalytics(SQLModel):
    total_users: int
    total_providers: int
    total_customers: int
    total_services: int
    total_bookings: int
    total_revenue: float
    average_rating: float
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None 