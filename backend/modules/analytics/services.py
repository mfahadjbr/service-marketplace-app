from sqlmodel import Session, select
from datetime import datetime
from typing import Optional
from .models import ProviderAnalytics, ServiceAnalytics, PlatformAnalytics
from modules.provider.models import ProviderProfile
from modules.service.models import Service
from modules.booking.models import Booking, BookingStatus
from modules.auth.models import User, UserRole

def get_provider_analytics(session: Session, provider_id: int, period_start: Optional[datetime] = None, period_end: Optional[datetime] = None) -> ProviderAnalytics:
    provider = session.exec(select(ProviderProfile).where(ProviderProfile.id == provider_id)).first()
    if not provider:
        raise ValueError("Provider not found")
    services = provider.services
    total_services = len(services)
    bookings = []
    for service in services:
        for booking in service.bookings:
            if period_start and booking.created_at < period_start:
                continue
            if period_end and booking.created_at > period_end:
                continue
            bookings.append(booking)
    total_bookings = len(bookings)
    completed_bookings = [b for b in bookings if b.status == BookingStatus.COMPLETED]
    cancelled_bookings = [b for b in bookings if b.status == BookingStatus.CANCELLED]
    total_revenue = sum(b.total_price for b in completed_bookings)
    ratings = [service.provider.rating for service in services if hasattr(service.provider, 'rating') and service.provider.rating is not None]
    average_rating = sum(ratings) / len(ratings) if ratings else 0
    return ProviderAnalytics(
        provider_id=provider_id,
        total_services=total_services,
        total_bookings=total_bookings,
        completed_bookings=len(completed_bookings),
        cancelled_bookings=len(cancelled_bookings),
        total_revenue=total_revenue,
        average_rating=average_rating,
        period_start=period_start,
        period_end=period_end
    )

def get_service_analytics(session: Session, service_id: int, period_start: Optional[datetime] = None, period_end: Optional[datetime] = None) -> ServiceAnalytics:
    service = session.exec(select(Service).where(Service.id == service_id)).first()
    if not service:
        raise ValueError("Service not found")
    bookings = [b for b in service.bookings if (not period_start or b.created_at >= period_start) and (not period_end or b.created_at <= period_end)]
    total_bookings = len(bookings)
    completed_bookings = [b for b in bookings if b.status == BookingStatus.COMPLETED]
    cancelled_bookings = [b for b in bookings if b.status == BookingStatus.CANCELLED]
    total_revenue = sum(b.total_price for b in completed_bookings)
    ratings = [service.provider.rating] if hasattr(service.provider, 'rating') and service.provider.rating is not None else []
    average_rating = sum(ratings) / len(ratings) if ratings else 0
    return ServiceAnalytics(
        service_id=service_id,
        total_bookings=total_bookings,
        completed_bookings=len(completed_bookings),
        cancelled_bookings=len(cancelled_bookings),
        total_revenue=total_revenue,
        average_rating=average_rating,
        period_start=period_start,
        period_end=period_end
    )

def get_platform_analytics(session: Session, period_start: Optional[datetime] = None, period_end: Optional[datetime] = None) -> PlatformAnalytics:
    total_users = session.exec(select(User)).count()
    total_providers = session.exec(select(User).where(User.role == UserRole.PROVIDER)).count()
    total_customers = session.exec(select(User).where(User.role == UserRole.CUSTOMER)).count()
    total_services = session.exec(select(Service)).count()
    bookings = session.exec(select(Booking)).all()
    if period_start:
        bookings = [b for b in bookings if b.created_at >= period_start]
    if period_end:
        bookings = [b for b in bookings if b.created_at <= period_end]
    total_bookings = len(bookings)
    completed_bookings = [b for b in bookings if b.status == BookingStatus.COMPLETED]
    total_revenue = sum(b.total_price for b in completed_bookings)
    ratings = []
    for service in session.exec(select(Service)).all():
        if hasattr(service.provider, 'rating') and service.provider.rating is not None:
            ratings.append(service.provider.rating)
    average_rating = sum(ratings) / len(ratings) if ratings else 0
    return PlatformAnalytics(
        total_users=total_users,
        total_providers=total_providers,
        total_customers=total_customers,
        total_services=total_services,
        total_bookings=total_bookings,
        total_revenue=total_revenue,
        average_rating=average_rating,
        period_start=period_start,
        period_end=period_end
    ) 