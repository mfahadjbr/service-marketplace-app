from sqlmodel import Session, select, or_
from typing import List, Optional
from .models import Location, LocationCreate, LocationSearchParams

def create_location(session: Session, location_data: LocationCreate) -> Location:
    db_location = Location(**location_data.dict())
    session.add(db_location)
    session.commit()
    session.refresh(db_location)
    return db_location

def get_location(session: Session, location_id: int) -> Optional[Location]:
    statement = select(Location).where(Location.id == location_id)
    return session.exec(statement).first()

def update_location(session: Session, location_id: int, location_data: LocationCreate) -> Optional[Location]:
    location = get_location(session, location_id)
    if location:
        for key, value in location_data.dict().items():
            setattr(location, key, value)
        session.add(location)
        session.commit()
        session.refresh(location)
    return location

def delete_location(session: Session, location_id: int) -> bool:
    location = get_location(session, location_id)
    if location:
        session.delete(location)
        session.commit()
        return True
    return False

def search_locations(session: Session, params: LocationSearchParams) -> List[Location]:
    query = select(Location)
    if params.city:
        query = query.where(Location.city.ilike(f"%{params.city}%"))
    if params.state:
        query = query.where(Location.state.ilike(f"%{params.state}%"))
    if params.country:
        query = query.where(Location.country.ilike(f"%{params.country}%"))
    if params.is_active is not None:
        query = query.where(Location.is_active == params.is_active)
    if params.query:
        search = f"%{params.query}%"
        query = query.where(
            or_(
                Location.name.ilike(search),
                Location.address.ilike(search),
                Location.city.ilike(search),
                Location.state.ilike(search),
                Location.country.ilike(search)
            )
        )
    return session.exec(query).all()

def get_all_locations(session: Session, active_only: bool = False) -> List[Location]:
    statement = select(Location)
    if active_only:
        statement = statement.where(Location.is_active == True)
    return session.exec(statement).all() 