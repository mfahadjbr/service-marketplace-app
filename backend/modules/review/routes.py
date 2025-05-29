from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from ..auth.services import get_current_user
from ..auth.models import User
from ..database import get_session
from .models import Review, ReviewCreate, ReviewRead
from .services import (
    create_review,
    get_review,
    update_review,
    delete_review,
    get_reviews_for_service,
    get_reviews_for_provider,
    get_reviews_for_customer
)

router = APIRouter()

@router.post("/", response_model=ReviewRead)
def create_review_endpoint(
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Only customers can create reviews
    if current_user.role != "customer":
        raise HTTPException(status_code=403, detail="Only customers can create reviews")
    return create_review(session, review_data)

@router.get("/{review_id}", response_model=ReviewRead)
def get_review_endpoint(
    review_id: int,
    session: Session = Depends(get_session)
):
    review = get_review(session, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/{review_id}", response_model=ReviewRead)
def update_review_endpoint(
    review_id: int,
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    review = get_review(session, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if current_user.role != "customer" or review.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this review")
    return update_review(session, review_id, review_data)

@router.delete("/{review_id}")
def delete_review_endpoint(
    review_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    review = get_review(session, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if current_user.role != "customer" or review.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this review")
    if delete_review(session, review_id):
        return {"message": "Review deleted successfully"}
    raise HTTPException(status_code=500, detail="Failed to delete review")

@router.get("/service/{service_id}", response_model=List[ReviewRead])
def get_reviews_for_service_endpoint(
    service_id: int,
    session: Session = Depends(get_session)
):
    return get_reviews_for_service(session, service_id)

@router.get("/provider/{provider_id}", response_model=List[ReviewRead])
def get_reviews_for_provider_endpoint(
    provider_id: int,
    session: Session = Depends(get_session)
):
    return get_reviews_for_provider(session, provider_id)

@router.get("/customer/{customer_id}", response_model=List[ReviewRead])
def get_reviews_for_customer_endpoint(
    customer_id: int,
    session: Session = Depends(get_session)
):
    return get_reviews_for_customer(session, customer_id) 