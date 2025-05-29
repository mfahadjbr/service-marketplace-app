from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from app.database import get_session
from modules.auth.services import oauth2_scheme
from . import services
from .models import CustomerProfileCreate, CustomerProfileRead, CustomerDashboard

router = APIRouter()

# Get customer profile
@router.get("/profile", response_model=CustomerProfileRead)
def get_customer_profile(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    auth_service = AuthService(session)
    user = auth_service.get_current_user(token)
    if user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access customer profile"
        )
    
    profile = services.get_profile(session, user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found"
        )
    return profile

# Create customer profile
@router.post("/profile", response_model=CustomerProfileRead)
def create_customer_profile(
    profile_data: CustomerProfileCreate,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    auth_service = AuthService(session)
    user = auth_service.get_current_user(token)
    if user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create customer profile"
        )
    
    existing_profile = services.get_profile(session, user.id)
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer profile already exists"
        )
    
    return services.create_profile(session, user.id, profile_data)

# Update customer profile
@router.put("/profile", response_model=CustomerProfileRead)
def update_customer_profile(
    profile_data: CustomerProfileCreate,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    auth_service = AuthService(session)
    user = auth_service.get_current_user(token)
    if user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update customer profile"
        )
    
    profile = services.update_profile(session, user.id, profile_data)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found"
        )
    return profile

# Get customer dashboard
@router.get("/dashboard", response_model=CustomerDashboard)
def get_customer_dashboard(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    auth_service = AuthService(session)
    user = auth_service.get_current_user(token)
    if user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access customer dashboard"
        )
    
    try:
        return services.get_dashboard(session, user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

# Get customer statistics
@router.get("/stats")
def get_customer_stats(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    auth_service = AuthService(session)
    user = auth_service.get_current_user(token)
    if user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access customer statistics"
        )
    
    try:
        return services.get_customer_stats(session, user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

# Add favorite provider
@router.post("/favorites/{provider_id}")
def add_favorite_provider(
    provider_id: int,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    auth_service = AuthService(session)
    user = auth_service.get_current_user(token)
    if user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add favorite providers"
        )
    
    try:
        if services.add_favorite_provider(session, user.id, provider_id):
            return {"message": "Provider added to favorites"}
        return {"message": "Provider already in favorites"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

# Remove favorite provider
@router.delete("/favorites/{provider_id}")
def remove_favorite_provider(
    provider_id: int,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    auth_service = AuthService(session)
    user = auth_service.get_current_user(token)
    if user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to remove favorite providers"
        )
    
    try:
        if services.remove_favorite_provider(session, user.id, provider_id):
            return {"message": "Provider removed from favorites"}
        return {"message": "Provider not in favorites"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) 