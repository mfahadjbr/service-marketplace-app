from sqlmodel import Session, select
from datetime import datetime, timedelta
from typing import List, Optional
from .models import ProviderProfile, ProviderProfileCreate, ProviderDashboard
from modules.booking.models import Booking, BookingStatus
from modules.review.models import Review

class ProviderService:
    def __init__(self, session: Session):
        self.session = session

    def create_profile(self, user_id: int, profile_data: ProviderProfileCreate) -> ProviderProfile:
        db_profile = ProviderProfile(
            user_id=user_id,
            **profile_data.dict()
        )
        self.session.add(db_profile)
        self.session.commit()
        self.session.refresh(db_profile)
        return db_profile

    def get_profile(self, user_id: int) -> Optional[ProviderProfile]:
        statement = select(ProviderProfile).where(ProviderProfile.user_id == user_id)
        return self.session.exec(statement).first()

    def update_profile(self, user_id: int, profile_data: ProviderProfileCreate) -> Optional[ProviderProfile]:
        profile = self.get_profile(user_id)
        if profile:
            for key, value in profile_data.dict().items():
                setattr(profile, key, value)
            profile.updated_at = datetime.utcnow()
            self.session.add(profile)
            self.session.commit()
            self.session.refresh(profile)
        return profile

    def get_dashboard(self, user_id: int) -> ProviderDashboard:
        profile = self.get_profile(user_id)
        if not profile:
            raise ValueError("Provider profile not found")

        # Get today's date range
        today = datetime.utcnow().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())

        # Get today's earnings
        today_bookings = self.session.exec(
            select(Booking)
            .where(
                Booking.provider_id == profile.id,
                Booking.status == BookingStatus.COMPLETED,
                Booking.created_at >= today_start,
                Booking.created_at <= today_end
            )
        ).all()
        today_earnings = sum(booking.total_price for booking in today_bookings)

        # Get upcoming bookings
        upcoming_bookings = self.session.exec(
            select(Booking)
            .where(
                Booking.provider_id == profile.id,
                Booking.status == BookingStatus.CONFIRMED,
                Booking.booking_date > datetime.utcnow()
            )
        ).all()

        # Get recent reviews
        recent_reviews = self.session.exec(
            select(Review)
            .where(Review.provider_id == profile.id)
            .order_by(Review.created_at.desc())
            .limit(5)
        ).all()

        return ProviderDashboard(
            today_earnings=today_earnings,
            upcoming_bookings=len(upcoming_bookings),
            average_rating=profile.rating,
            total_reviews=profile.total_reviews,
            recent_bookings=upcoming_bookings[:5],
            recent_reviews=recent_reviews
        )

    def get_provider_stats(self, user_id: int) -> dict:
        profile = self.get_profile(user_id)
        if not profile:
            raise ValueError("Provider profile not found")

        # Get total bookings
        total_bookings = self.session.exec(
            select(Booking)
            .where(Booking.provider_id == profile.id)
        ).all()

        # Get completed bookings
        completed_bookings = [b for b in total_bookings if b.status == BookingStatus.COMPLETED]

        # Get total earnings
        total_earnings = sum(b.total_price for b in completed_bookings)

        return {
            "total_bookings": len(total_bookings),
            "completed_bookings": len(completed_bookings),
            "total_earnings": total_earnings,
            "average_rating": profile.rating,
            "total_reviews": profile.total_reviews
        } 