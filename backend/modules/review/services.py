from sqlmodel import Session, select
from typing import List, Optional
from .models import Review, ReviewCreate

def create_review(session: Session, review_data: ReviewCreate) -> Review:
    db_review = Review(**review_data.dict())
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

def get_review(session: Session, review_id: int) -> Optional[Review]:
    statement = select(Review).where(Review.id == review_id)
    return session.exec(statement).first()

def update_review(session: Session, review_id: int, review_data: ReviewCreate) -> Optional[Review]:
    review = get_review(session, review_id)
    if review:
        for key, value in review_data.dict().items():
            setattr(review, key, value)
        session.add(review)
        session.commit()
        session.refresh(review)
    return review

def delete_review(session: Session, review_id: int) -> bool:
    review = get_review(session, review_id)
    if review:
        session.delete(review)
        session.commit()
        return True
    return False

def get_reviews_for_service(session: Session, service_id: int) -> List[Review]:
    statement = select(Review).where(Review.service_id == service_id)
    return session.exec(statement).all()

def get_reviews_for_provider(session: Session, provider_id: int) -> List[Review]:
    statement = select(Review).where(Review.provider_id == provider_id)
    return session.exec(statement).all()

def get_reviews_for_customer(session: Session, customer_id: int) -> List[Review]:
    statement = select(Review).where(Review.customer_id == customer_id)
    return session.exec(statement).all() 