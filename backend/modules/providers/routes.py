from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from typing import List
from .models import ProviderCreate, ProviderUpdate, ProviderInDB, BusinessDetails
from .service import (
    create_provider,
    update_business_details,
    get_provider,
    get_provider_by_email,
    update_provider,
    delete_provider,
    list_providers,
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    verify_token
)

router = APIRouter(tags=["providers"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_provider(token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if not token_data or token_data.get("user_type") != "provider":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    provider = get_provider_by_email(token_data.get("sub"))
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider not found"
        )
    return provider

@router.post("/register", response_model=dict)
def register_provider(provider: ProviderCreate):
    """Step 1: Register a new provider with basic info"""
    # Check if provider already exists
    if get_provider_by_email(provider.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new provider
    provider.password = get_password_hash(provider.password)
    provider_obj = provider
    provider = create_provider(provider_obj)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": provider.email, "user_type": "provider", "provider_id": provider.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login for providers"""
    provider = get_provider_by_email(form_data.username)
    print("Provider from DB:", provider)
    print("Password from form:", form_data.password)
    if not provider:
        print("Provider not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Debug password check
    password_check = verify_password(form_data.password, provider.password)
    print("Password check result:", password_check)
    if not password_check:
        print("Password does not match")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not provider.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Provider account is inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": provider.email, "user_type": "provider", "provider_id": provider.id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/{provider_id}/business-details", response_model=ProviderInDB)
async def add_business_details(
    provider_id: str,
    business_details: BusinessDetails,
    current_user: ProviderInDB = Depends(get_current_provider)
):
    """Step 2: Add business details to an existing provider"""
    # Verify the provider exists and matches the current user
    provider = get_provider(provider_id)
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider not found"
        )
    
    if provider.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this provider"
        )
    
    return update_business_details(provider_id, business_details)

@router.get("/me", response_model=ProviderInDB)
async def get_current_provider(current_user: ProviderInDB = Depends(get_current_provider)):
    """Get current provider's details"""
    return current_user

@router.get("/{provider_id}", response_model=ProviderInDB)
async def get_provider_details(provider_id: str):
    """Get provider details by ID"""
    provider = get_provider(provider_id)
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider not found"
        )
    return provider

@router.put("/{provider_id}", response_model=ProviderInDB)
async def update_provider_details(
    provider_id: str,
    provider_update: ProviderUpdate,
    current_user: ProviderInDB = Depends(get_current_provider)
):
    """Update provider details"""
    # Verify the provider exists and matches the current user
    provider = get_provider(provider_id)
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider not found"
        )
    
    if provider.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this provider"
        )
    
    updated_provider = update_provider(provider_id, provider_update)
    if not updated_provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider not found"
        )
    return updated_provider

@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_provider_account(
    provider_id: str,
    current_user: ProviderInDB = Depends(get_current_provider)
):
    """Delete provider account"""
    # Verify the provider exists and matches the current user
    provider = get_provider(provider_id)
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider not found"
        )
    
    if provider.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this provider"
        )
    
    success = delete_provider(provider_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider not found"
        )

@router.get("/", response_model=List[ProviderInDB])
async def get_all_providers(skip: int = 0, limit: int = 100):
    """List all providers"""
    return list_providers(skip=skip, limit=limit) 