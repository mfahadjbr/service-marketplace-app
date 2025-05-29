from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from datetime import timedelta
from typing import Optional
from app.database import get_session
from . import services
from .models import UserCreate, UserRead, UserRole

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Provider registration
@router.post("/provider/register", response_model=UserRead)
def register_provider(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    auth_service = services.AuthService(session)
    # Check if user already exists
    if auth_service.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # Set role as provider
    user_data.role = UserRole.PROVIDER
    return auth_service.create_user(user_data)

# Customer registration
@router.post("/customer/register", response_model=UserRead)
def register_customer(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    auth_service = services.AuthService(session)
    # Check if user already exists
    if auth_service.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # Set role as customer
    user_data.role = UserRole.CUSTOMER
    return auth_service.create_user(user_data)

# Login endpoint
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    auth_service = services.AuthService(session)
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=services.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        }
    }

# Get current user
@router.get("/me", response_model=UserRead)
def read_users_me(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    auth_service = services.AuthService(session)
    payload = auth_service.verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = auth_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user 