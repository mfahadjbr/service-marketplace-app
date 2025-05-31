from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from typing import List
from .models import UserCreate, UserUpdate, UserInDB
from .service import (
    create_user,
    get_user_by_email,
    update_user,
    delete_user,
    list_users,
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_user_by_id,
    verify_token
)

router = APIRouter(tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if not token_data or token_data.get("user_type") != "customer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_email(token_data.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.post("/register", response_model=dict)
def register_customer(user: UserCreate):
    """Register a new customer"""
    # Check if user already exists
    if get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user.password = get_password_hash(user.password)
    create_user(user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_type": "customer"},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login for customers"""
    user = get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "user_type": "customer"},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserInDB)
def get_current_user_route(current_user: UserInDB = Depends(get_current_user)):
    """Get current user's details"""
    return current_user

@router.put("/me", response_model=UserInDB)
def update_user_me(
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    updated_user = update_user(current_user["id"], user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_me(current_user: dict = Depends(get_current_user)):
    if not delete_user(current_user["id"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        ) 