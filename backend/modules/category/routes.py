from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from ..auth.services import get_current_user
from ..auth.models import User
from ..database import get_session
from .models import (
    Category,
    CategoryCreate,
    CategoryRead,
    CategoryWithChildren,
    CategoryWithServices,
    CategoryStats
)
from .services import (
    create_category,
    get_category,
    update_category,
    delete_category,
    get_all_categories,
    get_category_with_children,
    get_category_with_services,
    get_category_stats
)

router = APIRouter()

@router.post("/", response_model=CategoryRead)
def create_category_endpoint(
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create categories")
    return create_category(session, category_data)

@router.get("/", response_model=List[CategoryRead])
def get_all_categories_endpoint(
    active_only: bool = Query(False),
    session: Session = Depends(get_session)
):
    return get_all_categories(session, active_only)

@router.get("/{category_id}", response_model=CategoryRead)
def get_category_endpoint(
    category_id: int,
    session: Session = Depends(get_session)
):
    category = get_category(session, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=CategoryRead)
def update_category_endpoint(
    category_id: int,
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update categories")
    category = update_category(session, category_id, category_data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{category_id}")
def delete_category_endpoint(
    category_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete categories")
    if delete_category(session, category_id):
        return {"message": "Category deleted successfully"}
    raise HTTPException(status_code=404, detail="Category not found")

@router.get("/{category_id}/children", response_model=CategoryWithChildren)
def get_category_with_children_endpoint(
    category_id: int,
    session: Session = Depends(get_session)
):
    category = get_category_with_children(session, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/{category_id}/services", response_model=CategoryWithServices)
def get_category_with_services_endpoint(
    category_id: int,
    session: Session = Depends(get_session)
):
    category = get_category_with_services(session, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/{category_id}/stats", response_model=CategoryStats)
def get_category_stats_endpoint(
    category_id: int,
    session: Session = Depends(get_session)
):
    stats = get_category_stats(session, category_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Category not found")
    return stats 