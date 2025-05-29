from sqlmodel import Session, select
from datetime import datetime
from typing import List, Optional
from .models import CustomerProfile, CustomerProfileCreate, CustomerDashboard
from modules.booking.models import Booking, BookingStatus
from modules.review.models import Review
from modules.provider.models import ProviderProfile

def create_profile(session: Session, user_id: int, profile_data: CustomerProfileCreate) -> CustomerProfile:
    db_profile = CustomerProfile(
        user_id=user_id,
        **profile_data.dict()
    )
    session.add(db_profile)
    session.commit()
    session.refresh(db_profile)
    return db_profile

def get_profile(session: Session, user_id: int) -> Optional[CustomerProfile]:
    statement = select(CustomerProfile).where(CustomerProfile.user_id == user_id)
    return session.exec(statement).first()

def update_profile(session: Session, user_id: int, profile_data: CustomerProfileCreate) -> Optional[CustomerProfile]:
    profile = get_profile(session, user_id)
    if profile:
        for key, value in profile_data.dict().items():
            setattr(profile, key, value)
        profile.updated_at = datetime.utcnow()
        session.add(profile)
        session.commit()
        session.refresh(profile)
    return profile

def get_dashboard(session: Session, user_id: int) -> CustomerDashboard:
    profile = get_profile(session, user_id)
    if not profile:
        raise ValueError("Customer profile not found")

    # Get active bookings
    active_bookings = session.exec(
        select(Booking)
        .where(
            Booking.customer_id == profile.id,
            Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED])
        )
    ).all()

    # Get past bookings
    past_bookings = session.exec(
        select(Booking)
        .where(
            Booking.customer_id == profile.id,
            Booking.status.in_([BookingStatus.COMPLETED, BookingStatus.CANCELLED])
        )
    ).all()

    # Get favorite providers
    favorite_providers = session.exec(
        select(ProviderProfile)
        .where(ProviderProfile.id.in_(profile.preferences.get("favorite_providers", [])))
    ).all()

    # Get recent reviews
    recent_reviews = session.exec(
        select(Review)
        .where(Review.customer_id == profile.id)
        .order_by(Review.created_at.desc())
        .limit(5)
    ).all()

    return CustomerDashboard(
        active_bookings=len(active_bookings),
        past_bookings=len(past_bookings),
        favorite_providers=favorite_providers,
        recent_bookings=active_bookings[:5],
        recent_reviews=recent_reviews
    )

def get_customer_stats(session: Session, user_id: int) -> dict:
    profile = get_profile(session, user_id)
    if not profile:
        raise ValueError("Customer profile not found")

    # Get all bookings
    all_bookings = session.exec(
        select(Booking)
        .where(Booking.customer_id == profile.id)
    ).all()

    # Get completed bookings
    completed_bookings = [b for b in all_bookings if b.status == BookingStatus.COMPLETED]

    # Get total spent
    total_spent = sum(b.total_price for b in completed_bookings)

    # Get average rating given
    customer_reviews = session.exec(
        select(Review)
        .where(Review.customer_id == profile.id)
    ).all()
    average_rating_given = sum(r.rating for r in customer_reviews) / len(customer_reviews) if customer_reviews else 0

    return {
        "total_bookings": len(all_bookings),
        "completed_bookings": len(completed_bookings),
        "total_spent": total_spent,
        "average_rating_given": average_rating_given,
        "total_reviews_given": len(customer_reviews)
    }

def add_favorite_provider(session: Session, user_id: int, provider_id: int) -> bool:
    profile = get_profile(session, user_id)
    if not profile:
        raise ValueError("Customer profile not found")

    favorite_providers = profile.preferences.get("favorite_providers", [])
    if provider_id not in favorite_providers:
        favorite_providers.append(provider_id)
        profile.preferences["favorite_providers"] = favorite_providers
        profile.updated_at = datetime.utcnow()
        session.add(profile)
        session.commit()
        return True
    return False

def remove_favorite_provider(session: Session, user_id: int, provider_id: int) -> bool:
    profile = get_profile(session, user_id)
    if not profile:
        raise ValueError("Customer profile not found")

    favorite_providers = profile.preferences.get("favorite_providers", [])
    if provider_id in favorite_providers:
        favorite_providers.remove(provider_id)
        profile.preferences["favorite_providers"] = favorite_providers
        profile.updated_at = datetime.utcnow()
        session.add(profile)
        session.commit()
        return True
    return False 