from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class CategoryBase(SQLModel):
    name: str
    description: str
    icon: Optional[str] = None
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id")
    is_active: bool = Field(default=True)

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    parent: Optional["Category"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Category.id"}
    )
    children: List["Category"] = Relationship(back_populates="parent")
    services: List["Service"] = Relationship(back_populates="category")

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

class CategoryWithChildren(CategoryRead):
    children: List["CategoryRead"]

class CategoryWithServices(CategoryRead):
    services: List["ServiceRead"]

class CategoryStats(SQLModel):
    total_services: int
    active_services: int
    total_providers: int
    average_rating: float
    total_bookings: int

if TYPE_CHECKING:
    from modules.service.models import Service, ServiceRead 