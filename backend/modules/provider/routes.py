from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from app.database import get_session
from modules.auth.services import oauth2_scheme
from . import services
from .models import ProviderProfileCreate, ProviderProfileRead, ProviderDashboard

router = APIRouter()

# Get provider profile
@router.get("/profile", response_model=ProviderProfileRead)
def get_provider_profile(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    auth_service = AuthService(session)
    user = auth_service.get_current_user(token)
    if user.role != "provider":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access provider profile"
        )
    
    provider_service = services.ProviderService(session)
    profile = provider_service.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider profile not found"
        )
    return profile

# Create provider profile
@router.post("/profile", response_model=ProviderProfileRead)
def create_provider_profile(
    profile_data: ProviderProfileCreate,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    auth_service = AuthService(session)
    user = auth_service.get_current_user(token)
    if user.role != "provider":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create provider profile"
        )
    
    provider_service = services.ProviderService(session)
    existing_profile = provider_service.get_profile(user.id)
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provider profile already exists"
        )
    
    return provider_service.create_profile(user.id, profile_data)

# Update provider profile
@router.put("/profile", response_model=ProviderProfileRead)
def update_provider_profile(
    profile_data: ProviderProfileCreate,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    auth_service = AuthService(session)
    user = auth_service.get_current_user(token)
    if user.role != "provider":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update provider profile"
        )
    
    provider_service = services.ProviderService(session)
    profile = provider_service.update_profile(user.id, profile_data)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider profile not found"
        )
    return profile

# Get provider dashboard
@router.get("/dashboard", response_model=ProviderDashboard)
def get_provider_dashboard(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    auth_service = AuthService(session)
    user = auth_service.get_current_user(token)
    if user.role != "provider":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access provider dashboard"
        )
    
    provider_service = services.ProviderService(session)
    try:
        return provider_service.get_dashboard(user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

# Get provider statistics
@router.get("/stats")
def get_provider_stats(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    auth_service = AuthService(session)
    user = auth_service.get_current_user(token)
    if user.role != "provider":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access provider statistics"
        )
    
    provider_service = services.ProviderService(session)
    try:
        return provider_service.get_provider_stats(user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) 