from sqlmodel import Session, select, or_
from datetime import datetime
from typing import List, Optional
from .models import Service, ServiceCreate, ServiceSearchParams, ServiceWithProvider
from modules.provider.services import get_profile as get_provider_profile

def create_service(session: Session, provider_id: int, service_data: ServiceCreate) -> Service:
    # Verify provider exists
    provider = get_provider_profile(session, provider_id)
    if not provider:
        raise ValueError("Provider not found")

    db_service = Service(
        provider_id=provider_id,
        **service_data.dict()
    )
    session.add(db_service)
    session.commit()
    session.refresh(db_service)
    return db_service

def get_service(session: Session, service_id: int) -> Optional[Service]:
    statement = select(Service).where(Service.id == service_id)
    return session.exec(statement).first()

def update_service(session: Session, service_id: int, service_data: ServiceCreate) -> Optional[Service]:
    service = get_service(session, service_id)
    if service:
        for key, value in service_data.dict().items():
            setattr(service, key, value)
        service.updated_at = datetime.utcnow()
        session.add(service)
        session.commit()
        session.refresh(service)
    return service

def delete_service(session: Session, service_id: int) -> bool:
    service = get_service(session, service_id)
    if service:
        session.delete(service)
        session.commit()
        return True
    return False

def get_provider_services(session: Session, provider_id: int) -> List[Service]:
    statement = select(Service).where(Service.provider_id == provider_id)
    return session.exec(statement).all()

def search_services(session: Session, params: ServiceSearchParams) -> List[ServiceWithProvider]:
    # Start with base query
    query = select(Service)

    # Apply filters
    if params.category_id:
        query = query.where(Service.category_id == params.category_id)
    
    if params.min_price is not None:
        query = query.where(Service.price >= params.min_price)
    
    if params.max_price is not None:
        query = query.where(Service.price <= params.max_price)
    
    if params.is_available is not None:
        query = query.where(Service.is_available == params.is_available)
    
    if params.search_query:
        search = f"%{params.search_query}%"
        query = query.where(
            or_(
                Service.title.ilike(search),
                Service.description.ilike(search)
            )
        )

    # Apply sorting
    if params.sort_by:
        if params.sort_by == "price":
            query = query.order_by(
                Service.price.desc() if params.sort_order == "desc" else Service.price.asc()
            )
        elif params.sort_by == "rating":
            # Join with provider profile to sort by rating
            query = query.join(Service.provider).order_by(
                Service.provider.rating.desc() if params.sort_order == "desc" else Service.provider.rating.asc()
            )

    # Execute query
    services = session.exec(query).all()

    # Filter by minimum rating if specified
    if params.min_rating is not None:
        services = [
            service for service in services
            if service.provider.rating >= params.min_rating
        ]

    return services

def get_featured_services(session: Session, limit: int = 5) -> List[ServiceWithProvider]:
    # Get services from highly rated providers
    statement = (
        select(Service)
        .join(Service.provider)
        .where(Service.provider.rating >= 4.5)
        .where(Service.is_available == True)
        .order_by(Service.provider.rating.desc())
        .limit(limit)
    )
    return session.exec(statement).all()

def get_services_by_category(session: Session, category_id: int) -> List[Service]:
    statement = select(Service).where(Service.category_id == category_id)
    return session.exec(statement).all()

def toggle_service_availability(session: Session, service_id: int) -> Optional[Service]:
    service = get_service(session, service_id)
    if service:
        service.is_available = not service.is_available
        service.updated_at = datetime.utcnow()
        session.add(service)
        session.commit()
        session.refresh(service)
    return service

def get_service_stats(session: Session, service_id: int) -> dict:
    service = get_service(session, service_id)
    if not service:
        raise ValueError("Service not found")

    # Get total bookings
    total_bookings = len(service.bookings)
    
    # Get completed bookings
    completed_bookings = [b for b in service.bookings if b.status == "completed"]
    
    # Calculate average rating
    ratings = [r.rating for r in service.provider.reviews]
    average_rating = sum(ratings) / len(ratings) if ratings else 0

    return {
        "total_bookings": total_bookings,
        "completed_bookings": len(completed_bookings),
        "average_rating": average_rating,
        "total_revenue": sum(b.total_price for b in completed_bookings)
    } 