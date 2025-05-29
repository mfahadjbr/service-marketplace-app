from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from ..auth.services import get_current_user
from ..auth.models import User
from ..database import get_session
from .models import Location, LocationCreate, LocationRead, LocationSearchParams
from .services import (
    create_location,
    get_location,
    update_location,
    delete_location,
    search_locations,
    get_all_locations
)

router = APIRouter()

@router.post("/", response_model=LocationRead)
def create_location_endpoint(
    location_data: LocationCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create locations")
    return create_location(session, location_data)

@router.get("/", response_model=List[LocationRead])
def get_all_locations_endpoint(
    active_only: bool = Query(False),
    session: Session = Depends(get_session)
):
    return get_all_locations(session, active_only)

@router.get("/search/", response_model=List[LocationRead])
def search_locations_endpoint(
    city: Optional[str] = None,
    state: Optional[str] = None,
    country: Optional[str] = None,
    is_active: Optional[bool] = None,
    query: Optional[str] = None,
    session: Session = Depends(get_session)
):
    params = LocationSearchParams(
        city=city,
        state=state,
        country=country,
        is_active=is_active,
        query=query
    )
    return search_locations(session, params)

@router.get("/{location_id}", response_model=LocationRead)
def get_location_endpoint(
    location_id: int,
    session: Session = Depends(get_session)
):
    location = get_location(session, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.put("/{location_id}", response_model=LocationRead)
def update_location_endpoint(
    location_id: int,
    location_data: LocationCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update locations")
    location = update_location(session, location_id, location_data)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.delete("/{location_id}")
def delete_location_endpoint(
    location_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete locations")
    if delete_location(session, location_id):
        return {"message": "Location deleted successfully"}
    raise HTTPException(status_code=404, detail="Location not found") 