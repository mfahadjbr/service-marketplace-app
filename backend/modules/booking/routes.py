from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from datetime import datetime
from ..auth.services import get_current_user
from ..auth.models import User
from ..database import get_session
from .models import (
    Booking,
    BookingCreate,
    BookingRead,
    BookingWithDetails,
    BookingStatus,
    BookingSearchParams
)
from .services import (
    create_booking,
    get_booking,
    update_booking_status,
    cancel_booking,
    complete_booking,
    search_bookings,
    get_customer_bookings,
    get_provider_bookings,
    get_booking_stats
)

router = APIRouter()

@router.post("/", response_model=BookingRead)
def create_booking_endpoint(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "customer":
        raise HTTPException(status_code=403, detail="Only customers can create bookings")
    try:
        return create_booking(session, booking_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{booking_id}", response_model=BookingWithDetails)
def get_booking_endpoint(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    booking = get_booking(session, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Check authorization
    if current_user.role == "customer" and booking.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this booking")
    if current_user.role == "provider" and booking.service.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this booking")
    
    return booking

@router.put("/{booking_id}/status", response_model=BookingRead)
def update_booking_status_endpoint(
    booking_id: int,
    status: BookingStatus,
    notes: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    booking = get_booking(session, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Check authorization
    if current_user.role == "customer" and booking.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this booking")
    if current_user.role == "provider" and booking.service.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this booking")
    
    try:
        return update_booking_status(session, booking_id, status, notes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{booking_id}/cancel", response_model=BookingRead)
def cancel_booking_endpoint(
    booking_id: int,
    notes: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    booking = get_booking(session, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Check authorization
    if current_user.role == "customer" and booking.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this booking")
    if current_user.role == "provider" and booking.service.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this booking")
    
    try:
        return cancel_booking(session, booking_id, notes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{booking_id}/complete", response_model=BookingRead)
def complete_booking_endpoint(
    booking_id: int,
    notes: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    booking = get_booking(session, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Only providers can complete bookings
    if current_user.role != "provider" or booking.service.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to complete this booking")
    
    try:
        return complete_booking(session, booking_id, notes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/search/", response_model=List[BookingWithDetails])
def search_bookings_endpoint(
    status: Optional[BookingStatus] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    service_id: Optional[int] = None,
    customer_id: Optional[int] = None,
    provider_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Check authorization
    if current_user.role == "customer" and (customer_id is None or customer_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to search these bookings")
    if current_user.role == "provider" and (provider_id is None or provider_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to search these bookings")
    
    params = BookingSearchParams(
        status=status,
        start_date=start_date,
        end_date=end_date,
        service_id=service_id,
        customer_id=customer_id,
        provider_id=provider_id
    )
    return search_bookings(session, params)

@router.get("/customer/me", response_model=List[BookingWithDetails])
def get_my_bookings_endpoint(
    status: Optional[BookingStatus] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "customer":
        raise HTTPException(status_code=403, detail="Only customers can access their bookings")
    return get_customer_bookings(session, current_user.id, status)

@router.get("/provider/me", response_model=List[BookingWithDetails])
def get_provider_bookings_endpoint(
    status: Optional[BookingStatus] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "provider":
        raise HTTPException(status_code=403, detail="Only providers can access their bookings")
    return get_provider_bookings(session, current_user.id, status)

@router.get("/provider/stats")
def get_provider_booking_stats_endpoint(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "provider":
        raise HTTPException(status_code=403, detail="Only providers can access booking statistics")
    try:
        return get_booking_stats(session, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 