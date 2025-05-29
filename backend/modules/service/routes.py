from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from ..auth.services import get_current_user
from ..auth.models import User
from ..database import get_session
from .models import Service, ServiceCreate, ServiceRead, ServiceSearchParams, ServiceWithProvider
from .services import (
    create_service,
    get_service,
    update_service,
    delete_service,
    get_provider_services,
    search_services,
    get_featured_services,
    get_services_by_category,
    toggle_service_availability,
    get_service_stats
)

router = APIRouter()

@router.post("/", response_model=ServiceRead)
def create_service_endpoint(
    service_data: ServiceCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "provider":
        raise HTTPException(status_code=403, detail="Only providers can create services")
    return create_service(session, current_user.id, service_data)

@router.get("/{service_id}", response_model=ServiceRead)
def get_service_endpoint(
    service_id: int,
    session: Session = Depends(get_session)
):
    service = get_service(session, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.put("/{service_id}", response_model=ServiceRead)
def update_service_endpoint(
    service_id: int,
    service_data: ServiceCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    service = get_service(session, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    if service.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this service")
    return update_service(session, service_id, service_data)

@router.delete("/{service_id}")
def delete_service_endpoint(
    service_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    service = get_service(session, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    if service.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this service")
    if delete_service(session, service_id):
        return {"message": "Service deleted successfully"}
    raise HTTPException(status_code=500, detail="Failed to delete service")

@router.get("/provider/{provider_id}", response_model=List[ServiceRead])
def get_provider_services_endpoint(
    provider_id: int,
    session: Session = Depends(get_session)
):
    return get_provider_services(session, provider_id)

@router.get("/search/", response_model=List[ServiceWithProvider])
def search_services_endpoint(
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_available: Optional[bool] = None,
    search_query: Optional[str] = None,
    min_rating: Optional[float] = None,
    sort_by: Optional[str] = Query(None, regex="^(price|rating)$"),
    sort_order: Optional[str] = Query(None, regex="^(asc|desc)$"),
    session: Session = Depends(get_session)
):
    params = ServiceSearchParams(
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        is_available=is_available,
        search_query=search_query,
        min_rating=min_rating,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return search_services(session, params)

@router.get("/featured/", response_model=List[ServiceWithProvider])
def get_featured_services_endpoint(
    limit: int = Query(5, ge=1, le=20),
    session: Session = Depends(get_session)
):
    return get_featured_services(session, limit)

@router.get("/category/{category_id}", response_model=List[ServiceRead])
def get_services_by_category_endpoint(
    category_id: int,
    session: Session = Depends(get_session)
):
    return get_services_by_category(session, category_id)

@router.post("/{service_id}/toggle-availability", response_model=ServiceRead)
def toggle_service_availability_endpoint(
    service_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    service = get_service(session, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    if service.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this service")
    return toggle_service_availability(session, service_id)

@router.get("/{service_id}/stats")
def get_service_stats_endpoint(
    service_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    service = get_service(session, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    if service.provider_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view these stats")
    return get_service_stats(session, service_id) 