from sqlmodel import Session, select
from typing import List, Optional
from .models import Category, CategoryCreate, CategoryStats
from modules.service.models import Service
from modules.provider.models import ProviderProfile

def create_category(session: Session, category_data: CategoryCreate) -> Category:
    db_category = Category(**category_data.dict())
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

def get_category(session: Session, category_id: int) -> Optional[Category]:
    statement = select(Category).where(Category.id == category_id)
    return session.exec(statement).first()

def update_category(session: Session, category_id: int, category_data: CategoryCreate) -> Optional[Category]:
    category = get_category(session, category_id)
    if category:
        for key, value in category_data.dict().items():
            setattr(category, key, value)
        session.add(category)
        session.commit()
        session.refresh(category)
    return category

def delete_category(session: Session, category_id: int) -> bool:
    category = get_category(session, category_id)
    if category:
        session.delete(category)
        session.commit()
        return True
    return False

def get_all_categories(session: Session, active_only: bool = False) -> List[Category]:
    statement = select(Category)
    if active_only:
        statement = statement.where(Category.is_active == True)
    return session.exec(statement).all()

def get_category_with_children(session: Session, category_id: int) -> Optional[Category]:
    category = get_category(session, category_id)
    if category:
        # children are loaded via relationship
        return category
    return None

def get_category_with_services(session: Session, category_id: int) -> Optional[Category]:
    category = get_category(session, category_id)
    if category:
        # services are loaded via relationship
        return category
    return None

def get_category_stats(session: Session, category_id: int) -> Optional[CategoryStats]:
    category = get_category(session, category_id)
    if not category:
        return None
    services = category.services
    total_services = len(services)
    active_services = len([s for s in services if s.is_available])
    provider_ids = set(s.provider_id for s in services)
    total_providers = len(provider_ids)
    ratings = [s.provider.rating for s in services if hasattr(s.provider, 'rating') and s.provider.rating is not None]
    average_rating = sum(ratings) / len(ratings) if ratings else 0
    total_bookings = sum(len(s.bookings) for s in services)
    return CategoryStats(
        total_services=total_services,
        active_services=active_services,
        total_providers=total_providers,
        average_rating=average_rating,
        total_bookings=total_bookings
    ) 