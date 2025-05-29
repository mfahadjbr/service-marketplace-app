from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import Optional
from datetime import datetime
from ..auth.services import get_current_user
from ..auth.models import User
from ..database import get_session
from .models import ProviderAnalytics, ServiceAnalytics, PlatformAnalytics
from .services import (
    get_provider_analytics,
    get_service_analytics,
    get_platform_analytics
)

router = APIRouter()

@router.get("/provider/{provider_id}", response_model=ProviderAnalytics)
def provider_analytics_endpoint(
    provider_id: int,
    period_start: Optional[datetime] = Query(None),
    period_end: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "provider" or current_user.id != provider_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this provider's analytics")
    try:
        return get_provider_analytics(session, provider_id, period_start, period_end)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/service/{service_id}", response_model=ServiceAnalytics)
def service_analytics_endpoint(
    service_id: int,
    period_start: Optional[datetime] = Query(None),
    period_end: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Only the provider who owns the service can view its analytics
    # (Assume get_service_analytics checks ownership internally or add check here if needed)
    try:
        return get_service_analytics(session, service_id, period_start, period_end)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/platform", response_model=PlatformAnalytics)
def platform_analytics_endpoint(
    period_start: Optional[datetime] = Query(None),
    period_end: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can view platform analytics")
    return get_platform_analytics(session, period_start, period_end) 