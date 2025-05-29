from sqlmodel import Session, select, and_
from datetime import datetime
from typing import List, Optional
from .models import Booking, BookingCreate, BookingStatus, BookingSearchParams, BookingWithDetails
from modules.service.services import get_service
from modules.customer.services import get_profile as get_customer_profile
from modules.provider.services import get_profile as get_provider_profile

def create_booking(session: Session, booking_data: BookingCreate) -> Booking:
    # Verify service exists and is available
    service = get_service(session, booking_data.service_id)
    if not service:
        raise ValueError("Service not found")
    if not service.is_available:
        raise ValueError("Service is not available")

    # Verify customer exists
    customer = get_customer_profile(session, booking_data.customer_id)
    if not customer:
        raise ValueError("Customer not found")

    # Create booking
    db_booking = Booking(**booking_data.dict())
    session.add(db_booking)
    session.commit()
    session.refresh(db_booking)
    return db_booking

def get_booking(session: Session, booking_id: int) -> Optional[Booking]:
    statement = select(Booking).where(Booking.id == booking_id)
    return session.exec(statement).first()

def update_booking_status(
    session: Session,
    booking_id: int,
    status: BookingStatus,
    notes: Optional[str] = None
) -> Optional[Booking]:
    booking = get_booking(session, booking_id)
    if booking:
        booking.status = status
        if notes:
            booking.notes = notes
        booking.updated_at = datetime.utcnow()
        session.add(booking)
        session.commit()
        session.refresh(booking)
    return booking

def cancel_booking(session: Session, booking_id: int, notes: Optional[str] = None) -> Optional[Booking]:
    booking = get_booking(session, booking_id)
    if not booking:
        return None
    
    if booking.status in [BookingStatus.COMPLETED, BookingStatus.CANCELLED]:
        raise ValueError("Cannot cancel a completed or already cancelled booking")
    
    return update_booking_status(session, booking_id, BookingStatus.CANCELLED, notes)

def complete_booking(session: Session, booking_id: int, notes: Optional[str] = None) -> Optional[Booking]:
    booking = get_booking(session, booking_id)
    if not booking:
        return None
    
    if booking.status != BookingStatus.CONFIRMED:
        raise ValueError("Only confirmed bookings can be marked as completed")
    
    return update_booking_status(session, booking_id, BookingStatus.COMPLETED, notes)

def search_bookings(session: Session, params: BookingSearchParams) -> List[Booking]:
    query = select(Booking)

    if params.status:
        query = query.where(Booking.status == params.status)
    
    if params.start_date:
        query = query.where(Booking.booking_date >= params.start_date)
    
    if params.end_date:
        query = query.where(Booking.booking_date <= params.end_date)
    
    if params.service_id:
        query = query.where(Booking.service_id == params.service_id)
    
    if params.customer_id:
        query = query.where(Booking.customer_id == params.customer_id)
    
    if params.provider_id:
        query = query.join(Booking.service).where(Booking.service.provider_id == params.provider_id)

    return session.exec(query).all()

def get_customer_bookings(
    session: Session,
    customer_id: int,
    status: Optional[BookingStatus] = None
) -> List[Booking]:
    query = select(Booking).where(Booking.customer_id == customer_id)
    if status:
        query = query.where(Booking.status == status)
    return session.exec(query).all()

def get_provider_bookings(
    session: Session,
    provider_id: int,
    status: Optional[BookingStatus] = None
) -> List[Booking]:
    query = (
        select(Booking)
        .join(Booking.service)
        .where(Booking.service.provider_id == provider_id)
    )
    if status:
        query = query.where(Booking.status == status)
    return session.exec(query).all()

def get_booking_stats(session: Session, provider_id: int) -> dict:
    provider = get_provider_profile(session, provider_id)
    if not provider:
        raise ValueError("Provider not found")

    # Get all bookings for provider's services
    bookings = get_provider_bookings(session, provider_id)
    
    # Calculate statistics
    total_bookings = len(bookings)
    completed_bookings = [b for b in bookings if b.status == BookingStatus.COMPLETED]
    cancelled_bookings = [b for b in bookings if b.status == BookingStatus.CANCELLED]
    pending_bookings = [b for b in bookings if b.status == BookingStatus.PENDING]
    
    # Calculate revenue
    total_revenue = sum(b.total_price for b in completed_bookings)
    
    # Calculate completion rate
    completion_rate = len(completed_bookings) / total_bookings if total_bookings > 0 else 0
    
    # Calculate cancellation rate
    cancellation_rate = len(cancelled_bookings) / total_bookings if total_bookings > 0 else 0

    return {
        "total_bookings": total_bookings,
        "completed_bookings": len(completed_bookings),
        "cancelled_bookings": len(cancelled_bookings),
        "pending_bookings": len(pending_bookings),
        "total_revenue": total_revenue,
        "completion_rate": completion_rate,
        "cancellation_rate": cancellation_rate
    } 